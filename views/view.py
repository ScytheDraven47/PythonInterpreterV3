# Ben Rogers-McKee (ScytheDraven47)
# 08/03/2017
#
# View for Interpreter Program

from abc import ABCMeta, abstractmethod


class IView(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self, query):
        pass

    @abstractmethod
    def output(self, message):
        pass
