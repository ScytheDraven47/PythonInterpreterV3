# Ben Rogers-McKee (ScytheDraven47)
# 02/03/2017
#
# Validation file for Interpreter project

import re
import doctest
from datetime import datetime


class Validate:
    @staticmethod
    def validate_emp_id(emp_id):
        """
        Checks if given Employee ID is a valid format.
        (A001 - Z999)

        :param emp_id: str
        :return: bool

        >>> Validate.validate_emp_id("A001")
        True
        >>> Validate.validate_emp_id("a001")
        False
        """
        valid_emp_id = bool(re.search("^[A-Z][0-9]{3}$", str(emp_id)))
        return valid_emp_id

    @staticmethod
    def validate_gender(gender):
        """
        Checks if given Gender is a valid format.
        (M/m or F/f)

        :param gender: str
        :return: bool

        >>> Validate.validate_gender("M")
        True
        >>> Validate.validate_gender("Male")
        False
        """
        valid_gender = bool(re.search("^(M|F)$", str(gender).upper()))
        return valid_gender

    @staticmethod
    def validate_age(age):
        """
        Checks if given Age is a valid format.
        (10 - 99)

        :param age: str / int
        :return: bool

        >>> Validate.validate_age(22)
        True
        >>> Validate.validate_age(6)
        False
        """
        valid_age = bool(re.search("^[0-9]{2}$", str(age)))
        return valid_age

    @staticmethod
    def validate_sales(sales):
        """
        Checks if given Sales is a valid format.
        (10 - 999)

        :param sales: str / int
        :return: bool

        >>> Validate.validate_sales(42)
        True
        >>> Validate.validate_sales(9999)
        False
        """
        valid_sales = bool(re.search("^[0-9]{2,3}$", str(sales)))
        return valid_sales

    @staticmethod
    def validate_bmi(bmi):
        """
        Checks if given BMI is a valid format.
        (Normal, Underweight, Overweight, Obese)

        :param bmi: str
        :return: bool value

        >>> Validate.validate_bmi("Normal")
        True
        >>> Validate.validate_bmi("Skinny")
        False
        """
        valid_bmi = bool(re.search("^normal$|^overweight$|^obese$|^underweight$", str(bmi).lower()))
        return valid_bmi

    @staticmethod
    def validate_salary(salary):
        """
        Checks if given Salary is a valid format.
        (10 - 999)

        :param salary: str / int
        :return: bool

        >>> Validate.validate_salary(180)
        True
        >>> Validate.validate_salary(-1)
        False
        """
        valid_salary = bool(re.search("^[0-9]{2,3}$", str(salary)))
        return valid_salary

    @staticmethod
    def validate_birthday(birthday):
        """
        Checks if given Birthday is a valid format.
        (DD-MM-YYYY)

        :param birthday: str / datetime
        :return: bool

        >>> Validate.validate_birthday("08-07-1994")
        True
        >>> Validate.validate_birthday("08/07/1994")
        False
        """
        if type(birthday) == datetime:
            return True
        elif type(birthday) == str:
            try:
                valid_birthday = bool(datetime.strptime(birthday, '%d-%m-%Y'))
                return valid_birthday
            except ValueError:
                return False
        else:
            return False

    @staticmethod
    def validate_age_birthday(age, birthday):
        """
        Checks if given Age and Birthday match correctly.

        :param age: str / int
        :param birthday: str / datetime
        :return: bool

        >>> Validate.validate_age_birthday(22, "08-07-1994")
        True
        >>> Validate.validate_age_birthday(42, "08-07-1994")
        False
        """
        if type(birthday) == datetime:
            actual_age = datetime.now() - birthday
        else:
            actual_age = datetime.now() - datetime.strptime(birthday, '%d-%m-%Y')
        return bool(int(actual_age.days / 365.25) == int(age))

    def validate_all(self, input_data):
        """
        Checks if all given Employee Data is valid, according to the validate functions.

        :param input_data: list
        :return: list
        """
        checklist = {'emp_id': self.validate_emp_id(input_data['emp_id']),
                     'gender': self.validate_gender(input_data['gender']),
                     'age': self.validate_age(input_data['age']),
                     'sales': self.validate_sales(input_data['sales']),
                     'bmi': self.validate_bmi(input_data['bmi']),
                     'salary': self.validate_salary(input_data['salary']),
                     'birthday': self.validate_birthday(input_data['birthday'])}
        return checklist

if __name__ == '__main__':
    doctest.testmod()
