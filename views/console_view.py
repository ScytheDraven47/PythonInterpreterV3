# Ben Rogers-McKee (ScytheDraven47)
# 08/03/2017
#
# ConsoleView for Interpreter Program

from views.view import IView


class ConsoleView(IView):
    def get_data(self, query):
        """Returns raw user input"""
        result = input("{}: ".format(query))
        return result

    def output(self, message):
        """Prints message"""
        print(message)
