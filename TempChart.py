from PySide6.QtWidgets import QWidget, QHBoxLayout, QSlider, QMessageBox
from PySide6.QtCharts import QChart, QLineSeries, QChartView, QSplineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QColor, QMouseEvent


class TempChart(QWidget):
    def __init__(self, parent):
        super(TempChart, self).__init__(parent)

        self.axis_time = QDateTimeAxis()
        self.axis_time.setTitleText("Zeitachse")
        self.axis_time.setFormat("mm.ss")
        self.axis_time.setTickCount(6)
        self.axis_time.setGridLineColor(QColor("red"))
        self.axis_time.setRange(QDateTime.currentDateTime(), QDateTime.currentDateTime().addSecs(5 * 60))

        self.axis_percent = QValueAxis()
        self.axis_percent.setTitleText("Prozent")
        self.axis_percent.setRange(0, 100)

        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("x-Achse")
        self.axis_x.setRange(0, 5)

        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("y-Achse")
        self.axis_y.setRange(0, 20)

        self.chart = QChart()
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_time, Qt.AlignTop)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.chart.addAxis(self.axis_percent, Qt.AlignRight)

        self.chart_view = QChartView()
        self.chart_view.setChart(self.chart)

        self.my_layout = QHBoxLayout()
        self.my_layout.addWidget(self.chart_view)

        self.slider = QSlider()
        self.slider.valueChanged.connect(self.addPoint)
        self.my_layout.addWidget(self.slider)

        self.setLayout(self.my_layout)

        self.series = QSplineSeries()
        self.chart.addSeries(self.series)
        self.series.setName("f(x) = x^2")
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

#        self.series.append(0, 0)
#        self.series.append(1, 1)
#        self.series.append(2, 4)
#        self.series.append(3, 9)
#        self.series.append(4, 16)
#        self.series.append(5, 25)

        self.series_2 = QLineSeries()
        self.chart.addSeries(self.series_2)
        self.series_2.attachAxis(self.axis_time)
        self.series_2.attachAxis(self.axis_percent)
        self.series_2.setName("Prozent über Zeit")

    def addPoint(self, percent):
        self.series_2.append(QDateTime.currentDateTime().toMSecsSinceEpoch(), percent)

    def mousePressEvent(self, event: QMouseEvent):
        if event.isBeginEvent():
            event.accept()
            self.series_2.setName("Du hälst die Maus gedrückt.")
        elif event.isEndEvent():
            event.accept()
            self.series_2.setName("Du hälst die Maus nicht mehr gedrückt.")

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.series_2.setName("Du hälst die Maus nicht mehr gedrückt.")

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        msgBox = QMessageBox()

        text = "Sie haben auf die Position\n"
        text += "x: " + str(event.x()) + "\n"
        text += "y: " + str(event.y()) + "\n"
        text += "global x: " + str(event.globalX()) + "\n"
        text += "global y: " + str(event.globalY()) + "\n"
        text += "doppelt geklickt."

        msgBox.setText(text)

        msgBox.exec()

        maped_point = self.chart.mapToValue(event.pos(), self.series_2)
        self.series_2.append(maped_point)

