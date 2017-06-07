# Ben Rogers-McKee (ScytheDraven47)
# 20/03/2017
#
# Main file for Interpreter project

# Imports -------------------------------------------
import cmd
from sys import argv
from datetime import datetime
from controllers.main_controller import InterpreterController
from views.database_view import DatabaseView
from views.excel_view import ExcelView
from builder.graph_builder import BoxGraphBuilder, PieGraphBuilder, ScatterGraphBuilder, GraphDirector
# ---------------------------------------------------

# Declaration ---------------------------------------
ic = InterpreterController()
# ---------------------------------------------------


class MainFlow(cmd.Cmd):
    excel_file = "data_src/OfficialData.xlsx"
    database_name = "data_src/db_test.db"
    prompt = "Interpreter >>>"

    # def do_add_manual_data(self, line):
    #     """
    #     Add data manually, via user input.
    #     Each piece of data will be prompted.
    #     Syntax: add_manual_data
    #     """
    #     if len(line) > 0:
    #         ic.log.output("Incorrect syntax." + str(self.do_add_manual_data.__doc__))
    #     try:
    #         ic.get_manual_data()
    #     except Exception as err:
    #         ic.log.output(err)

    def do_show_data(self, line):
        """
        Prints current held data.
        Syntax: show_data
        """
        show_data_flag = self.valid_flag(line, [], 0, self.do_show_data.__doc__)
        if show_data_flag == 0:
            ic.show_console_data()
        return show_data_flag

    def do_pull_data(self, line):
        """
        Adds data from a chosen source.
        If excel, must contain data in a sheet labelled 'input'
        Syntax: pull_data [-d|-e]
        [-d] Pulls from chosen database
        [-e] Pulls from chosen excel spreadsheet
        """
        pull_flag = self.valid_flag(line, ["-d", "-e"], 1, self.do_pull_data.__doc__)
        if pull_flag == "-d":
            view = DatabaseView()
            pull_file = self.database_name
        elif pull_flag == "-e":
            view = ExcelView()
            pull_file = self.excel_file
        else:
            return pull_flag
        try:
            ic.get_data(pull_file, view)
        except FileNotFoundError:
            ic.log.output("File does not exist... Please use 'change_data_source [-d|-e]' to edit data source.")
            return 3
        except KeyError:
            ic.log.output("File exists, but there is no worksheet labelled 'input'.")
            return 4
        return 0

    def do_push_data(self, line):
        """
        Sends data to a chosen source.
        Syntax: push_data [-d|-e}
        [-d] Saves to chosen database
        [-e] Saves to chosen excel spreadsheet
        """
        push_flag = self.valid_flag(line, ["-d", "-e"], 1, self.do_push_data.__doc__)
        if push_flag == "-d":
            view = DatabaseView()
            push_file = self.database_name
        elif push_flag == "-e":
            view = ExcelView()
            push_file = self.excel_file
        else:
            return push_flag
        ic.save_data(push_file, view)
        return 0

    def do_validate(self, line):
        """
        Validates current data, removing any data that is invalid.
        Syntax: validate
        """
        validate_flag = self.valid_flag(line, [], 0, self.do_validate.__doc__)
        if validate_flag == 0:
            count = ic.check()
            ic.log.output(str(count) + " counts of invalid data found.")
        return validate_flag

    def do_change_data_source(self, line):
        """
        Changes the source file to save to or load from.
        Syntax: change_data_source [-d|-e] <filename.xlsx>
        [-d] changes database name (requires extension)
        [-e] changes excel file name (requires extension)
        """
        cds_flag = self.valid_flag(line, ["-d", "-e"], 2, self.do_change_data_source.__doc__)
        if type(cds_flag) == int:
            return cds_flag
        filename = line.split()[1]
        if cds_flag == "-d" and filename.endswith(".db"):
            self.database_name = filename
        elif cds_flag == "-e" and filename.endswith(".xlsx"):
            self.excel_file = filename
        else:
            ic.log.output("Incorrect file, please use .xlsx or .db")
            return 5
        return 0

    def do_show_data_source(self, line):
        """
        Shows the source files to save to and load from.
        Syntax: show_data_source
        """
        sds_flag = self.valid_flag(line, [], 0, self.do_show_data_source.__doc__)
        if sds_flag == 0:
            ic.log.output("Current settings are:\n"
                          "Database Name: " + self.database_name + "\n"
                          "Excel Name: " + self.excel_file + "\n")
        return sds_flag

    def do_save_pickle(self, line):
        """
        Saves current data inside a pickle. (no extension required)
        Syntax: save_pickle <pickle_name>
        """
        import pickle
        args = line.split()
        if len(args) == 1:
            with open(args[0]+".pickle", 'wb') as f:
                pickle.dump(ic.all_data, f)
        else:
            ic.log.output("Incorrect syntax." + str(self.do_save_pickle.__doc__))
            return 1
        return 0

    def do_load_pickle(self, line):
        """
        Loads given pickle into current data. (no extension required)
        This is a replacement, not additional.
        Syntax: load_pickle <pickle_name>
        """
        import pickle
        args = line.split()
        if len(args) == 1:
            try:
                with open(args[0]+".pickle", 'rb') as f:
                    ic.all_data = pickle.load(f)
            except FileNotFoundError:
                ic.log.output("Pickle doesn't exist... Please type the name of an existing pickle")
                return 3
        else:
            ic.log.output("Incorrect syntax." + str(self.do_save_pickle.__doc__))
            return 1
        return 0

    def do_graph(self, line):
        """
        Creates a graph of data, given a valid flag.
        Options are as follows:
            graph [--scatter, --pie, --box]
        Scatter
            Graphs the relationship between sales and salary per employee as a scatter plot
            Syntax: graph --scatter
        Pie
            Graphs the BMIs of employees as a pie chart
            Syntax: graph --pie
        Box
            Graphs the sales and salary of employees as a box plot
            Syntax: graph --box
        """
        options = {
            "--pie": PieGraphBuilder(),
            "--scatter": ScatterGraphBuilder(),
            "--box": BoxGraphBuilder()
        }
        graph_flag = self.valid_flag(line, options.keys(), 1, self.do_graph.__doc__)
        if graph_flag in options.keys():
            builder = options[graph_flag]
        else:
            return graph_flag
        director = GraphDirector(builder)
        director.make_graph(ic.all_data)
        graph = builder.get_graph()
        graph.show()
        return 0

    # def do_graph_scatter(self, line):
    #     """
    #     Graphs the relationship between sales and salary per employee as a scatter plot
    #     Syntax: graph_scatter
    #     """
    #     graph_flag = self.valid_flag(line, [], 0, self.do_graph_scatter.__doc__)
    #     if graph_flag == 0:
    #         scatter_builder = graph.ScatterGraphBuilder()
    #         director = graph.GraphDirector(scatter_builder)
    #         director.make_graph(ic.all_data)
    #         scatter_builder.get_graph()
    #         # sales = []
    #         # salary = []
    #         # for data in ic.all_data:
    #         #     sales.append(data['sales'])
    #         #     salary.append(data['salary'])
    #         # import matplotlib.pyplot as plt
    #         # plt.plot(sales, salary, 'bo')
    #         # plt.axis([0, 999, 0, 999])
    #         # plt.xlabel("# of Sales")
    #         # plt.ylabel("Salary (in $1000's)")
    #         # plt.title("Sales by salary per employee")
    #         # plt.show()
    #     return graph_flag
    #
    # def do_graph_pie(self, line):
    #     """
    #     Graphs the BMIs of employees as a pie chart
    #     Syntax: graph_pie
    #     """
    #     graph_flag = self.valid_flag(line, [], 0, self.do_graph_pie.__doc__)
    #     if graph_flag == 0:
    #         pie_builder = graph.PieGraphBuilder()
    #         director = graph.GraphDirector(pie_builder)
    #         director.make_graph(ic.all_data)
    #         pie_builder.get_graph()
    #         # array = []
    #         # for data in ic.all_data:
    #         #     array.append(data['bmi'].lower())
    #         # array.sort()
    #         # array2 = {x: array.count(x) for x in array}
    #         # labels, numbers = list(array2.keys()), list(array2.values())
    #         # import matplotlib.pyplot as plt
    #         # plt.pie(numbers, explode=(0.1, 0, 0, 0), labels=labels, autopct='%1.1f%%', shadow=True)
    #         # plt.title("Body Mass Index per employee")
    #         # plt.show()
    #     return graph_flag
    #
    # def do_graph_box(self, line):
    #     """
    #     Graphs the sales and salary of employees as a box plot
    #     Syntax: graph_box
    #     """
    #     graph_flag = self.valid_flag(line, [], 0, self.do_graph_box.__doc__)
    #     if graph_flag == 0:
    #         box_builder = graph.BoxGraphBuilder()
    #         director = graph.GraphDirector(box_builder)
    #         director.make_graph(ic.all_data)
    #         box_builder.get_graph()
    #         # male, female = [],[]
    #         # for data in ic.all_data:
    #         #     if data['gender'] is 'M':
    #         #         male.append(data['salary'])
    #         #     else:
    #         #         female.append(data['salary'])
    #         # all_data = [male, female]
    #         # import matplotlib.pyplot as plt
    #         # box_plot = plt.boxplot(all_data, labels=['Male', 'Female'], vert=True, patch_artist=True)
    #         # colors = ['pink', 'lightblue']
    #         # for patch, color in zip(box_plot['boxes'], colors):
    #         #     patch.set_facecolor(color)
    #         # plt.title("Salary per employee")
    #         # plt.show()
    #     return graph_flag

    def do_clear(self, line):
        """
        Clears current held data
        Syntax: clear
        """
        clear_flag = self.valid_flag(line, [], 0, self.do_clear.__doc__)
        if clear_flag == 0:
            ic.all_data = []
        return clear_flag

    def do_quit(self, line):
        """
        Quits program
        Syntax: quit
        """
        quit_flag = self.valid_flag(line, [], 0, self.do_quit.__doc__)
        if quit_flag == 0:
            print("Quitting...")
            raise SystemExit
        return quit_flag

    @staticmethod
    def valid_flag(line, expected_flags, expected_arg_num, error_string):
        args = line.split()
        if len(args) != expected_arg_num:
            ic.log.output("Incorrect syntax. " + error_string)
            return 1
        if args == expected_flags:
            return 0
        elif args[0] in expected_flags:
            return args[0]
        else:
            ic.log.output("Invalid flag. " + error_string)
            return 2

    # Start of Interpreter CMD
    def start(self):
        ic.log.output("------- " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " -------\n"
                      "This is the python interpreter program, type 'help' for commands\n"
                      "Current settings are:\n"
                      "Database Name: " + self.database_name + "\n"
                      "Excel File: " + self.excel_file + "\n"
                      "Starting...\n")
        return 0

if __name__ == "__main__":
    m = MainFlow()
    m.start()
    # m.cmdloop()
    if len(argv) == 1:
        m.cmdloop()
    elif len(argv[:1]) == 1:
        flag = argv[1:][0]
        file = argv[1:][1]
        if flag == "-l":
            m.do_load_pickle(file)
            m.cmdloop()
        else:
            ic.log.output("Invalid flag argument. Only [-l] is valid at this time.")
    else:
        ic.log.output("Invalid command program arguments.")
