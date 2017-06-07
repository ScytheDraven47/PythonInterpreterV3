from abc import abstractmethod, ABCMeta
import matplotlib.pyplot as plt


class GraphBuilder(metaclass=ABCMeta):
    @abstractmethod
    def build_data(self, data_src):
        pass

    @abstractmethod
    def build_graph(self):
        pass

    @abstractmethod
    def build_title(self):
        pass

    def build_decorations(self):
        pass

    @staticmethod
    def get_graph():
        return plt


class ScatterGraphBuilder(GraphBuilder):
    def __init__(self):
        self.__sales = []
        self.__salary = []

    def build_data(self, data_src):
        for data in data_src:
            self.__sales.append(data['sales'])
            self.__salary.append(data['salary'])

    def build_graph(self):
        plt.plot(self.__sales, self.__salary, 'bo')

    def build_title(self):
        plt.title("Sales by salary per employee")

    def build_decorations(self):
        plt.axis([0, 999, 0, 999])
        plt.xlabel("# of Sales")
        plt.ylabel("Salary (in $1000's)")


class PieGraphBuilder(GraphBuilder):
    def __init__(self):
        self.__labels = []
        self.__numbers = []

    def build_data(self, data_src):
        array = []
        for data in data_src:
            array.append(data['bmi'].lower())
        array.sort()
        array2 = {x: array.count(x) for x in array}
        self.__labels, self.__numbers = list(array2.keys()), list(array2.values())

    def build_graph(self):
        plt.pie(self.__numbers, explode=(0.1, 0, 0, 0), labels=self.__labels, autopct='%1.1f%%', shadow=True)

    def build_title(self):
        plt.title("Body Mass Index per employee")


class BoxGraphBuilder(GraphBuilder):
    def __init__(self):
        self.__all_data = []
        self.__box_plot = None

    def build_data(self, data_src):
        male, female = [], []
        for data in data_src:
            if data['gender'] is 'M':
                male.append(data['salary'])
            else:
                female.append(data['salary'])
        self.__all_data = [male, female]

    def build_graph(self):
        self.__box_plot = plt.boxplot(self.__all_data, labels=['Male', 'Female'], vert=True, patch_artist=True)

    def build_title(self):
        plt.title("Body Mass Index per employee")

    def build_decorations(self):
        colors = ['pink', 'lightblue']
        for patch, color in zip(self.__box_plot['boxes'], colors):
            patch.set_facecolor(color)


class GraphDirector:
    def __init__(self, builder):
        self.__builder = builder

    def make_graph(self, data_src):
        self.__builder.build_data(data_src)
        self.__builder.build_graph()
        self.__builder.build_decorations()
        self.__builder.build_title()
