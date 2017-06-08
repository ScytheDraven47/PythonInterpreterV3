# Ben Rogers-McKee (ScytheDraven47)
# 02/03/2017
#
# Validation file for Interpreter project

from strategy.validate_strategy import TwoDigit, DateStringOrDatetime, \
    BMIWord, EmployeeID, OneLetterGender, TwoOrThreeDigit, ValidateContext


class Validate:
    @staticmethod
    def validate_all(input_data):
        """
        Checks if all given Employee Data is valid, according to the validate functions.

        :param input_data: list
        :return: list
        """
        emp_id = ValidateContext(EmployeeID())
        gender = ValidateContext(OneLetterGender())
        age = ValidateContext(TwoDigit())
        sales = ValidateContext(TwoOrThreeDigit())
        bmi = ValidateContext(BMIWord())
        salary = ValidateContext(TwoOrThreeDigit())
        birthday = ValidateContext(DateStringOrDatetime())

        checklist = {'emp_id': emp_id.validate_data(input_data['emp_id']),
                     'gender': gender.validate_data(input_data['gender']),
                     'age': age.validate_data(input_data['age']),
                     'sales': sales.validate_data(input_data['sales']),
                     'bmi': bmi.validate_data(input_data['bmi']),
                     'salary': salary.validate_data(input_data['salary']),
                     'birthday': birthday.validate_data(input_data['birthday'])}
        return checklist
