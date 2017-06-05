# Ben Rogers-McKee (ScytheDraven47)
# 09/05/2017
#
# FileView for Interpreter Program

from abc import ABCMeta, abstractmethod


class FileView(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self, filename):
        pass

    @abstractmethod
    def output(self, data_to_output, filename):
        pass
