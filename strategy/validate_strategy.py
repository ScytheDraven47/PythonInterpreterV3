# Ben Rogers-McKee (ScytheDraven47)
# 08/06/2017
#
# Strategy for Validation for Interpreter project

from abc import abstractmethod, ABCMeta
import re
from datetime import datetime


class ValidateContext:
    def __init__(self, data_type):
        self.__type = data_type

    def validate_data(self, data):
        return self.__type.validate(data)


class AbstractValidateStrategy(metaclass=ABCMeta):
    @abstractmethod
    def validate(self, data):
        pass


class EmployeeID(AbstractValidateStrategy):
    def validate(self, data):
        return bool(re.search("^[A-Z][0-9]{3}$", str(data)))


class OneLetterGender(AbstractValidateStrategy):
    def validate(self, data):
        return bool(re.search("^([MF])$", str(data).upper()))


class TwoDigit(AbstractValidateStrategy):
    def validate(self, data):
        return bool(re.search("^[0-9]{2}$", str(data)))


class TwoOrThreeDigit(AbstractValidateStrategy):
    def validate(self, data):
        return bool(re.search("^[0-9]{2,3}$", str(data)))


class BMIWord(AbstractValidateStrategy):
    def validate(self, data):
        return bool(re.search("^normal$|^overweight$|^obese$|^underweight$", str(data).lower()))


class DateStringOrDatetime(AbstractValidateStrategy):
    def validate(self, data):
        if type(data) == datetime:
            return True
        elif type(data) == str:
            try:
                valid_birthday = bool(datetime.strptime(data, '%d-%m-%Y'))
                return valid_birthday
            except ValueError:
                return False
        else:
            return False


class AgeAndBirthday(AbstractValidateStrategy):
    def validate(self, data):
        age = data[0]
        birthday = data[1]
        if type(birthday) == datetime:
            actual_age = datetime.now() - birthday
        else:
            actual_age = datetime.now() - datetime.strptime(birthday, '%d-%m-%Y')
        return bool(int(actual_age.days / 365.25) == int(age))
