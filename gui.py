import sys
from PyQt6 import QtWidgets
from cls import *
import ui


class App(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.main_tab.tabBarClicked.connect(self.market_on)

    def get_query(self, type_id):
        query = MainQuery(type_id)


def run_app():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec()
