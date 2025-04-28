from biosensor_new import Ui_MainWindow
from PyQt5 import QtWidgets,QtCore,QtGui
import os
from PyQt5.QtWidgets import QMessageBox
# from splash_screen_ui import Ui_SplashScreen
# from PyQt5.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
class data:
    def __init__(self,fig_create_num,wavelengths,powers,peak_power,peak_wavelength,subplot,canvas):
        self.fig_create_num = fig_create_num
        self.wavelengths = wavelengths
        self.powers = powers
        self.peak_power = peak_power
        self.peak_wavelength = peak_wavelength
        self.subplot = subplot
        self.canvas = canvas