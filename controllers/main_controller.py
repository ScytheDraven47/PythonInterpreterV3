# Ben Rogers-McKee (ScytheDraven47)
# 08/03/2017
#
# Controller for Interpreter project

from datetime import datetime

from models.model_validator import Validate
from views.console_view import ConsoleView
from strategy.validate_strategy import AgeAndBirthday, ValidateContext


class InterpreterController:
    def __init__(self):
        self.all_data = []
        self.log = ConsoleView()

    # def get_manual_data(self):
    #     input_data = {
    #         'emp_id': self.log.get_data("What is your employee ID? (A001)"),
    #         'gender': self.log.get_data("What is your gender? (M/F)"),
    #         'age': int(self.log.get_data("What is your age? (16-99)")),
    #         'sales': int(self.log.get_data("What is your total sales? (01-999)")),
    #         'bmi': self.log.get_data("What is your BMI? (Normal/Overweight/Obese/Underweight)"),
    #         'salary': int(self.log.get_data("What is your salary in thousands? (01-999)")),
    #         'birthday': self.log.get_data("What is your birthday? (DD-MM-YYYY)"),
    #     }
    #     self.all_data.append(input_data)

    def show_console_data(self):
        self.log.output(self.to_string(self.all_data))

    def get_data(self, filename, view):
        data_array = view.get_data(filename)
        for i in data_array:
            input_data = {
                'emp_id': i[0],
                'gender': i[1],
                'age': i[2],
                'sales': i[3],
                'bmi': i[4],
                'salary': i[5],
                'birthday': i[6],
            }
            self.all_data.append(input_data)

    def save_data(self, filename, view):
        view.output(self.all_data, filename)

    def check(self):
        """
        Validates all_data using model_validator
        Runs show_errors when invalidation data is found
        """
        validate = Validate()
        age_birthday = ValidateContext(AgeAndBirthday())
        all_valid_data = []
        count = 0
        for data in self.all_data:
            checklist = validate.validate_all(data)
            if False in checklist.values():
                self.show_errors(data, checklist)
                count += 1
            elif not age_birthday.validate_data([data['age'], data['birthday']]):
                checklist['age_birthday'] = False
                self.show_errors(data, checklist)
                count += 1
            else:
                all_valid_data.append(data)
        self.all_data = all_valid_data
        return count

    def show_errors(self, data, checklist):
        for key, value in checklist.items():
            if value is False:
                self.log.output("For emp_id '" + str(data['emp_id']) + "', " + key + " is invalid")

    @staticmethod
    def to_string(_list):
        """
        Converts a list of arrays to strings separated by new commas and new lines.
        :param _list:
        :return: String of comma separated data, on new lines
        """
        result = ""
        for _dict in _list:
            result += "> "
            for key, value in _dict.items():
                if type(value) is datetime:
                    value = value.strftime('%d-%m-%Y')
                # result += ">" + key + ": " + str(value) + "\n"
                result += str(value) + ", "
            result += "\n"
        return result
