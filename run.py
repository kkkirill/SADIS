from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt
import sys
from itertools import combinations


class CalculatorConfig:
    def __init__(self):
        self.amount_of_blocks = 4
        self.spin_box_defaults = (100, 65, 30, 23)
        self.combo_box_defaults = (0, 1, 2, 3)
        self.edit_line_default = ''

    def get_default(self):
        for i in range(self.amount_of_blocks):
            yield (self.spin_box_defaults[i], self.combo_box_defaults[i], self.edit_line_default)


class Calculator(QDialog):
    def __init__(self):
        super(Calculator, self).__init__()
        self.config = CalculatorConfig()
        self.ui = uic.loadUi('main.ui', self)
        self.spin_values = [value for value in self.config.spin_box_defaults]
        self.combo1, self.combo2 = None, None
        self.massageBox = self.__create_message_box('Check the correctness of input!', False)
        self.__bind()

    @staticmethod
    def __create_message_box(message: str, is_info: bool = True) ->QMessageBox:
        temp = QMessageBox()
        temp.setIcon(QMessageBox.Information if is_info else QMessageBox.Critical)
        temp.setWindowTitle('Info' if is_info else 'Error')
        temp.setText(message)
        temp.setStandardButtons(QMessageBox.Ok)
        return temp

    def __reset(self):
        for i, (spin_box_value, combo_box_value, line_edit_value) in enumerate(self.config.get_default(), start=1):
            getattr(self, f'spinBox{i}').setValue(spin_box_value)
            getattr(self, f'comboBox{i}').setCurrentIndex(combo_box_value)
            getattr(self, f'lineEdit{i}').setText(line_edit_value)
        self.__update()

    def __bind(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.okButton.clicked.connect(self.__calculate)
        self.resetButton.clicked.connect(self.__reset)
        self.exitButton.clicked.connect(self.close)

    def __update(self):
        for i in range(self.config.amount_of_blocks):
            self.spin_values[i] = getattr(self, f'spinBox{i+1}').value()
        self.combo1 = sorted([combination for combination in combinations(self.spin_values[1:], 2)],
                             reverse=True)
        self.combo2 = sorted([combination for combination in combinations(self.spin_values[2:], 2)],
                             reverse=True)

    def __check(self) -> bool:
        return all(self.spin_values[0] > sum(combination) for combination in self.combo1) and \
               all(self.spin_values[1] > sum(combination) for combination in self.combo2)

    def __calculate(self):
        self.__update()
        if self.__check():
            total = sum(self.spin_values)
            self.massageBox = self.__create_message_box(str([round(value / total, 2) for value in self.spin_values]))
        else:
            self.massageBox = self.__create_message_box('Check the correctness of input!', False)
        self.output()
        self.massageBox.show()

    def output(self):
        def sign(value1: int, value2: int) -> str:
            return '=' if value1 == value2 else '<' if value1 < value2 else '>'
        ref = self.spin_values
        ref1 = self.combo2
        for i, val in enumerate(self.combo1, start=1):
            getattr(self, f'lineEdit{i}').setText(f'{ref[0]} {sign(ref[0],sum(val))} {val[0]} + {val[1]} = {sum(val)}')
        getattr(self, f'lineEdit{4}').setText(f'{ref[1]} > {ref1[0][0]} + {ref1[0][1]} = {sum(ref1[0])}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()

    sys.exit(app.exec_())
