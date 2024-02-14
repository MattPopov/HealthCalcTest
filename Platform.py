"""
@author: lataf 
@file: Platform.py 
@time: 11.02.2024 13:49
Модуль отвечает за консолидацию модулей
UML схема модуля
Сценарий работы модуля:
Тест модуля находится в папке model/tests.
"""

import numpy as np
import matplotlib.pyplot as plt
import math


class User:
    """Вводи и вывод данных пользователем """

    def __init__(self):
        self.health: Health = Health(self)  # ресурсы легких

    def input(self):
        ...

    @staticmethod
    def output(value):
        plt.show()
        print(f'Сердце - {value}')


class Health:
    """Управление объектами """

    def __init__(self, _user: User = None):
        self.user = _user  # Ссылка на родителя
        self.heart = Heart(self)  # ресурсы сердечно-сосудистой системы
        self.imt = IMT(self)  # индекс массы тела
        self.resp = Resp(self)  # ресурсы легких
        self.harrington = Harrington(self)  # перевод параметра в безразмерную величину

    @staticmethod
    def create_diagram():
        """Показываем диаграмму"""
        params = ['imt', 'heart', 'resp']
        results = [0.5, 0.8, 0.9, ]

        theta = np.linspace(start=0, stop=2 * np.pi, num=len(results), endpoint=False)
        theta = np.concatenate((theta, [theta[0]]))
        results = np.append(results, results[0])

        fig = plt.figure(figsize=(5, 5), facecolor='#f3f3f3')
        ax = fig.add_subplot(111, projection='polar')
        ax.plot(theta, results, linewidth=2, color="red")
        ax.set_thetagrids(range(0, 360, int(360 / len(params))), params)
        plt.yticks(np.arange(0, 1.1, 0.1), fontsize=8)
        ax.set(facecolor='#f3f3f3')
        ax.set_theta_offset(np.pi / 2)

        pl = ax.yaxis.get_gridlines()
        for line in pl:
            line.get_path()._interpolation_steps = 5
        # plt.show()


class Harrington:
    """Управление объектами """

    def __init__(self, _health: Health = None):
        self.h_bad = 0.20  # С
        self.h_good = 0.63    # С

    @staticmethod
    def calc(bad: float, good: float, value: float):
        param1 = math.log(math.log(1/0.63))
        param2 = math.log(math.log(1/0.2))
        b1 = (param1-param2)/(good-bad)
        b0 = param2-bad*b1
        good = math.exp(-math.exp(b0+b1*good))
        bad = math.exp(-math.exp(b0+b1*bad))
        value = math.exp(-math.exp(b0+b1*value))
        print(bad, good, value)
        return bad, good, value


class IMT:
    """Управление объектами """

    def __init__(self, _health: Health = None):
        self.health = _health  # Ссылка на родителя


class Resp:
    """Управление объектами """

    def __init__(self, contr: Health = None):
        self.controller = contr  # Ссылка на родителя


class Heart:
    """Управление объектами """

    def __init__(self, _health: Health = None):
        self.health = _health  # Ссылка на родителя

    def calc(self):
        self.health.create_diagram()
        self.health.user.output('хорошо')


if __name__ == '__main__':
    user = User()  # Создаем объект
    user.health.heart.calc()
    user.health.harrington.calc(320, 430, 500)
