import re
import sys
import threading
import time
from datetime import datetime
import numpy as np
import subprocess

# from agilent_8168D_laser import LaserAgilent8168D
# from AQ2140 import Opticalmultimeter

from BBlaserFOTF import LaserBB2Filter


from biosensor_new import Ui_MainWindow
from PyQt5 import QtWidgets,QtCore,QtGui
import os
from PyQt5.QtWidgets import QMessageBox
# from splash_screen_ui import Ui_SplashScreen
# from PyQt5.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from ui_splash_screen import Ui_SplashScreen
from data import data
from pump_control import pump_control_function
# class biosensor_function(Ui_MainWindow,LaserAgilent8168D,Opticalmultimeter,pump_control_function):
class biosensor_function(Ui_MainWindow, LaserBB2Filter,pump_control_function):
    # s = sched.scheduler(time.time, time.sleep)
    
    def __init__(self):
        
        super().__init__()
        
        self.pump = pump_control_function()
        # step parameter
        self.is_connected = False
        self.is_setting_mode = False
        self.is_setting_light_source = False
        self.is_setting_sweep = False
        self.is_finish =False
        self.is_selected_manual =False


        self.can_continue = False
        # machine parameter
        self.is_laser_on = False
        self.output_value = 1450.0
        self.power_value = -13.80
        self.start_value = 1450.0
        self.delay_value = 1450.0
        self.stop_value = 1450.0
        self.step_value = 0.001
        self.is_W = False  # False if dBm
        self.status = False # True if currently busy
        self.peak_power = 0
        self.peak_wavelength = 0
        self.progress = 0
        self.is_saved= False
        self.is_run = False
        # result parameter
        self.flowrate_maximum = 50;
        self.flowrate_minimum = 6.25*10**-2;
        
        self.setupUi(MyProgram)
        MyProgram.closeEvent = self.closeEvent
        # page component
        

        ### select style
        self.selected = ("border-style: outset;\n"
            "border-width: 4px;\n"
            "border-radius: 10px;\n"
            "border-color: #000000;\n"
            "color: #FFFFFF;\n"
            "background-color: #9D59BF;\n"
                )
        self.unselected =("background-color: #9D59BF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    )
        self.selected_green = ("border-style: outset;\n"
            "border-width: 4px;\n"
            "border-radius: 10px;\n"
            "border-color: #000000;\n"
            "color: #FFFFFF;\n"
            "background-color: #3AB795;\n"
                )
        self.unselected_green =("background-color: #3AB795;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    )
        ### step style
        self.not_in_step_button = ("background-color: #BFBFBF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    )
        self.in_step_button = ("background-color: #9D59BF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    )
        self.in_step_button_green = ("background-color: #3AB795;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    )
        self.in_step_button_red = ("background-color: #ff6961;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    )
        self.not_in_step_label = ("color:#BFBFBF;")
        self.not_in_step_label_with_border = ("color:#BFBFBF;\n"                                      "color:#BFBFBF;\n"
                            "border-style: outset;\n"
                            "border-width: 3px;\n"
                            "border-radius: 10px;\n"
                            "border-color: #BFBFBF;\n")
        self.in_step_label_with_border = ("color:#3AB795;\n"
                            "border-style: outset;\n"
                            "border-width: 3px;\n"
                            "border-radius: 10px;\n"
                            "border-color: #9D59BF;\n")
        self.in_step_label = ("color:#9D59BF;")
        self.in_step_label_green = ("color:#3AB795;")
        self.in_step_label_unit = ("color:#3AB795;")
        self.in_step_input = (
            "color:#9D59BF;\n"
            "border: 2px solid #3AB795;\n"
            "padding: 0 8px;\n"
        )
        self.in_step_input_pump = (
            "color:#3AB795;\n"
            "border: 2px solid #9D59BF;\n"
            "padding: 0 8px;\n"
        )
        self.not_in_step_input = ("border: 2px solid #BFBFBF;\n"
        "padding: 0 8px;\n"
        "color:#BFBFBF")
        
        # stacked widget
        self.lightsource_pump.setCurrentIndex(0);
        # self.back_button.clicked.connect(self.change_to_figure_page)
        # select device
        self.lightsource_setting_select_button.setStyleSheet(self.not_in_step_button)
        self.lightsource_setting_select_button.setEnabled(True)
        # ritipong addon --> set range of OSA wavelength
        self.input_wavelength.setMinimum(1527.0)
        self.input_wavelength.setMaximum(1567.0)

        self.pump_setting_select_button.setStyleSheet(self.not_in_step_button)
        self.setting_device_field.setStyleSheet("")
        # # un-activate
        self.label_settingParameter.setStyleSheet(self.not_in_step_label)
        self.defaultParameter_button.setStyleSheet(self.not_in_step_button)
        self.defaultParameter_button.setEnabled(False)
        self.manualParameter_button.setStyleSheet(self.not_in_step_button)
        self.manualParameter_button.setEnabled(False)

        self.borderParameter_style = ("#setParameterField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #A49BA8;\n"
                                    "}\n")
        self.setParameterField.setStyleSheet(self.borderParameter_style)
        ## light source field
        self.label_settingLightSource.setStyleSheet(self.not_in_step_label)
        self.label_outputWavelength.setStyleSheet(self.not_in_step_label)
        self.label_outputPower.setStyleSheet(self.not_in_step_label)
        self.input_wavelength.setStyleSheet(self.not_in_step_input)
        self.input_wavelength.setReadOnly(True)
        self.input_power.setStyleSheet(self.not_in_step_input)
        self.input_power.setReadOnly(True)
        #ritipong addon
        self.input_power.setMinimum(-13)
        self.input_power.setMaximum(10)

        self.offLaser_button.setStyleSheet(self.not_in_step_button)
        self.offLaser_button.setEnabled(False)
        self.onLaser_button.setStyleSheet(self.not_in_step_button)
        self.onLaser_button.setEnabled(False)
        self.W_button.setStyleSheet(self.not_in_step_button)
        self.W_button.setEnabled(False)
        self.dBm_button.setStyleSheet(self.not_in_step_button)
        self.dBm_button.setEnabled(False)

        self.borderLightSource_style = ("#settingLightSourceField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #A49BA8;\n"
                                    "}\n")
        self.settingLightSourceField.setStyleSheet(self.borderLightSource_style)

        # ## sweep field
        self.label_wavelengthSweep.setStyleSheet(self.not_in_step_label)
        self.label_start.setStyleSheet(self.not_in_step_label)
        self.label_stop.setStyleSheet(self.not_in_step_label)
        self.label_step.setStyleSheet(self.not_in_step_label)
        self.label_stepDelay.setStyleSheet(self.not_in_step_label)
        self.label_stepDelay_2.setStyleSheet(self.not_in_step_label)
        self.label_ms.setStyleSheet(self.not_in_step_label)
        self.input_start.setReadOnly(True)
        self.input_step.setReadOnly(True)
        self.input_stop.setReadOnly(True)
        self.input_stepdelay.setReadOnly(True)
        self.input_start.setStyleSheet(self.not_in_step_input)
        self.input_step.setStyleSheet(self.not_in_step_input)
        self.input_stop.setStyleSheet(self.not_in_step_input)
        self.input_stepdelay.setStyleSheet(self.not_in_step_input)
        self.borderwavelength_style = ("#wavelenghtSweepField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #A49BA8;\n"
                                    "}\n")
        self.wavelenghtSweepField.setStyleSheet(self.borderwavelength_style)

        
        # ## connect light source
        self.connect_button.clicked.connect(self.connect_instrument);
        # ## Setting param default or manual
        self.defaultParameter_button.clicked.connect(self.default_setting_param);
        self.manualParameter_button.clicked.connect(self.manual_setting_param)

        # ## laser
        
        self.onLaser_button.clicked.connect(self.set_laser_on)
        self.offLaser_button.clicked.connect(self.set_laser_off)

        # # handle input
        self.input_wavelength.textChanged.connect(self.handle_output_wavelength_input)
        self.input_power.textChanged.connect(self.handle_output_power_input)
        self.input_start.textChanged.connect(self.handle_start_input)
        self.input_stop.textChanged.connect(self.handle_stop_input)
        self.input_step.textChanged.connect(self.handle_step_input)
        self.input_stepdelay.textChanged.connect(self.handle_step_delay_input)

        # ## W dBM converter
        self.W_button.clicked.connect(self.dBm_to_W)
        self.dBm_button.clicked.connect(self.W_to_Bm)
        
        # # Start Stop Laser
    
        ## plot graph
    

        self.wavelength = []
        self.power = []

        # self.wavelength = [1525,1525.1,1525.2,1525.1,1525.4,1525.5,1525.6,1525.7,1525.8,1525.9,1526,1526.1,1526.2,1526.1,1526.4,1526.5,1526.6,1526.7,1526.8,1526.9,1527,1527.1,1527.2,1527.1,1527.4,1527.5,1527.6,1527.7,1527.8,1527.9,1528,1528.1,1528.2,1528.1,1528.4,1528.5,1528.6,1528.7,1528.8,1528.9,1529,1529.1,1529.2,1529.1,1529.4,1529.5,1529.6,1529.7,1529.8,1529.9,1530,1530.1,1530.2,1530.1,1530.4,1530.5,1530.6,1530.7,1530.8,1530.9,1531,1531.1,1531.2,1531.1,1531.4,1531.5,1531.6,1531.7,1531.8,1531.9,1532,1532.1,1532.2,1532.1,1532.4,1532.5,1532.6,1532.7,1532.8,1532.9,1533,1533.1,1533.2,1533.1,1533.4,1533.5,1533.6,1533.7,1533.8,1533.9,1534,1534.1,1534.2,1534.1,1534.4,1534.5,1534.6,1534.7,1534.8,1534.9,1535,1535.1,1535.2,1535.1,1535.4,1535.5,1535.6,1535.7,1535.8,1535.9,1536,1536.1,1536.2,1536.1,1536.4,1536.5,1536.6,1536.7,1536.8,1536.9,1537,1537.1,1537.2,1537.1,1537.4,1537.5,1537.6,1537.7,1537.8,1537.9,1538,1538.1,1538.2,1538.1,1538.4,1538.5,1538.6,1538.7,1538.8,1538.9,1539,1539.1,1539.2,1539.1,1539.4,1539.5,1539.6,1539.7,1539.8,1539.9,1540]
        # self.power = [-43.7476,-43.7366,-44.1364,-43.1366,-43.0064,-43.9646,-43.4486,-43.5438,-43.5338,-43.6742,-44.586,-43.8858,-43.705,-44.3114,-45.0998,-45.4824,-44.9838,-45.6332,-45.7642,-47.04,-48.3224,-49.8152,-52.2128,-57.3208,-62.7824,-59.2582,-53.8532,-50.0206,-48.6364,-47.192,-46.4956,-46.2394,-45.2796,-45.5998,-45.4058,-45.2596,-45.0862,-45.3528,-45.0098,-45.0648,-44.801,-44.8846,-44.2986,-43.6876,-43.7938,-43.9008,-43.855,-43.7864,-44.9096,-43.977,-43.7568,-43.9912,-44.7348,-43.4874,-43.8444,-44.4074,-43.8796,-44.541,-44.7462,-44.5406,-44.6336,-44.1886,-44.7692,-44.5974,-44.358,-44.1904,-44.3998,-45.3082,-45.9538,-45.4758,-44.783,-46.0478,-45.8224,-45.8488,-46.2736,-47.2618,-47.7482,-50.1782,-50.9202,-53.7232,-59.5948,-65.5182,-58.2672,-52.7968,-50.0944,-48.1658,-47.25,-46.8628,-46.8382,-46.1718,-45.0204,-45.113,-45.7312,-44.9978,-45.4774,-44.5426,-44.6494,-44.809,-44.5738,-44.2668,-44.2128,-43.4992,-44.2868,-44.0858,-43.9556,-43.882,-43.871,-43.8716,-44.313,-44.5612,-44.1392,-43.96,-44.0512,-44.2212,-44.6162,-44.2736,-43.8966,-44.011,-44.8376,-44.1974,-43.895,-44.7772,-44.0686,-44.6928,-44.4762,-44.3902,-45.1422,-44.7348,-45.1646,-46.127,-46.2952,-45.7368,-46.7824,-47.5714,-48.7834,-50.8468,-53.3186,-58.1178,-66.5278,-59.8814,-54.0512,-50.7346,-48.7952,-47.6338,-47.1,-46.0734,-45.2902,-44.8232,-44.9658,-45.0306,-44.7656]
        

        # self.wavelength2 = [1525,1540]
        # self.power2 = [-43.7476,-44.7656]

        ## matplot lib
        self.figure = plt.figure( dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, None)
        self.figure.clear()
       
        self.figure.subplots_adjust(left=0.09,bottom=0.1,right=0.98,top=0.9)
        self.ax = self.figure.subplots()
        self.color_purple = '#9D59BF'
        self.color_green = "#3AB795"
        self.color_darkerpurple = "#73428C"
        self.color_gray = "#BFBFBF"
        # self.ax.style.use('dark_background')
        self.ax.plot(self.wavelength,self.power, marker='o', color=self.color_purple , markerfacecolor=self.color_darkerpurple) 
        plt.subplots_adjust(wspace=0, hspace=0)
        self.set_graph_disable()
        self.peak = 0
        self.fig_create_num = 1
        self.result_list = []
        
        # self.ax.set_xlim([1450, 1590])
        # self.ax.set_ylim([-13.8, 8])
        self.canvas.draw()

        self.reference_peak = 0
        # fig setting
        self.pump_setting_style= ("background-color: #3AB795;\n"
"border-radius: 10px;\n"
"border:none;\n"
"color: #FFFFFF;\n"
)
        self.connect_button_pump.clicked.connect(self.connect_pump_selector)
        self.initialization_button.clicked.connect(self.handle_initilize)
        self.pump_setting_select_button.clicked.connect(self.handle_click_pump_setting)  
        self.lightsource_setting_select_button.clicked.connect(self.handle_clicked_lightsource_setting)     
        self.selectorA.clicked.connect(self.handle_click_selectorA)
        self.selectorB.clicked.connect(self.handle_click_selectorB)
        self.selectorC.clicked.connect(self.handle_click_selectorC)
        self.selectorD.clicked.connect(self.handle_click_selectorD)
        self.selectorE.clicked.connect(self.handle_click_selectorE)
        self.selectorF.clicked.connect(self.handle_click_selectorF)
        self.selector_sewage.clicked.connect(self.handle_click_selectorSewage)
        self.selectorMedia.clicked.connect(self.handle_click_selectorMedia)

        # disable syringe and command
        self.border_syringe_style = ("#syringe_setup_field{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #A49BA8;\n"
                                    "}\n")
        self.border_syringe2_style = ("#selector_control_field{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #A49BA8;\n"
                                    "}\n")
        self.syringe_setup_field.setStyleSheet(self.border_syringe_style)
        self.selector_control_field.setStyleSheet(self.border_syringe2_style)
        # syringe
        self.label_syringe_setup.setStyleSheet(self.not_in_step_label)
        self.label_volume.setStyleSheet(self.not_in_step_label)
        self.label_mL.setStyleSheet(self.not_in_step_label)
        self.input_volume.setStyleSheet(self.not_in_step_input)
        self.input_volume.setReadOnly(True)
        self.aspirate_button.setStyleSheet(self.not_in_step_button)
        self.aspirate_button.setEnabled(False)
        self.dispense_button.setStyleSheet(self.not_in_step_button)
        self.dispense_button.setEnabled(False)
        self.label_volume_syringe.setStyleSheet(self.not_in_step_label)
        self.input_volume_syringe.setStyleSheet(self.not_in_step_input)
        self.input_volume.setReadOnly(True)
        self.initialization_button.setStyleSheet(self.not_in_step_button)
        self.initialization_button.setEnabled(False)
        self.label_flowrate.setStyleSheet(self.not_in_step_label)
        self.input_flowrate.setStyleSheet(self.not_in_step_input)
        self.label_uls.setStyleSheet(self.not_in_step_label)
        self.fill_button.setStyleSheet(self.not_in_step_button)
        self.fill_button.setEnabled(False)
        self.empty_button.setStyleSheet(self.not_in_step_button)
        self.empty_button.setEnabled(False)
        self.In.setStyleSheet(self.not_in_step_button)
        self.In.setEnabled(False)
        self.Out.setStyleSheet(self.not_in_step_button)
        self.Out.setEnabled(False)
        self.stop_syringe_button.setStyleSheet(self.not_in_step_button)
        self.stop_syringe_button.setEnabled(False)
        self.input_volume_syringe.setCurrentIndex(6) #set syringe pump volume -> 6 means 10 mL
        #disable combobox of input_volume_syringe
        self.input_volume_syringe.setEnabled(False)
        #--- set default value -----#
        self.volume_syringe =  1
        self.current_volume  = 1
        self.flow_rate = 1
        #---------------------------#
        self.command = ""
        self.input_volume.setValue(1) #set current syringe volume that want to feed
        self.input_volume.setMaximum(10) #set maximum volume that want to feed
        self.input_flowrate.setValue(1) #set syringe pump speed (1-slowest, 40-fastest)
        self.input_flowrate.setMaximum(50) #set maximum speed of syring pump
        self.input_flowrate.setMinimum(6.25*10**-2) #set minimum speed of syring pump
        ##selector 
        self.selectorA.setStyleSheet(self.not_in_step_button)
        self.selectorA.setEnabled(False)
        self.selectorB.setStyleSheet(self.not_in_step_button)
        self.selectorB.setEnabled(False)
        self.selectorC.setStyleSheet(self.not_in_step_button)
        self.selectorC.setEnabled(False)
        self.selectorD.setStyleSheet(self.not_in_step_button)
        self.selectorD.setEnabled(False)
        self.selectorE.setStyleSheet(self.not_in_step_button)
        self.selectorE.setEnabled(False)
        self.selectorF.setStyleSheet(self.not_in_step_button)
        self.selectorF.setEnabled(False)
        self.selectorMedia.setStyleSheet(self.not_in_step_button)
        self.selectorMedia.setEnabled(False)
        self.selector_sewage.setStyleSheet(self.not_in_step_button)
        self.selector_sewage.setEnabled(False)
        self.label_selectorcontrol.setStyleSheet(self.not_in_step_label)
        #command script

        #handle input syring
        self.input_volume_syringe.currentIndexChanged.connect(self.handle_input_volume_syring)
        self.input_volume.textChanged.connect(self.handle_input_volume)
        self.input_flowrate.textChanged.connect(self.handle_input_rate)
        self.flowrate_slider.valueChanged.connect(self.handle_flowrate_slider)
        self.In.clicked.connect(self.handle_valve_in)
        self.Out.clicked.connect(self.handle_valve_out)
        self.aspirate_button.clicked.connect(self.handle_aspirate_button)
        self.dispense_button.clicked.connect(self.handle_dispense_button)
        self.fill_button.clicked.connect(self.handle_fill_button)
        self.empty_button.clicked.connect(self.handle_empty_button)
        self.stop_syringe_button.clicked.connect(self.handle_stop_button)

        self.flowrate_slider.valueChanged.connect(self.handle_flowrate_slider)
        self.flowrate_slider.setRange(0,100)
        self.flowrate_slider.setSingleStep(1)
        self.flowrate_slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.flowrate_slider.setValue(50)
   
    def handle_ref_button(self):
        self.label_wavelength_shift.setStyleSheet(self.in_step_label)
        self.wavelength_shift_value.setStyleSheet(self.in_step_label_with_border)
        self.label_nm_wavelength_shift.setStyleSheet(self.in_step_label)

        if self.fig_result.currentIndex() < len(self.result_list):
            self.reference_peak = self.current_fig_peak

            self.wavelength_shift  = self.reference_peak - self.current_fig_peak
            self.wavelength_shift_value.setText(str(round(self.wavelength_shift,1)))
        else:
            if self.is_run :
                self.reference_peak = round(self.peak_wavelength,1)
                self.wavelength_shift  = self.reference_peak - round(self.peak_wavelength,1)
                self.wavelength_shift_value.setText(str(round(self.wavelength_shift,1)))
            else:
                self.reference_peak = 0
                self.wavelength_shift_value.setText(str(round(self.wavelength_shift,1)))
   
            if len(self.result_list) == 0:
                if self.is_run:
                    self.current_fig_peak = self.peak_wavelength
                    self.at_label.setText(str(round(self.current_fig_peak,1)))
                    self.wavelength_shift  = self.reference_peak - round(self.current_fig_peak,1)
                    self.wavelength_shift_value.setText(str(round(self.wavelength_shift,1)))
                else:
                    self.current_fig_peak = 0
                    self.at_label.setText("-")
                    self.wavelength_shift  = self.reference_peak - round(self.current_fig_peak,1)
                    self.wavelength_shift_value.setText(str(round(self.wavelength_shift,1)))
        if self.is_run :
            self.save_fig_button.setStyleSheet(self.in_step_button)
            self.save_fig_button.setEnabled(True)

    def export_file(self):

        try:
            dt = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")  
            
            for i in range(len(self.result_list)):
                
                fileName = "result_fig_"+ str(i+1) + "_" + dt + ".txt"
                                                
                if fileName:
                    print('ไฟล์ชื่อ:', fileName)
                    # print('ประเภทไฟล์:', _)

                with open('{}'.format(fileName), mode='w', encoding='utf-8') as f:
                    f.write('start: {} nm\nstop: {} nm\nstep: {} nm\nstep delay : {} ms\npeak value: {} dbm\nAt: {:.3f} nm\n\n'.format(
                        self.start_value,
                        self.stop_value,
                        self.step_value,
                        self.delay_value,
                        self.peak_power,
                        self.peak_wavelength
                        ))

                    for i in range(len(self.wavelength)):
                        f.write(
                            '{:.3f}\t {:<6.4f}\n'.format(self.wavelength[i], self.power[i]))

        except Exception as error:
            print(error)

    def set_graph(self):
        self.ax.margins(x=0.5,y=0.5) 
        self.ax.grid()
        self.ax.tick_params(axis='x', colors=self.color_darkerpurple)
        self.ax.tick_params(axis='y', colors=self.color_darkerpurple)
        self.ax.set_ylabel('Power (dBm)' , color = self.color_green)
        self.ax.set_xlabel('Wavelength (nm)', color = self.color_green)
    def set_graph_disable(self):
        self.ax.margins(x=0.5,y=0.5) 
        self.ax.grid()
        self.ax.tick_params(axis='x', colors=self.color_gray)
        self.ax.tick_params(axis='y', colors=self.color_gray)
        self.ax.set_ylabel('Power (dBm)' , color = self.color_gray)
        self.ax.set_xlabel('Wavelength (nm)', color = self.color_gray)
    def activate_lightsource(self):
        self.label_settingLightSource.setStyleSheet(self.in_step_label)
        self.label_outputWavelength.setStyleSheet(self.in_step_label)
        self.label_outputPower.setStyleSheet(self.in_step_label)
        self.offLaser_button.setStyleSheet(self.in_step_button)
        self.offLaser_button.setEnabled(True)
        self.onLaser_button.setStyleSheet(self.in_step_button)
        self.onLaser_button.setEnabled(True)
        self.W_button.setStyleSheet(self.in_step_button)
        self.W_button.setEnabled(True)
        self.dBm_button.setStyleSheet(self.in_step_button)
        self.dBm_button.setEnabled(True)
        self.dBm_button.setStyleSheet(self.selected) # get unit before set if dbm skip ; else set dbm unit
        self.borderLightSource_style = ("#settingLightSourceField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #9D59BF;\n"
                                    "}\n")
        self.settingLightSourceField.setStyleSheet(self.borderLightSource_style)
        self.input_wavelength.setStyleSheet(self.in_step_input)
        self.input_power.setStyleSheet(self.in_step_input)
        self.input_wavelength.setReadOnly(False)
        self.input_power.setReadOnly(False)

    def activate_sweep(self):
        self.input_start.setValue(self.start_value)
        self.input_stepdelay.setValue(self.delay_value)
        self.input_stop.setValue(self.stop_value)
        self.input_step.setValue(self.step_value)
        self.label_wavelengthSweep.setStyleSheet(self.in_step_label)
        self.label_start.setStyleSheet(self.in_step_label)
        self.label_stop.setStyleSheet(self.in_step_label)
        self.label_step.setStyleSheet(self.in_step_label)
        self.label_stepDelay.setStyleSheet(self.in_step_label)
        self.label_stepDelay_2.setStyleSheet(self.in_step_label)

        self.label_ms.setStyleSheet(self.in_step_label_unit)
        self.offLaser_button.setStyleSheet(self.in_step_button)
        self.offLaser_button.setEnabled(True)
        self.onLaser_button.setStyleSheet(self.in_step_button)
        self.onLaser_button.setEnabled(True)
        self.input_start.setReadOnly(False)
        self.input_stepdelay.setReadOnly(False)
        self.input_stop.setReadOnly(False)
        self.input_step.setReadOnly(False)
        self.input_start.setStyleSheet(self.in_step_input)
        self.input_step.setStyleSheet(self.in_step_input)
        self.input_stop.setStyleSheet(self.in_step_input)
        self.input_stepdelay.setStyleSheet(self.in_step_input)
        self.borderwavelength_style = ("#wavelenghtSweepField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #9D59BF;\n"
                                    "}\n")
        self.wavelenghtSweepField.setStyleSheet(self.borderwavelength_style)
        self.timereminding_label.setStyleSheet(self.in_step_label)
        self.timereminding_value.setStyleSheet(self.in_step_label_with_border)
        self.timereminding_unit.setStyleSheet(self.in_step_label)

        #ritipong addon
        self.input_start.setMinimum(1527.0)
        self.input_start.setMaximum(1567.0)
        self.input_stop.setMinimum(1527.0)
        self.input_stop.setMaximum(1567.0)

    def connect_pump_selector(self):
        success = ("background-color: #3AB795;\n"
                   "border-radius: 10px;\n"
                   "border-style: outset;")
        failure = ("background-color: #ff6961;\n"
                    "border-radius: 10px;\n"
                    "border-style: outset;")
        self.connect_result = self.pump.connect_pump()
        # print(self.connect_result)
        self.connect_result[0] = True
        if self.connect_result[0]:
            #self.status_pump.setStyleSheet(success)
            self.pump_setting_select_button.setStyleSheet(self.pump_setting_style)

        if self.connect_result[1] :
            self.status_selector.setStyleSheet(success)
            self.pump_setting_select_button.setStyleSheet(self.pump_setting_style)
            # self.pump.ReadCTR()
            # if self.pump.LoadParaFlag == False:
            #     self.pump.LoadParameter()
            # self.pump.Operate()
            selector_th = self.pump.CheckSelector()
            if (selector_th == 1):
                self.selectorMedia.setStyleSheet(self.selected_green)
                self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector90.png"))
            elif (selector_th == 2):
                self.selector_sewage.setStyleSheet(self.selected_green)
                self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector45.png"))
            elif (selector_th == 3):
                self.selectorA.setStyleSheet(self.selected_green)
                self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector0.png"))
            elif (selector_th == 4):
                self.selectorB.setStyleSheet(self.selected_green)  
                self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector315.png"))
            elif (selector_th == 5):
                self.selectorC.setStyleSheet(self.selected_green)
                self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector270.png"))
            elif (selector_th == 6):
                self.selectorD.setStyleSheet(self.selected_green)
                self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector225.png"))
            elif (selector_th == 7):
                self.selectorE.setStyleSheet(self.selected_green)
                self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector180.png"))
            elif (selector_th == 8):
                self.selectorF.setStyleSheet(self.selected_green)
                self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector135.png"))        
    def handle_input_volume_syring(self):
        if self.input_volume_syringe.currentIndex() == 0 :
            self.volume_syringe = 0.001 * 50
            self.flowrate_maximum = 2.5
            self.flowrate_minimum = 3.125*10**-4
            self.input_flowrate.setMaximum(2.5)
            self.input_flowrate.setMinimum(3.125*10**-4)
        elif self.input_volume_syringe.currentIndex() == 1 :
            self.volume_syringe = 0.001 * 100
            self.flowrate_maximum = 5
            self.flowrate_minimum = 6.25*10**-4
            self.input_flowrate.setMaximum(5)
            self.input_flowrate.setMinimum(6.25*10**-4)
        elif self.input_volume_syringe.currentIndex() == 2 :
            self.volume_syringe = 0.001 * 250
            self.flowrate_maximum = 12.5
            self.flowrate_minimum = 1.563*10**-3
            self.input_flowrate.setMaximum(12.5)
            self.input_flowrate.setMinimum(1.563*10**-3)
        elif self.input_volume_syringe.currentIndex() == 3 :
            self.volume_syringe = 0.001 * 500
            self.flowrate_maximum = 25
            self.flowrate_minimum = 3.125*10**-3
            self.input_flowrate.setMaximum(25)
            self.input_flowrate.setMinimum(3.125*10**-3)
        elif self.input_volume_syringe.currentIndex() == 4 :
            self.volume_syringe =  1
            self.flowrate_maximum = 50
            self.flowrate_minimum = 6.25*10**-2
            self.input_flowrate.setMaximum(50) #----------------------> max speed command 'S'
            self.input_flowrate.setMinimum(6.25*10**-2) #-------------> min speed
        elif self.input_volume_syringe.currentIndex() == 5 :
            self.volume_syringe =  5
            self.flowrate_maximum = 250
            self.flowrate_minimum =3.125*10**-2
            self.input_flowrate.setMaximum(250)
            self.input_flowrate.setMinimum(3.125*10**-2)
        elif self.input_volume_syringe.currentIndex() == 6 :
            self.volume_syringe = 10
            self.flowrate_maximum = 50
            self.flowrate_minimum =6.25*10**-2
            self.input_flowrate.setMaximum(50)
            self.input_flowrate.setMinimum(6.25*10**-2)
        elif self.input_volume_syringe.currentIndex() == 7 :
            self.volume_syringe = 25
            self.flowrate_maximum = 1250
            self.flowrate_minimum =0.15625
            self.input_flowrate.setMaximum(1250)
            self.input_flowrate.setMinimum(0.15625)
        self.input_volume.setMaximum(self.volume_syringe)
        self.input_volume.setValue(self.volume_syringe)
        self.input_flowrate.setValue(1)
    def handle_input_volume(self):
        self.current_volume = self.input_volume.value()
    def handle_input_rate(self):
        self.flow_rate  = self.input_flowrate.value()
        self.flowrate_percent = int(self.flow_rate/self.flowrate_maximum*100)
        self.flowrate_slider.setValue(int(self.flow_rate/self.flowrate_maximum*100))
        # if self.flow_rate < 0:
        #     self.flowrate_slider.setValue(1)
        # else:
        #     self.flowrate_slider.setValue(int(self.flow_rate//1))
    def handle_flowrate_slider(self):
        self.flow_rate  = (self.flowrate_slider.value()/100) * self.flowrate_maximum
        self.flowrate_percent = self.flowrate_slider.value()/100
        if(self.flow_rate < self.flowrate_minimum):
            self.flow_rate = self.flowrate_minimum
        self.input_flowrate.setValue(self.flow_rate)
    def handle_initilize(self):
        self.pump.initlization()
        self.initialization_button.setStyleSheet(self.selected_green)
        self.In.setStyleSheet(self.unselected_green)
        self.Out.setStyleSheet(self.unselected_green)
    def handle_valve_in(self):
        self.pump.valveIn()
        self.initialization_button.setStyleSheet(self.unselected_green)
        self.In.setStyleSheet(self.selected_green)
        self.Out.setStyleSheet(self.unselected_green)
    def handle_valve_out(self):
        self.pump.valveOut()
        self.initialization_button.setStyleSheet(self.unselected_green)
        self.In.setStyleSheet(self.unselected_green)
        self.Out.setStyleSheet(self.selected_green)
    def handle_aspirate_button(self):

        self.flow_speed = 40 -int(self.flowrate_percent * 40)
        self.increment  = int((3000 * self.current_volume/self.volume_syringe)//10)
        print(f'speed={self.flow_speed}, position={self.increment}')

        self.pump.aspirate(self.current_volume,self.volume_syringe,self.flowrate_percent)
    def handle_dispense_button(self):
        self.pump.dispense(self.current_volume,self.volume_syringe,self.flowrate_percent)
    def handle_fill_button(self):
        self.pump.fill()
    def handle_empty_button(self):
        self.pump.empty()
    def handle_stop_button(self):
        self.pump.stop()
    def handle_operate(self):
        if(self.command != ""):
            self.pump.operate(self.command)
    def handle_emergency(self):
        self.pump.stop()

    def handle_click_selectorA(self):
        self.pump.ChA()
        self.selectorA.setStyleSheet(self.selected_green)
        self.selectorB.setStyleSheet(self.unselected_green)
        self.selectorC.setStyleSheet(self.unselected_green)
        self.selectorD.setStyleSheet(self.unselected_green)
        self.selectorE.setStyleSheet(self.unselected_green)
        self.selectorF.setStyleSheet(self.unselected_green)
        self.selector_sewage.setStyleSheet(self.unselected_green)
        self.selectorMedia.setStyleSheet(self.unselected_green)
        self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector0.png"))
    def handle_click_selectorB(self):
        self.pump.ChB()
        self.selectorA.setStyleSheet(self.unselected_green)
        self.selectorB.setStyleSheet(self.selected_green)
        self.selectorC.setStyleSheet(self.unselected_green)
        self.selectorD.setStyleSheet(self.unselected_green)
        self.selectorE.setStyleSheet(self.unselected_green)
        self.selectorF.setStyleSheet(self.unselected_green)
        self.selector_sewage.setStyleSheet(self.unselected_green)
        self.selectorMedia.setStyleSheet(self.unselected_green)
        self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector315.png"))
    def handle_click_selectorC(self):
        self.pump.ChC()
        self.selectorA.setStyleSheet(self.unselected_green)
        self.selectorB.setStyleSheet(self.unselected_green)
        self.selectorC.setStyleSheet(self.selected_green)
        self.selectorD.setStyleSheet(self.unselected_green)
        self.selectorE.setStyleSheet(self.unselected_green)
        self.selectorF.setStyleSheet(self.unselected_green)
        self.selector_sewage.setStyleSheet(self.unselected_green)
        self.selectorMedia.setStyleSheet(self.unselected_green)
        self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector270.png"))
    def handle_click_selectorD(self):
        self.pump.ChD()
        self.selectorA.setStyleSheet(self.unselected_green)
        self.selectorB.setStyleSheet(self.unselected_green)
        self.selectorC.setStyleSheet(self.unselected_green)
        self.selectorD.setStyleSheet(self.selected_green)
        self.selectorE.setStyleSheet(self.unselected_green)
        self.selectorF.setStyleSheet(self.unselected_green)
        self.selector_sewage.setStyleSheet(self.unselected_green)
        self.selectorMedia.setStyleSheet(self.unselected_green)
        self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector225.png"))
    def handle_click_selectorE(self):
        self.pump.ChE()
        self.selectorA.setStyleSheet(self.unselected_green)
        self.selectorB.setStyleSheet(self.unselected_green)
        self.selectorC.setStyleSheet(self.unselected_green)
        self.selectorD.setStyleSheet(self.unselected_green)
        self.selectorE.setStyleSheet(self.selected_green)
        self.selectorF.setStyleSheet(self.unselected_green)
        self.selector_sewage.setStyleSheet(self.unselected_green)
        self.selectorMedia.setStyleSheet(self.unselected_green)
        self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector180.png"))
    def handle_click_selectorF(self):
        self.pump.ChF()
        self.selectorA.setStyleSheet(self.unselected_green)
        self.selectorB.setStyleSheet(self.unselected_green)
        self.selectorC.setStyleSheet(self.unselected_green)
        self.selectorD.setStyleSheet(self.unselected_green)
        self.selectorE.setStyleSheet(self.unselected_green)
        self.selectorF.setStyleSheet(self.selected_green)
        self.selector_sewage.setStyleSheet(self.unselected_green)
        self.selectorMedia.setStyleSheet(self.unselected_green)
        self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector135.png"))
    def handle_click_selectorMedia(self):
        self.pump.ChInlet()
        self.selectorA.setStyleSheet(self.unselected_green)
        self.selectorB.setStyleSheet(self.unselected_green)
        self.selectorC.setStyleSheet(self.unselected_green)
        self.selectorD.setStyleSheet(self.unselected_green)
        self.selectorE.setStyleSheet(self.unselected_green)
        self.selectorF.setStyleSheet(self.unselected_green)
        self.selector_sewage.setStyleSheet(self.unselected_green)
        self.selectorMedia.setStyleSheet(self.selected_green)
        self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector90.png"))
    def handle_click_selectorSewage(self):
        self.pump.ChOutlet()
        self.selectorA.setStyleSheet(self.unselected_green)
        self.selectorB.setStyleSheet(self.unselected_green)
        self.selectorC.setStyleSheet(self.unselected_green)
        self.selectorD.setStyleSheet(self.unselected_green)
        self.selectorE.setStyleSheet(self.unselected_green)
        self.selectorF.setStyleSheet(self.unselected_green)
        self.selector_sewage.setStyleSheet(self.selected_green)
        self.selectorMedia.setStyleSheet(self.unselected_green)
        self.selector_img.setPixmap(QtGui.QPixmap(":/selector/selector/selector45.png"))
    def handle_click_pump_setting(self):
        self.setting_device_field.setStyleSheet("#setting_device_field{\n"
"border-width: 5px; border-style: solid; border-color: white #3AB795 #3AB795 white;\n"
"background-color : #FFFFFF;\n"
"}\n")
        self.lightsource_pump.setCurrentIndex(1)
        if self.connect_result[0]:
            self.label_syringe_setup.setStyleSheet(self.in_step_label_green)
            self.label_volume.setStyleSheet(self.in_step_label_green)
            self.label_mL.setStyleSheet(self.in_step_label)
            self.input_volume.setStyleSheet(self.in_step_input_pump)
            self.input_volume.setReadOnly(False)
            self.aspirate_button.setStyleSheet(self.in_step_button)
            self.aspirate_button.setEnabled(True)
            self.dispense_button.setStyleSheet(self.in_step_button)
            self.dispense_button.setEnabled(True)
            self.label_volume_syringe.setStyleSheet(self.in_step_label_green)
            self.input_volume_syringe.setStyleSheet(self.in_step_input_pump)
            self.input_volume.setReadOnly(False)
            self.initialization_button.setStyleSheet(self.in_step_button_green)
            self.initialization_button.setEnabled(True)
            self.label_flowrate.setStyleSheet(self.in_step_label_green)
            self.input_flowrate.setStyleSheet(self.in_step_input_pump)
            self.input_flowrate.setReadOnly(False)
            self.label_uls.setStyleSheet(self.in_step_label)
            self.fill_button.setStyleSheet(self.in_step_button_green)
            self.fill_button.setEnabled(True)
            self.empty_button.setStyleSheet(self.in_step_button_green)
            self.empty_button.setEnabled(True)
            self.In.setStyleSheet(self.in_step_button_green)
            self.In.setEnabled(True)
            self.Out.setStyleSheet(self.in_step_button_green)
            self.Out.setEnabled(True)
            self.stop_syringe_button.setStyleSheet(self.in_step_button_red)
            self.stop_syringe_button.setEnabled(True)
            self.syringe_setup_field.setStyleSheet("#syringe_setup_field{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #3AB795;\n"
                                    "}\n")
        if self.connect_result[1]:
            self.label_selectorcontrol.setStyleSheet(self.in_step_label_green)
            self.selectorA.setStyleSheet(self.in_step_button_green)
            self.selectorA.setEnabled(True)
            self.selectorB.setStyleSheet(self.in_step_button_green)
            self.selectorB.setEnabled(True)
            self.selectorC.setStyleSheet(self.in_step_button_green)
            self.selectorC.setEnabled(True)
            self.selectorD.setStyleSheet(self.in_step_button_green)
            self.selectorD.setEnabled(True)
            self.selectorE.setStyleSheet(self.in_step_button_green)
            self.selectorE.setEnabled(True)
            self.selectorF.setStyleSheet(self.in_step_button_green)
            self.selectorF.setEnabled(True)
            self.selectorMedia.setStyleSheet(self.in_step_button_green)
            self.selectorMedia.setEnabled(True)
            self.selector_sewage.setStyleSheet(self.in_step_button_green)
            self.selector_sewage.setEnabled(True)
            self.selector_control_field.setStyleSheet("#selector_control_field{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #3AB795;\n"
                                    "}\n")
        if self.connect_result[0] and self.connect_result[1]:
            self.emergency_button.setStyleSheet(self.not_in_step_button)
            self.command_script_field.setStyleSheet("#command_script_field{\n"
                                            "border-style: outset;\n"
                                            "border-width: 2px;\n"
                                            "border-radius: 10px;\n"
                                            "border-color: #3AB795;\n"
                                            "}\n"
                                            )

    def connect_instrument(self):
        success = ("background-color: #3AB795;\n"
                   "border-radius: 10px;\n"
                   "border-style: outset;")
        failure = ("background-color: #ff6961;\n"
                   "border-radius: 10px;\n"
                   "border-style: outset;")
        
        #ritipong addon 
        #connect OSA APP Demo
        self.exit_code = subprocess.call("{}/RunOSA.bat".format(os.getcwd()))

        # try:
        #     # connect broadband laser source
        #     self.startup_tunable_laser()
        #     # self.startup_tunable_laser(GPIB='COM17')
        #     # self.startup_tunable_laser(GPIB='GPIB2::15::INSTR')

        #     # connect power meter
        #     # self.startup_optical_multimeter() #ThorLab
        #     # self.startup_optical_multimeter(GPIB='GPIB0::19::INSTR')
        #     # self.startup_optical_multimeter(GPIB='GPIB2::4s::INSTR')


        #     self.status_light.setStyleSheet(success)
        #     self.status_power.setStyleSheet(success)
        #     # self.can_continue = True
        #     # self.system_value_set()
        #     self.status_light.setStyleSheet(success)
        #     self.status_power.setStyleSheet(success)
        #     self.is_connected = True
        #     self.lightsource_setting_select_button.setStyleSheet(self.in_step_button)
        #     self.lightsource_setting_select_button.setEnabled(True)
        # except Exception as error:
        #     print(error)

        

    def handle_clicked_lightsource_setting(self):
        self.setting_device_field.setStyleSheet("#setting_device_field{\n"
"border-width: 5px; border-style: solid;  border-color: #9D59BF white white #9D59BF;\n"
"background-color : #FFFFFF;\n"
"}\n")
        self.lightsource_pump.setCurrentIndex(0)
        self.result_figure_stack.setCurrentIndex(0)
         # setting style to setting parameter field
        self.label_settingParameter.setStyleSheet(self.in_step_label)
        self.defaultParameter_button.setStyleSheet(self.in_step_button)
        self.defaultParameter_button.setEnabled(True)
        self.manualParameter_button.setStyleSheet(self.in_step_button)
        self.manualParameter_button.setEnabled(True)
        self.borderParameter_style = ("#setParameterField{\n"
                                "border-style: outset;\n"
                                "border-width: 2px;\n"
                               "border-radius: 10px;\n"
                                "border-color: #9D59BF;\n"
                                "}\n")
        self.setParameterField.setStyleSheet(self.borderParameter_style)

    ## setting parameter
    def default_setting_param(self):
        self.set_laser_off()
        # self.input_wavelength.setValue(self.output_value)
        # self.input_power.setValue(self.power_value)
        # try default value
        self.output_value = 1550.0
        self.power_value = 10.0
        self.input_wavelength.setValue(self.output_value)
        self.W_to_Bm()
        self.input_power.setValue(self.power_value)
        
        
        
        self.start_value = 1540.0
        self.stop_value = 1560.0
        self.step_value = 0.1
        self.delay_value = 1000.0
        self.input_start.setValue(self.start_value)
        self.input_stepdelay.setValue(self.delay_value)
        self.input_stop.setValue(self.stop_value)
        self.input_step.setValue(self.step_value)
        self.activate_lightsource() #enable groupbox of setting light source
    def manual_setting_param(self):
        #ritipong addon
        self.start_value = 1540.0
        self.stop_value = 1560.0
        self.step_value = 0.1
        self.delay_value = 1000.0

        self.set_laser_off()
        # try default value
        self.input_wavelength.setValue(self.output_value)
        self.W_to_Bm()
        self.input_power.setValue(self.power_value)
        self.input_start.setValue(self.start_value)
        self.input_stepdelay.setValue(self.delay_value)
        self.input_stop.setValue(self.stop_value)
        self.input_step.setValue(self.step_value)
        
        self.activate_lightsource() #enable groupbox of setting light source
    ## setting channel
    def setting_channel(self):
        pass
    ###TODO read manual to select channel
    ## laser
    
    def set_laser_on(self):
        # ritipong addon
        self.activate_sweep()
        self.onLaser_button.setStyleSheet(self.selected)

        try:
            self.turn_on()
            ## Uncomment when test instrusment
            # laser_on = threading.Thread(target=self.turn_on())
            # laser_on.start()
            # laser_on.join()
            
            if self.is_laser_on == False:
                self.offLaser_button.setStyleSheet(self.unselected)
            self.is_laser_on = True
            self.activate_sweep()
            self.onLaser_button.setStyleSheet(self.selected)
            # self.Laser_on.setChecked(True)

        except Exception as error:
            print(error)
    def set_laser_off(self):
        try:
            self.turn_off()
            # laser_off = threading.Thread(target=self.turn_off())
            # laser_off.start()
            # laser_off.join()
            self.offLaser_button.setStyleSheet(self.selected)
            
            if self.is_laser_on == True:
                self.onLaser_button.setStyleSheet(self.unselected)
            self.is_laser_on = False

        except Exception as error:
            print(error)
    def handle_output_wavelength_input(self):
        try:
            self.output_value = self.input_wavelength.value()
            self.set_wavelength_nm(self.output_value)
            print("wavelegnth set: " + str(self.output_value))
        except Exception as error:
            # print("wavelegnth set")
            print(error)
    def handle_output_power_input(self):
        try:
        
            self.power_value = self.input_power.value()
            self.set_power(self.power_value)
            print("power set: " + str(self.power_value))
        except Exception as error:
            print(error )
    def handle_start_input(self):
        try:
            self.start_value = self.input_start.value()
            print(self.start_value)
        except Exception as error:
            print(error)
    def handle_stop_input(self):
        try:
            self.stop_value = self.input_stop.value()
            print(self.stop_value)
        except Exception as error:
            print(error)
    def handle_step_input(self):
        try:
            self.step_value = self.input_step.value()
            print(self.step_value)
        except Exception as error:
            print(error)
    def handle_step_delay_input(self):
        try:
            self.delay_value = self.input_stepdelay.value()
            print(self.delay_value)
        except Exception as error:
            print(error)
    def W_to_Bm(self):
            self.set_unit('dBm')
            if self.is_W:
                if self.is_connected == True:
                    self.is_W = False
                    self.dBm_button.setStyleSheet(self.selected)
                    self.W_button.setStyleSheet(self.unselected)
                    
                    self.set_power(self.power_value)
                    print(self.is_W )
    def dBm_to_W(self):
        self.set_unit('mW')
        # self.set_unit('mw')
        if self.is_W == False:
            if self.is_connected == True:
                self.dBm_button.setStyleSheet(self.unselected)
                self.W_button.setStyleSheet(self.selected)
                self.is_W = True
                
                self.set_power(self.power_value)
                print(self.is_W )
        
    def laser_start(self):
        self.laser_busy()
    def laser_stop(self):
        self.laser_idle()
        try:
            if ~self.is_laser_on :
                self.set_laser_on()
            self.data.clear()
            self.process_data.clear()
            self.final_data.clear()
            
            # self.measure_plot_list[n][0].clear()
            # self.measure_plot_list[n][1].clear()
        except Exception as error:
            print(error)
    def set_peak(self,min_wavelength,min_power):
        self.peak_power =min_power
        self.peak_wavelength =  min_wavelength
        
    def set_value_function(self):
        try:
            self.set_wavelength_nm(self.output_value)
            if self.is_W :
                self.set_unit('mW')
                # self.set_unit(' \u00B5mW')
            else:
                # self.set_unit(' dBm')
                self.set_unit('dBm')
            self.set_power(self.power_value)

        except Exception as error:
            print(error)
    def sweep_start(self):
        self.progress = 0
        try:

            self.set_result_field_able()
            self.ax.cla()
            self.set_laser_on()
            self.set_value_function()
            self.data.clear()
            self.process_data.clear()
            self.final_data.clear()
            self.wavelength.clear()
            self.laser_busy()
            self.set_graph()
            sweep = threading.Thread(target=self.wavelength_sweep, args=(self.start_value,
                                                                         self.stop_value,
                                                                         self.step_value,
                                                                         self.delay_value))

            sweep.start()
            

            
        except Exception as error:
            print(error)
    
    def wavelength_sweep(self,
                         start_wavelength,
                         stop_wavelength,
                         step_wavelength,
                         step_delay
                         ):
        try:
            LaserBB2Filter.stop_click = False
            # LaserAgilent8168D.stop_click = False
            self.set_result_field_able()
            
            for wavelength in np.arange(start_wavelength, stop_wavelength + step_wavelength, step_wavelength):
                if LaserBB2Filter.stop_click:
                # if LaserAgilent8168D.stop_click:
                    break
                self.set_wavelength_nm(wavelength)
                # self.tunable_laser.write(':WAVE {}nm'.format(str(wavelength)))
                if wavelength == start_wavelength:
                    time.sleep(1)
                time.sleep(step_delay / 1000)
                self.wavelength.append(wavelength)
                self.update_graph()
                self.set_peak(self.wavelength[self.power.index(min(self.power))],min(self.power))
                # self.progress = int(round((wavelength - start_wavelength + step_wavelength) * 100 /
                #              (stop_wavelength + step_wavelength - start_wavelength)))
                self.progress = int(((self.stop_value - wavelength)/ self.step_value) * self.delay_value / 1000)
                self.timereminding_value.setText(str(self.progress))
                
                self.wavelength_shift  = self.reference_peak - round(self.peak_wavelength,1)
                # print(self.wavelength_shift)
                self.wavelength_shift_value.setText(str(round(self.wavelength_shift,1))) 
                self.back_fig.setEnabled(False)
                self.back_fig.setStyleSheet(self.not_in_step_button)
            self.laser_finish()
            self.is_finish = True
            self.is_saved = False
            if len(self.result_list) > 0:
                self.back_fig.setEnabled(True)
                self.back_fig.setStyleSheet(self.in_step_button)

            if(self.fig_result.currentIndex() == len(self.result_list)):
                self.save_fig_button.setStyleSheet(self.in_step_button)
                self.save_fig_button.setEnabled(True)
            self.is_run = True
            
        except Exception as error:
            print(error)
    def update_graph(self):
        try:
            print(self.wavelength)
            print(self.power)
            
            # self.set_graph()
            self.ax.plot(self.wavelength,self.power, marker='o', color=self.color_purple , markerfacecolor=self.color_darkerpurple) 
            self.canvas.draw()
        except Exception as error:
            print(error)
    def sweep_stop(self):
        try:
            LaserBB2Filter.stop_click = True
            self.laser_idle()
        except Exception as error:
            print(error)
    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(MyProgram ,'Exit', 
                        quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.pump.close_pump()
            event.accept()
        else:
            event.ignore()

    # def showdialog(self):
    #     msg = QMessageBox()
    #     msg.setIcon(QMessageBox.Information)

    #     msg.setText("This is a message box")
    #     msg.setInformativeText("This is additional information")
    #     # msg.setWindowTitle("MessageBox demo")
    #     msg.setDetailedText("The details are as follows:")
    #     msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    #     msg.buttonClicked.connect(self.msgbtn)
	
    #     retval = msg.exec_()
    #     print ("value of pressed message box button:", retval)
    # def msgbtn(self,i):
    #     print("Button pressed is:",i.text())
class SplashScreen(QtWidgets.QMainWindow):
    def __init__(self):
        self.counter = 0
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        ## UI ==> INTERFACE CODES
        ########################################################################

        ## REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        ## DROP SHADOW EFFECT
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        self.ui.dropshadowframe.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(10)

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):

        

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(self.counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if self.counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            
            window = biosensor_function()
            
            MyProgram.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        
        self.counter += 1
        
if __name__ == "__main__":
    # if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    #     QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    
    app = QtWidgets.QApplication(sys.argv)
    
    app.setApplicationName("Biomed App")
    
    MyProgram = QtWidgets.QMainWindow()
    splash = SplashScreen()
    
    sys.exit(app.exec_())
