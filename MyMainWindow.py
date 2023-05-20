from PySide6.QtWidgets import QMainWindow
from TempChart import TempChart

class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("QChartView")

        self.setCentralWidget(TempChart(self))
