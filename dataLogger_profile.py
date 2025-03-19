# This Python file uses the following encoding: utf-8
import bz2
import configparser
import datetime
import fnmatch
import glob
import os
import re
import struct
import sys
import time
from time import sleep
from enum import Enum
from sys import platform

import serial
import serial.tools.list_ports


import serial
from PySide6.QtCore import QThread, Signal

import select

from threading import Thread
from multiprocessing import Queue
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import (QCoreApplication, Qt)
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QApplication, QWidget, QMessageBox)
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QTabBar

from adhat import ADS1263

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

os.environ["QT_LOGGING_RULES"] = "qt.accessibility.atspi.warning=false"
from ui_form import Ui_DataLogger_Profile


class ConnectionState(Enum):
    BLACK = 1
    RED = 2
    YELLOW = 3
    GREEN = 4
    BLUE = 5


class ProfileViewState(Enum):
    PROFILE_VIEW_MAG = 0
    PROFILE_VIEW_ORTHO = 1
    PROFILE_VIEW_GPS = 2
    PROFILE_VIEW_RA4500 = 3
    PROFILE_VIEW_LASER = 4
    PROFILE_VIEW_ADHAT = 5


class NoMouseTabBar(QTabBar):
    def mousePressEvent(self, event):
        # Ignore the mouse press event to disable tab switching by mouse
        event.ignore()


class ChartWidget(QWidget):
    def __init__(self, color):
        super().__init__()
        # Create Ortho QChart and QChartView

        self.chart_Obj = QChart()
        self.chart_Obj_view = QChartView(self.chart_Obj)
        self.chart_Obj_view.setRenderHint(QPainter.Antialiasing)

        self.chart_Obj.legend().hide()

        # Create QLineSeries
        self.series_Obj = QLineSeries()

        self.series_Obj.setColor(color)

        # Add the series to the chart
        self.chart_Obj.addSeries(self.series_Obj)

        # Create axes
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()

        # Set range for axes
        self.axis_x.setTickCount(10)  # Display a tick every 5 seconds for 1 minute

        # Add axes to the chart
        self.chart_Obj.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart_Obj.addAxis(self.axis_y, Qt.AlignLeft)

        # Attach axes to the series
        self.series_Obj.attachAxis(self.axis_x)
        self.series_Obj.attachAxis(self.axis_y)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_Obj_view)
        self.setLayout(layout)


style_Button_Off = """
             QPushButton {
                 background-color: black;
                 border: none;
                 color: white;
                 font: 700 16pt \"Segoe UI\";
                 border-image: url(buttons_grey.png);
               /*  transform: rotate(-90deg); */ /* Rotate the button vertically */
             }
             QPushButton:hover {
                 background-color: #333;
             }
             QPushButton:pressed {
                border-image: url(buttons_grey_p.png);
             }
        """

style_Button_On = """
             QPushButton {
                 background-color: black;
                 border: none;
    color: white;
                 font: 700 16pt \"Segoe UI\";
                 border-image: url(buttons_grey_p.png);
               /*  transform: rotate(-90deg); */ /* Rotate the button vertically */
             }
             QPushButton:hover {
                 background-color: #333;
             }
             QPushButton:pressed {
                border-image: url(buttons_grey_p.png);
             }
        """
#####  GLOBAL VARIABLES ##########
file_write_delay_sec = 10

profile_viewer_time = 300

instrument_timestamp_enable = False

Logdirectory = ""

gga_timestamp = "0"

qtfm_semaphore = False

utc_hour_diff = 0

gps_date = "0"

gga_utc_time = "0"
gps_day = "0"
gps_month = "0"
gps_year = "0"
gps_hour = "0"
gps_minute = "0"
gps_second = "0"
gps_microsecond = "0"

gps_antenna_on = True

f_gpsTimeUnSynch = False

last_gga_time = 0

synch_sysdate = False

READ_ALL_AVAILABLE = -1

last_qtfm_timestamp = 0

current_qtfm_timestamp = 0

last_adhat_timestamp = 0

current_adhat_timestamp = 0

adhat_rec_per_100ms = 5

Raspberry_PI = False

Logdirectory = ""

if platform == "linux" or platform == "linux2":
    Raspberry_PI = True
    config_PI_file = "DefaultConfiguration_PI.txt"

    Logdirectory = "//home//nsg//Desktop/NSG//"

elif platform == "win32":
    Raspberry_PI = False
    config_PI_file = "DefaultConfiguration_PI.txt"

if Raspberry_PI:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library

    Logdirectory = ""

dataCounter = 0
lastLaserHeight = "999999"

# Global Data Structure
# hashmap_GPS = {}
alist_GPS = []
alist_KANA8 = []
alist_KMAG4 = []
alist_KMAG4_BIN = []
alist_LASER = []
alist_RA4500 = []
alist_ADHAT = []
alist_QTFM = []
alist_QTFM_BIN = []

bz_buffer = []

default_QTFM = ",,"

isEnable_GPS = False
isEnable_KMAG4 = False
isEnable_KANA8 = False
isEnable_LASER = False
isEnable_QTFM = False
isEnable_RA4500 = False
isEnable_ADHAT = False

dataOutput = None

dataLogHeaderKana8 = ":kmag4:internal_counter,:kmag4:utc_time,:kmag4:utc_1pps_indicator,:kmag4:mag_a,:kmag4:mag_b,:kmag4:mag_c,:kmag4:mag_d,:kmag4:fx,:kmag4:fy,:kmag4:fz,:kmag4:radar_altimeter_m,:kmag4:vlf_line_tot,:kmag4:vlf_line_quad,:kmag4:vlf_ortho_tot,:kmag4:vlf_ortho_quad,"
dataLogHeaderKMAG4 = ":kmag4:internal_counter,:kmag4:utc_time,:kmag4:utc_1pps_indicator,:kmag4:mag_a,:kmag4:mag_b,:kmag4:mag_c,:kmag4:mag_d,"
dataLogHeaderGPS = ":gga:utctime,:gga:sats_in_use,:gga:hdop,:gga:msl_altitude,:gga:position_fix_indicator,:gga:latitude,:gga:ns_indicator,:gga:longitude,:gga:ew_indicator,"
dataLogHeaderLaser = "laser:altimeter_m,"
dataLogHeaderRA4500 = "ra4500:radar_altimeter_m,ra4500:radar_status,"
dataLogHeaderADHAT = "adhat:ch1,adhat:ch2,adhat:ch3,adhat:ch4,adhat:ch5,"
dataLogQuspinHeaderV1 = "qtfm:utctime,qtfm:ch0,qtfm:ch1,"
dataLogQuspinHeaderV2 = "qtfm:utctime,qtfm:q_fid,qtfm:q_msclock,qtfm:q_datacount,qtfm:q_mag_valid,qtfm:q_mag,qtfm:q_mag_sens,qtfm:qf_valid,qtfm:qf_x,qtfm:qf_y,qtfm:qf_z,qtfm:qf_sens,"
sDataLogHeaderGPS = ""
sDataLogHeaderQTFM = ""
sDataLogHeaderKana8 = ""
sDataLogHeaderLaser = ""
sDataLogHeaderRA4500 = ""
sDataLogHeaderADHAT = ""

quspinVersion = "1"
qtfm_q_fid_counter = 0
counter_QTFM = 0
qtfm_NoneDataFlag = False
quspin_speed_detect_flag = False
quspin_speed_detect_counter = 0
quspin_speed_last_sq_num = 0
quspin_speed_detect_value = 4
last_sq_number = 0
last_bz2_utc_time = 0
last_bz2_file_time = 0

last_KMAG4_utc_time = ""
last_KMAG4_data = ""

# debug_Timer_1 = 0
# debug_Timer_2 = 0

quspin_Mode = ""
mag_counter = 0
last_msclock = 0
last_datacount = 0
valid_mag_filter = 0
shutdown_process = False

counter_ADHAT = 0

last_valid_gps_value = 0 #Eugene

# Eugene
f_trigger = False
last_trigger_time = 0
trigger_start_time = 0


######################################################
## Class instrument
######################################################
class DataOutput:
    def __init__(self):
        self.name_kmag4_channel = ""
        self.newFile = 0
        self.enabled = False
        self.file_change = False
        self.file_name = ""
        self.file_size = 0
        self.file_ext = ""


######################################################
## Class instrument
######################################################
class Instrument:
    def __init__(self):
        self.name_instrument = 0
        self.newFile = 0
        self.enabled = False
        self.connected = False
        self.label = ""
        self.parser = 0
        self.inst_port = 0
        self.inst_baudrate = 0
        self.serial = None
        self.speed_Hz = 0
        self.rawdata_log_enabled = False
        self.packetheader = ""
        self.gpio_pin = 0
        self.timer = 0
        self.buffer = []
        self.start_timer = 0


class Instrument_HighSpeed_Serial(QThread):
    data_ready = Signal(str)

    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, parent=None, profile=any):
        super().__init__(parent)
        self.running = True
        self.profile = profile
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.port_reset = False

    def run(self):

        if platform == "linux" or platform == "linux2":
            self.serial_connection = serial.Serial(self.port, self.baudrate)
        else:
            self.serial_connection = serial.Serial(self.port.name, self.baudrate)

        self.serial_connection.reset_input_buffer()

        while self.running:
            value = self.read_serial()
            if value is not None:
                self.data_ready.emit(value)
                if self.port_reset == True:
                    self.port_reset = False
                    self.serial_connection.reset_input_buffer()
                    #print("Quspin input buffer reset\n")
                    #self.serial_connection.reset_output_buffer()

    def read_serial(self):
        """Non-blocking serial read using select() to avoid delays."""
        if platform == "linux" or platform == "linux2":
            ready, _, _ = select.select([self.serial_connection], [], [], 0.01)
        else:
            ready = True

        if ready:
            try:
                return self.serial_connection.readline().decode('utf-8').strip()
            except UnicodeDecodeError:
                return None
        return None

    def stop(self):
        self.running = False
        self.wait()
        print(f"Stop process: {self.port}")
        if self.serial_connection is not None:
            self.serial_connection.close()

class Instrument_LowSpeed_Serial(QThread):
    data_ready = Signal(str)

    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, parent=None, profile=any):
        super().__init__(parent)
        self.profile = profile
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.port_reset = False
        self.read_time = 50  # 10 Hz (1000ms / 10 = 100ms)


        if platform == "linux" or platform == "linux2":
            self.serial_connection = serial.Serial(self.port, self.baudrate)
        else:
            self.serial_connection = serial.Serial(self.port.name, self.baudrate)

        self.serial_connection.reset_input_buffer()


        self.read_data_timer = QTimer()
        self.read_data_timer.timeout.connect(self.read_data)
        self.read_data_timer.start(self.read_time)  # 50 Hz (1000ms / 50 = 20ms)

    def read_data(self):
            value = self.read_serial()
            if value is not None:
                self.data_ready.emit(value)
                if self.port_reset == True:
                    self.port_reset = False
                    self.serial_connection.reset_input_buffer()


    def read_serial(self):
        if self.serial_connection.in_waiting > 0:
            try:
                line = self.serial_connection.readline().decode('utf-8').strip()
                #print("read_serial: " + line)
            except UnicodeDecodeError:
                line = None
            return line
        return None

    def stop(self):
        self.read_data_timer.stop()
        print(f"Stop process:  {self.port}")
        if self.serial_connection is not None:
            self.serial_connection.close()


class Instrument_ADHAT(QThread):
    data_ready = Signal(list)

    def __init__(self, profile):
        super().__init__()
        self.running = True
        self.ADC = None
        self.profile = profile
        self.channel_active = []
        self.ch_multiplier = []
        self.ch_divider = []
        self.ch_offset = []
        self.start_timer = time.time()

    def run(self):
        global file_write_delay_sec
        REF = 5.08  # Modify according to actual voltage
        # external AVDD and AVSS(Default), or internal 2.5V
        if platform == "linux" or platform == "linux2":
            try:
                self.ADC = ADS1263.ADS1263()

                # The faster the rate, the worse the stability
                # and the need to choose a suitable digital filter(REG_MODE1)
                if (self.ADC.ADS1263_init_ADC1('ADS1263_50SPS') == -1):
                    print("ADHAT is not found")
                    self.running = False
                    return

                self.ADC.ADS1263_SetMode(1)  # 0 is singleChannel, 1 is diffChannel
                # Create channel list based on active channels
                channelList = [i for i in range(5) if self.channel_active[i]]

                #period = 1.0 / 50  # 50Hz -> 20ms per iteration


                while self.running:
                    #start_time = time.perf_counter()  # Get time at loop start
                    ADC_Value = self.ADC.ADS1263_GetAll(channelList)  # Get ADC values for active channels
                    #print(f"ADC_Value: {ADC_Value}, Time: { int(time.time() * 1000)} ms")


                    values = [0] * 5  # Initialize the array with zero values for all channels

                    # Process each active channel
                    for idx, ch in enumerate(channelList):
                        if self.channel_active[ch]:  # Check if the channel is active
                            values[ch] = ADC_Value[idx] * self.ch_multiplier[ch] / self.ch_divider[ch] + self.ch_offset[ch]
                        else:
                            values[ch] = 0  # Set to 0 if channel is not active

                    self.data_ready.emit(values)

                    # Adjust sleep to maintain 50Hz rate
                    #elapsed_time = time.perf_counter() - start_time
                    #sleep_time = max(0, period - elapsed_time)  # Ensure we don’t sleep negative time
                    #sleep(sleep_time)
                    sleep(0.01)

            except IOError as e:
                print(e)

    def stop(self):
        self.running = False
        self.wait()
        print("Stop ADHAT process")


class Instrument_Serial_Bin(QThread):
    data_ready = Signal(bytes)

    def __init__(self, port='/dev/ttyUSB0', baudrate=57600, parent=None, profile=any):
        super().__init__(parent)
        self.running = True
        self.profile = profile
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.buffer = bytearray()  # Buffer to store incomplete messages

    def run(self):
        # Open the serial connection depending on the platform
        if platform == "linux" or platform == "linux2":
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
        else:
            self.serial_connection = serial.Serial(self.port.name, self.baudrate, timeout=1)

        while self.running:
            value = self.read_serial_bin()
            if value is not None:
                self.data_ready.emit(value)
                # if self.profile.start_timer_Profile and self.profile.ProfileView == ProfileViewState.PROFILE_VIEW_ADHAT:
                #     sleep(0.1)

    def read_serial_bin(self):
        start_sequence = b'\x10\xdf\x03'  # Start sequence
        end_sequence = b'\x10\x03'  # End sequence
        expected_message_length = 9

        # Read incoming bytes
        while self.serial_connection.in_waiting > 0:
            byte = self.serial_connection.read(1)
            self.buffer += byte

            # Check if buffer contains a complete message
            if len(self.buffer) >= expected_message_length:
                start_index = self.buffer.find(start_sequence)
                if start_index != -1:
                    # Check if we have the end sequence as well
                    end_index = self.buffer.find(end_sequence, start_index + 3)
                    if end_index != -1:
                        # Verify that the total length of the message is exactly 9 bytes
                        message_length = end_index - start_index + len(end_sequence)
                        if message_length == expected_message_length:
                            # We found a complete valid message of 9 bytes
                            message = self.buffer[start_index:end_index + len(end_sequence)]
                            self.buffer = self.buffer[end_index + len(end_sequence):]  # Remove the processed message
                            return message
                        else:
                            # Skip message if it's not 9 bytes long
                            self.buffer = self.buffer[end_index + len(end_sequence):]  # Skip the invalid message

        return None

    def write_serial(self, data):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write(data)

    def stop(self):
        self.running = False
        self.wait()
        if self.serial_connection is not None:
            self.serial_connection.close()


class DataLogger_Profile(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.series_Laser = None
        self.series_Mag = None
        self.series_RA4500 = None
        self.series_ADHAT = None

        self.start_timer = None

        #self.program_msg_q_timer = None
        self.dataLogger_proc = None
        self.dataOutput_timer = None

        self.quspin_chart_timer = None
        self.gps_chart_timer = None
        self.ra4500_chart_timer = None
        self.adhat_chart_timer = None
        self.laser_chart_timer = None

        self.CurrentDataRate = 16

        self.quspin_connect_time = 0
        self.gps_connect_time = 0
        self.laser_connect_time = 0
        self.ra4500_connect_time = 0
        self.adhat_connect_time = 0

        self.message_timer = 0
        self.message_count = 0

        self.profile_viewer_auto_off_timer = None

        self.profile_viewer_pause_off_timer = None
        self.profile_viewer_pause_on_timer = None

        self.start_timer_Profile = False
        self.program_DataOutput = None
        self.program_msg_q = None
        self.instruments_config_array = {}

        self.data_rates_index = None
        self.update_display_time_mag = None
        self.display_time_mag_wait = None
        self.display_time_mag_pause = None

        self.update_display_time_sensivity = None
        self.update_display_time_ortho_X = None
        self.update_display_time_ortho_Y = None
        self.update_display_time_ortho_Z = None

        self.update_display_time_gps_lat = None
        self.update_display_time_gps_lon = None
        self.update_display_time_gps_alt = None

        self.update_display_time_laser = None
        self.update_display_time_ra4500 = None
        self.update_display_time_adhat = None

        self.inst_Process = {
            "GPS": self.gps_process,
            "KANA8": self.KANA8_process,
            "KMAG4": self.KMAG4_process,
            "LASER": self.laser_process,
            "RA4500": self.RA4500_process,
            "ADHAT": self.ADHAT_process,
            "QTFM_V1": self.qtfm_process,
            "QTFM_V2": self.qtfm_process
        }

        self.inst_ProcessPriority = {
            "GPS": QThread.HighPriority ,
            "KANA8": QThread.NormalPriority ,
            "KMAG4": QThread.NormalPriority ,
            "LASER": QThread.NormalPriority ,
            "RA4500": QThread.NormalPriority ,
            "ADHAT": QThread.HighestPriority,
            "QTFM_V1": QThread.TimeCriticalPriority,
            "QTFM_V2": QThread.TimeCriticalPriority
        }

        self.last_valid_mag_value = 0
        self.last_valid_ortho_X = 0
        self.last_valid_ortho_Y = 0
        self.last_valid_ortho_Z = 0

        self.debug_counter = 0

        self.ra4500_msg_counter = 0
        self.adhat_msg_counter = 0

        self.max_records = 2500
        self.record_separator = '\n'  # Define how records are separated

        self.profile_scale_index = None
        self.vector_mode_index = None
        self.ui = Ui_DataLogger_Profile()
        self.ui.setupUi(self)
        self.currentSerialPort = ""
        self.connection_state = ConnectionState.YELLOW
        self.serialPortList = []
        self.serial_interval = 4
        self.chart_factor = 3
        self.serialPortConfig()

        self.alist_QTFM = []

        self.DataRecordsAmount = 24
        self.DataRecordsCounter = 0
        self.ProfileView = ProfileViewState.PROFILE_VIEW_MAG

        self.currentProfileScale = 10
        self.series_max_count = 1000

        self.ui.label_Status.setStyleSheet("background-color: yellow;")
        #self.showFullScreen()  # Make the dialog full screen

        self.connectSignalsAndSlots()

        self.run_instruments()

    def get_instrument_config(self, name_instrument, gpio_pin):
        global quspinVersion

        config_object = configparser.ConfigParser()
        config_object.read(config_PI_file)

        param_instrument = Instrument()
        param_instrument.name_instrument = name_instrument

        config_inst = config_object["INSTRUMENT_" + name_instrument]

        if config_inst["disabled"].strip() == "false":
            param_instrument.enabled = True

        param_instrument.label = config_inst["label"].strip()
        param_instrument.parser = config_inst["parser"].strip()
        param_instrument.inst_port = config_inst["port"].strip()
        param_instrument.inst_baudrate = int(config_inst["baudrate"].strip())

        param_instrument.speed_Hz = config_inst["speed_Hz"].strip()

        if config_inst["rawdata_log_disabled"].strip() == "false":
            param_instrument.rawdata_log_enabled = True

        parser_inst = config_object[param_instrument.parser]

        param_instrument.packetheader = parser_inst["packetheader"].strip()

        param_instrument.gpio_pin = gpio_pin

        if name_instrument == "QTFM_V2":
            quspinVersion = "2"

        return param_instrument

    def get_adhat_config(self):

        config_object = configparser.ConfigParser()
        config_object.read(config_PI_file)

        param_instrument = Instrument_ADHAT(self)
        param_instrument.name_instrument = "ADHAT"

        config_inst = config_object["INSTRUMENT_" + param_instrument.name_instrument]

        if config_inst["disabled"].strip() == "false":
            param_instrument.enabled = True

        param_instrument.label = config_inst["label"].strip()
        param_instrument.parser = config_inst["parser"].strip()
        param_instrument.inst_port = config_inst["port"].strip()
        param_instrument.inst_baudrate = int(config_inst["baudrate"].strip())

        param_instrument.speed_Hz = config_inst["speed_Hz"].strip()

        if config_inst["rawdata_log_disabled"].strip() == "false":
            param_instrument.rawdata_log_enabled = True

        parser_inst = config_object[param_instrument.parser]

        param_instrument.packetheader = parser_inst["packetheader"].strip()

        for i in range(5):  # 5 channels, index 0-4
            param_instrument.channel_active.append(config_inst["channel_" + str(i + 1) + "_active"].strip() == 'true')
            param_instrument.ch_multiplier.append(float(config_inst["ch_" + str(i + 1) + "_multiplier"].strip()))
            param_instrument.ch_offset.append(float(config_inst["ch_" + str(i + 1) + "_offset"].strip()))

            # Check if the divider is in hexadecimal format, and convert if necessary
            divider_str = config_inst["ch_" + str(i + 1) + "_divider"].strip()
            if divider_str.startswith("0x") or divider_str.startswith("0X"):
                param_instrument.ch_divider.append(int(divider_str, 16))  # Convert hex to decimal
            else:
                param_instrument.ch_divider.append(float(divider_str))  # If not hex, treat as decimal

        return param_instrument

    def _timestamp(self, prec=2):
        t = gga_timestamp
        s = time.strftime("%H%M%S", time.localtime(t))
        if prec > 0:
            s += ("%.9f" % (t % 1,))[1:2 + prec]

        return s

    def generate_timestamp(self, t=gga_timestamp, prec=2, add_time=0):
        s = time.strftime("%H%M%S", time.localtime(t + add_time))
        if prec > 0:
            s += ("%.9f" % ((t + add_time) % 1,))[1:2 + prec]

            f = round(float(s), prec - 1)

        return str(f)

    def run_instruments(self):
        global isEnable_GPS
        global isEnable_KMAG4
        global isEnable_KANA8
        global isEnable_LASER
        global isEnable_QTFM
        global isEnable_RA4500
        global isEnable_ADHAT
        global dataOutput
        global Logdirectory
        global file_write_delay_sec
        global instrument_timestamp_enable
        global profile_viewer_time

        config_PI_file = "DefaultConfiguration_PI.txt"
        config_object_PI = configparser.ConfigParser()
        config_object_PI.read(config_PI_file)

        # Get Logdirectory
        config_PI = config_object_PI["CONFIG_PI"]

        current_time = datetime.datetime.now()

        if platform != "win32":
            Logdirectory = config_PI["logdirectory"].strip()

            if not os.path.isdir(Logdirectory):
                os.mkdir(Logdirectory)

        else:
            Logdirectory = current_time.strftime("%Y%m%d") + "\\"

            if not os.path.isdir(Logdirectory):
                os.mkdir(Logdirectory)

        Logfilename = config_PI["logfile_name"].strip() + current_time.strftime("_%Y-%m-%d %H_%M_%S") + ".csv"

        instrument_amount = int(config_PI["instrument_amount"].strip())

        if instrument_amount < 1:
            print("ERROR: CONFIG_PI instrument_amount is wrong")

        file_write_delay_sec = int(config_PI["file_write_time"].strip())

        profile_viewer_time = int(config_PI["profile_viewer_time"].strip())

        if config_PI["instrument_timestamp_enable"].strip() == "true":
            instrument_timestamp_enable = True

        instrument_List = []

        for inst in range(1, instrument_amount + 1):
            inst_name = config_PI["instrument_" + str(inst)].strip()

            gpio_led_pin = int(config_PI["gpio_led_pin_" + str(inst)].strip())

            print("Instrument=" + inst_name + " GPI_PIN=" + str(gpio_led_pin))
            instrument_config = self.get_instrument_config(inst_name, gpio_led_pin)

            if instrument_config.enabled:
                instrument_List.append(instrument_config)

        # Get Data Output config
        dataOutput = self.DataOutput_Init()

        self.start_timer = time.time()

        if dataOutput.enabled:
            self.dataOutput_timer = QTimer()
            self.dataOutput_timer.timeout.connect(self.DataOutput_Process)
            self.dataOutput_timer.start(200)  # Update every 100 ms

        # self.program_msg_q_timer = QTimer()
        # self.program_msg_q_timer.timeout.connect(self.processDataLogging)
        # self.program_msg_q_timer.start(200)  # Update every 100 ms
        self.dataLogger_proc = self.DataLogger_Process()
        self.dataLogger_proc.start(QThread.Priority.NormalPriority)

        ################# Checking Com Ports ###############################

        if platform != "win32":
            available_ports = self.auto_detect_serial_unix()
        else:
            available_ports = self.auto_detect_serial_win()

        for inst in instrument_List:
            for port in available_ports:
                if not inst.connected:
                    if self.auto_detect_instrument(port, inst):
                        inst.connected = True
                        inst.inst_port = port
                        available_ports.remove(port)

                        if inst.name_instrument == "GPS":
                            isEnable_GPS = True
                        if inst.name_instrument == "KMAG4":
                            isEnable_KMAG4 = True
                        if inst.name_instrument == "KANA8":
                            isEnable_KANA8 = True
                        if inst.name_instrument == "LASER":
                            isEnable_LASER = True
                        if "QTFM" in inst.name_instrument:
                            isEnable_QTFM = True
                        if inst.name_instrument == "RA4500":
                            isEnable_RA4500 = True
                        if inst.name_instrument == "ADHAT":
                            isEnable_ADHAT = True

                        break

        ################# Create Thread #################

        if not isEnable_GPS:
            self.ui.label_Error.setText(
                QCoreApplication.translate("DataLogger_Profile", u"GPS NOT DETECTED\nNO CSV FILE GENERATION", None))

        elif not isEnable_QTFM:
            self.ui.label_Error.setText(
                QCoreApplication.translate("DataLogger_Profile", u"QUSPIN  NOT DETECTED\nNO CSV FILE GENERATION", None))

        for inst in instrument_List:

            if inst.connected:
                print("Connected: " + inst.name_instrument)
                if inst.name_instrument == "RA4500":
                    inst.serial = Instrument_Serial_Bin(port=inst.inst_port, baudrate=inst.inst_baudrate, parent=None,
                                                        profile=self)
                elif inst.name_instrument == "ADHAT":
                    inst.serial = Instrument_ADHAT(self)
                    instrument_config = self.get_adhat_config()
                    inst.serial.channel_active = instrument_config.channel_active
                    inst.serial.ch_multiplier = instrument_config.ch_multiplier
                    inst.serial.ch_divider = instrument_config.ch_divider
                    inst.serial.ch_offset = instrument_config.ch_offset

                elif inst.name_instrument == "QTFM_V2":
                    inst.serial = Instrument_HighSpeed_Serial(port=inst.inst_port, baudrate=inst.inst_baudrate, parent=None,
                                                    profile=self)
                else:
                    inst.serial = Instrument_LowSpeed_Serial(port=inst.inst_port, baudrate=inst.inst_baudrate, parent=None,
                                                    profile=self)
                    sleep(2) #Eugene
                read_from_port = self.inst_Process[inst.name_instrument]
                inst.serial.data_ready.connect(read_from_port)
                inst.serial.start(self.inst_ProcessPriority[inst.name_instrument])
                self.instruments_config_array[inst.name_instrument] = inst

    def write_config_file(self, setting, value):
        # Read the existing configuration
        self.config_object_PI.read(self.config_PI_file)

        # Check if the section exists; if not, create it
        if not self.config_object_PI.has_section("CONFIG_PI"):
            self.config_object_PI.add_section("CONFIG_PI")

        # Update the setting with the new value
        self.config_object_PI.set("CONFIG_PI", setting, value)

        # Write the updated configuration back to the file
        with open(self.config_PI_file, 'w') as configfile:
            self.config_object_PI.write(configfile)

    def stop_Profile(self):

        # Quspin
        self.alist_quspin_data.clear()
        self.max_Mag_value = 0
        self.min_Mag_value = 0
        self.mag_numbers.clear()
        self.ortho_X_numbers.clear()
        self.ortho_Y_numbers.clear()
        self.ortho_Z_numbers.clear()
        self.series_Mag.clear()
        self.ortho_chart_widgets[0].series_Obj.clear()
        self.ortho_chart_widgets[1].series_Obj.clear()
        self.ortho_chart_widgets[2].series_Obj.clear()

        if self.quspin_chart_timer:
            self.quspin_chart_timer.stop()

        #GPS
        self.alist_gps_data.clear()
        self.gps_Lon_numbers.clear()
        self.gps_Lat_numbers.clear()
        self.gps_Alt_numbers.clear()

        self.gps_chart_widgets[0].series_Obj.clear()
        self.gps_chart_widgets[1].series_Obj.clear()
        self.gps_chart_widgets[2].series_Obj.clear()

        if self.gps_chart_timer:
            self.gps_chart_timer.stop()

        #LASER
        self.alist_laser_data.clear()
        self.Laser_numbers.clear()
        self.series_Laser.clear()
        if self.laser_chart_timer:
            self.laser_chart_timer.stop()

        # RA4500
        self.alist_ra4500_data.clear()
        self.RA4500_numbers.clear()
        self.series_RA4500.clear()
        if self.ra4500_chart_timer:
            self.ra4500_chart_timer.stop()

        # ADHAT
        self.alist_adhat_data.clear()
        self.ADHAT_numbers.clear()
        self.series_ADHAT.clear()
        if self.adhat_chart_timer:
            self.adhat_chart_timer.stop()

    def set_serial_interval(self, dataRate):

        if dataRate == 4 or dataRate == 8:
            self.serial_interval = 8
        elif dataRate == 16:
            self.serial_interval = 4
        else:
            self.serial_interval = 1

        #print("set_serial_interval: " + str(self.serial_interval))

    def quspin_profile_data(self, QTFMdata):
        global mag_counter
        channel_value = 0
        #print("quspin_profile_data: " + QTFMdata)

        real_time = time.time() - self.quspin_connect_time

        str_current_time = str(real_time)
        current_qtfm_data = str_current_time + ',' + QTFMdata

        self.alist_quspin_data.append(current_qtfm_data)

        start = QTFMdata.find('!') + 1
        end = QTFMdata.find('_')
        mag_str = QTFMdata[start:end]

        mag_counter += 1

        # Mag value check
        if self.check_format(mag_str) is None:
            if (self.last_valid_mag_value == 0):
                return
            else:
                mag_str = str(self.last_valid_mag_value)

        try:
            mag_value = float(mag_str.strip())
        except ValueError:
            value = self.last_valid_mag_value

        vector_valid = False
        if "=" in QTFMdata:
            vector_valid = True

        if vector_valid:
            # vector channels= X, Y or Z
            fQF_X = False
            fQF_Y = False
            fQF_Z = False
            if "X" in QTFMdata:
                fQF_X = True
            elif "Y" in QTFMdata:
                fQF_Y = True
            elif "Z" in QTFMdata:
                fQF_Z = True

            start = QTFMdata.find('_') + 2
            end = QTFMdata.find('=')
            channels_str = QTFMdata[start:end]

            if "nan" in QTFMdata:
                #print(" Time: " + str_current_time + "Warning: Quspin No Data: " + QTFMdata)
                channels_str = ""

            try:
                channel_value = float(channels_str.strip())
            except ValueError:
                channel_value = 0

        if (mag_counter % self.serial_interval) == 0:

            if self.ProfileView is ProfileViewState.PROFILE_VIEW_MAG:
                self.series_Mag.append(float(str_current_time), mag_value)

                if self.series_Mag.count() > self.series_max_count:  # Keep only the last 100 points
                    self.series_Mag.remove(0)

            #if (mag_counter % self.serial_interval) == 0:

            if self.ProfileView is ProfileViewState.PROFILE_VIEW_ORTHO:

                if not channel_value or channel_value == 0 or not vector_valid:
                    return

                if (fQF_X):
                    self.ortho_chart_widgets[0].series_Obj.append(float(str_current_time), channel_value)

                    if self.ortho_chart_widgets[
                        0].series_Obj.count() > self.series_max_count:  # Keep only the last 100 points
                        self.ortho_chart_widgets[0].series_Obj.remove(0)

                if (fQF_Y):
                    self.ortho_chart_widgets[1].series_Obj.append(float(str_current_time), channel_value)

                    if self.ortho_chart_widgets[
                        1].series_Obj.count() > self.series_max_count:  # Keep only the last 100 points
                        self.ortho_chart_widgets[1].series_Obj.remove(0)

                if (fQF_Z):
                    self.ortho_chart_widgets[2].series_Obj.append(float(str_current_time), channel_value)

                    if self.ortho_chart_widgets[
                        2].series_Obj.count() > self.series_max_count:  # Keep only the last 100 points
                        self.ortho_chart_widgets[2].series_Obj.remove(0)

    def gps_profile_data(self, GPSdata):

        if not self.start_timer_Profile or GPSdata.find("GGA") == -1:
            return

        #print("gps_profile_data: " + GPSdata)

        GPS_GGAdata = ""
        gga_utctime = ""
        gga_lat = ""
        gga_lon = ""
        gga_alt = ""

        real_time = time.time() - self.gps_connect_time

        str_current_time = str(real_time)
        current_gps_data = str_current_time + ',' + GPSdata

        self.alist_gps_data.append(current_gps_data)

        st_GPS = current_gps_data.split(",")

        if len(st_GPS) > 11:
            # gga:utctime
            # gga_utctime = st_GPS[2]

            # gga:latitude
            gga_lat = st_GPS[3]

            # gga:longitude
            gga_lon = st_GPS[5]

            # gga:msl_altitude
            gga_alt = st_GPS[10]

        try:
            gga_lat_value = float(gga_lat.strip())
            gga_lon_value = float(gga_lon.strip())
            gga_alt_value = float(gga_alt.strip())
        except ValueError:
            print("GPS Data Error")
            return

        self.gps_chart_widgets[0].series_Obj.append(float(str_current_time), gga_lat_value)

        if self.gps_chart_widgets[0].series_Obj.count() > self.series_max_count:  # Keep only the last 100 points
            self.gps_chart_widgets[0].series_Obj.remove(0)

        self.gps_chart_widgets[1].series_Obj.append(float(str_current_time), gga_lon_value)

        if self.gps_chart_widgets[1].series_Obj.count() > self.series_max_count:  # Keep only the last 100 points
            self.gps_chart_widgets[1].series_Obj.remove(0)

        self.gps_chart_widgets[2].series_Obj.append(float(str_current_time), gga_alt_value)

        if self.gps_chart_widgets[2].series_Obj.count() > self.series_max_count:  # Keep only the last 100 points
            self.gps_chart_widgets[2].series_Obj.remove(0)

    def laser_profile_data(self, laser_data):
        global lastLaserHeight

        if not self.start_timer_Profile:
            return

        if len(laser_data) > 0:

            laser_data = laser_data.replace("m", "")

            st_Laser = laser_data.split(",")

            if st_Laser[0] != "999999":
                lastLaserHeight = st_Laser[0]
        try:
            laser_value = float(lastLaserHeight.strip())
        except ValueError:
            print(f"Laser Data Error: {laser_data}")
            return

        real_time = time.time() - self.laser_connect_time

        str_current_time = str(real_time)
        current_laser_data = str_current_time + ',' + lastLaserHeight

        self.alist_laser_data.append(current_laser_data)

        self.series_Laser.append(float(str_current_time), laser_value)

        if self.series_Laser.count() > self.series_max_count:  # Keep only the last 100 points
            self.series_Laser.remove(0)

    def ra4500_profile_data(self, ra4500_value):

        if not self.start_timer_Profile:
            return

        real_time = time.time() - self.ra4500_connect_time

        str_current_time = str(real_time)
        current_ra4500_data = str_current_time + ',' + str(ra4500_value)

        self.alist_ra4500_data.append(current_ra4500_data)

        self.series_RA4500.append(float(str_current_time), ra4500_value)

        if self.series_RA4500.count() > self.series_max_count:  # Keep only the last 100 points
            self.series_RA4500.remove(0)

    def adhat_profile_data(self, adhat_value):

        if not self.start_timer_Profile:
            return

        real_time = time.time() - self.adhat_connect_time

        str_current_time = str(real_time)
        current_adhat_data = str_current_time + ',' + str(adhat_value[self.profile_channel_index])

        self.alist_adhat_data.append(current_adhat_data)

        self.series_ADHAT.append(float(str_current_time), adhat_value[self.profile_channel_index])

        if self.series_ADHAT.count() > self.series_max_count:  # Keep only the last 100 points
            self.series_ADHAT.remove(0)

    def update_quspin_chart(self):
        global last_msclock
        global last_datacount
        global valid_mag_filter
        global quspin_speed_detect_value

        if not self.start_timer_Profile or (
                self.ProfileView != ProfileViewState.PROFILE_VIEW_MAG and self.ProfileView != ProfileViewState.PROFILE_VIEW_ORTHO):
            # self.alist_quspin_data.clear()
            # self.series_Mag.clear()
            return

        while len(self.alist_quspin_data) > 0:

            # Wait chart timer
            if (time.time() - self.display_time_mag_wait) > 10 and (time.time() - self.display_time_mag_wait) < 10.3:
                return

            if (time.time() - self.display_time_mag_wait) >= 10.3:
                self.display_time_mag_wait = time.time()  # Reset the timer
                #print("Quspin Reset Timer")

                record_amount = int((0.3 * 1000) / quspin_speed_detect_value)  # Calculate records to delete
                if len(self.alist_quspin_data) < record_amount:
                    record_amount = len(self.alist_quspin_data) - 2  # Limit the number of records to delete

                    del self.alist_quspin_data[:record_amount]  # Delete the calculated number of elements

            QTFMdata = self.alist_quspin_data[0]
            del self.alist_quspin_data[0]

            resultData = ""

            QTFMdata = re.sub('\r\n', '', QTFMdata)

            if len(QTFMdata) > 0:
                # print(QTFMdata)

                valid_mag = False
                if "_" in QTFMdata:

                    valid_mag = True
                    QTFMdata = QTFMdata.replace("_", "")

                elif "*" in QTFMdata:

                    valid_mag = False
                    QTFMdata = QTFMdata.replace("*", "")

                # vector channels= X, Y or Z
                fQF_X = False
                fQF_Y = False
                fQF_Z = False
                if "X" in QTFMdata:

                    fQF_X = True
                    QTFMdata = QTFMdata.replace("X", ",")

                elif "Y" in QTFMdata:

                    fQF_Y = True
                    QTFMdata = QTFMdata.replace("Y", ",")

                elif "Z" in QTFMdata:

                    fQF_Z = True
                    QTFMdata = QTFMdata.replace("Z", ",")

                vector_valid = False
                if "=" in QTFMdata:

                    vector_valid = True
                    #QTFMdata = QTFMdata.replace("=", ",")
                    QTFMdata = QTFMdata.replace("=", "")

                elif "?" in QTFMdata:

                    vector_valid = False
                    QTFMdata = QTFMdata.replace("?", "")

                QTFMdata = QTFMdata.replace("!", "")

                #  # vector channels= X, Y or Z (_Y-22790.819)
                #QTFMdata = QTFMdata.replace("-", "")
                # @ 022  datacounter...always 3 digits
                QTFMdata = QTFMdata.replace("@", ",")

                # > q_msclock
                QTFMdata = QTFMdata.replace(">", ",")

                # s094                      mag_sensitivity
                QTFMdata = QTFMdata.replace("s", ",")

                # v006              vector_synsitivy
                QTFMdata = QTFMdata.replace("v", ",")

                QTFMdata += ",0,0,0,0,0,0,0,0,0,0,"  # just in case for missing data s and v

                st_QTFM_Data = QTFMdata.split(",")

                # 25. qtfm: q_mag
                resultData += st_QTFM_Data[1] + ","

                if self.check_format(st_QTFM_Data[1]) is None:
                    if (self.last_valid_mag_value == 0):
                        continue
                    else:
                        st_QTFM_Data[1] = str(self.last_valid_mag_value)

                try:
                    mag_value = float(st_QTFM_Data[1].strip())
                except ValueError:
                    mag_value = self.last_valid_mag_value
                    print("Error float: " + st_QTFM_Data[1].strip())
                    print("replace value: " + mag_value)
                    # qtfm: q_fid
                resultData += st_QTFM_Data[2] + ","

                # 24.qtfm: q_mag_valid
                if (valid_mag):
                    resultData += "TRUE" + ","
                else:
                    resultData += "FALSE" + ","

                # 26. qtfm: q_mag_sens
                resultData += st_QTFM_Data[5] + ","

                # 27.qtfm: qf_valid
                if (vector_valid):
                    resultData += "TRUE" + ","
                else:
                    resultData += "FALSE" + ","

                channels_str = st_QTFM_Data[2]
                if "nan" in st_QTFM_Data[2]:
                    channels_str = ""

                # 28.qtfm:qf_x
                if (fQF_X):
                    resultData += channels_str + ","
                else:
                    resultData += ","

                # 29. qtfm: qf_y
                if (fQF_Y):
                    resultData += channels_str + ","
                else:
                    resultData += ","

                # 30. qtfm: qf_z
                if (fQF_Z):
                    resultData += channels_str + ","
                else:
                    resultData += ","

                try:
                    channel_value = float(st_QTFM_Data[2].strip())
                except ValueError:
                    return

                # 31.qtfm: qf_sens
                if st_QTFM_Data[8] is not None:
                    resultData += st_QTFM_Data[8] + ","

                if (self.connection_state != ConnectionState.BLUE) and valid_mag is True and fQF_X is True:
                    self.connection_state = ConnectionState.BLUE
                    self.ui.label_Status.setStyleSheet("background-color: blue;")

                if (self.connection_state != ConnectionState.RED) and \
                        (valid_mag is False or
                         (fQF_X is False and fQF_Y is False and fQF_Z is False)):
                    self.connection_state = ConnectionState.RED
                    self.ui.label_Status.setStyleSheet("background-color: red;")

                current_time = float(st_QTFM_Data[0])

                if self.ProfileView == ProfileViewState.PROFILE_VIEW_MAG:
                    # check filter
                    if self.series_Mag.count() > 10:

                        if self.check_difference(mag_value, self.min_Mag_value, self.max_Mag_value):
                            valid_mag_filter = +1
                        else:
                            valid_mag_filter = 0

                        if valid_mag_filter > 0 and valid_mag_filter < 4 and self.last_valid_mag_value > 0:
                            mag_value = self.last_valid_mag_value

                    self.last_valid_mag_value = mag_value
                    self.mag_numbers.append(mag_value)

                    if (time.time() - self.update_display_time_mag) > 0.15:
                        self.update_display_time_mag = time.time()

                        if self.series_Mag.count() > 1:
                            self.max_Mag_value = max(self.mag_numbers)
                            self.min_Mag_value = min(self.mag_numbers)

                            mag_numbers_threshold = int((self.currentProfileScale * 1000) / self.CurrentDataRate)
                            if len(self.mag_numbers) > mag_numbers_threshold:  # Adjust this threshold as needed
                                self.mag_numbers = self.mag_numbers[
                                                   -mag_numbers_threshold:]  # Keep the last 1000 elements

                            self.ui.lcdNumber_CurrentMag.display(mag_value)
                            self.ui.lcdNumber_MaxMag.display(self.max_Mag_value)
                            self.ui.lcdNumber_MinMag.display(self.min_Mag_value)

                            self.axis_y_Mag.setRange(self.min_Mag_value - 1, self.max_Mag_value + 1)

                            self.axis_x_Mag.setRange(current_time - self.currentProfileScale, current_time)

                #**************************************************************************
                if self.ProfileView == ProfileViewState.PROFILE_VIEW_ORTHO:

                    if not channels_str:
                        return

                    formatted_channel_value = f"{channel_value:.0f}"

                    ortho_numbers_threshold = int((self.currentProfileScale * 1000) /
                                                  (self.CurrentDataRate * self.chart_factor))

                    if (fQF_X):
                        self.ortho_X_numbers.append(channel_value)

                        # if self.max_ortho_X_value == 0:
                        #     self.max_ortho_X_value = channel_value
                        #     self.min_ortho_X_value = channel_value
                        #
                        # if channel_value > self.max_ortho_X_value:
                        #     self.max_ortho_X_value = channel_value
                        #
                        # if channel_value < self.min_ortho_X_value:
                        #     self.min_ortho_X_value = channel_value

                        if (time.time() - self.update_display_time_ortho_X) > 0.15:
                            self.update_display_time_ortho_X = time.time()

                            if self.ortho_chart_widgets[0].series_Obj.count() > 1:
                                self.max_ortho_X_value = max(self.ortho_X_numbers)
                                self.min_ortho_X_value = min(self.ortho_X_numbers)

                                if len(self.ortho_X_numbers) > ortho_numbers_threshold:  # Adjust this threshold as needed
                                    self.ortho_X_numbers = self.ortho_X_numbers[
                                                           -ortho_numbers_threshold:]  # Keep the last 1000 elements

                                self.ui.lcdNumber_Channel_X.display(formatted_channel_value)

                                self.ortho_chart_widgets[0].axis_y.setRange(self.min_ortho_X_value - 1,
                                                                            self.max_ortho_X_value + 1)

                                self.ortho_chart_widgets[0].axis_x.setRange(
                                    current_time - self.currentProfileScale, current_time)

                    if (fQF_Y):
                        self.ortho_Y_numbers.append(channel_value)

                        if len(self.ortho_Y_numbers) > ortho_numbers_threshold:  # Adjust this threshold as needed
                            self.ortho_Y_numbers = self.ortho_Y_numbers[
                                                   -ortho_numbers_threshold:]  # Keep the last 1000 elements

                        if (time.time() - self.update_display_time_ortho_Y) > 0.15:
                            self.update_display_time_ortho_Y = time.time()

                            if self.ortho_chart_widgets[1].series_Obj.count() > 1:
                                self.max_ortho_Y_value = max(self.ortho_Y_numbers)
                                self.min_ortho_Y_value = min(self.ortho_Y_numbers)

                                self.ui.lcdNumber_Channel_Y.display(formatted_channel_value)

                                self.ortho_chart_widgets[1].axis_y.setRange(self.min_ortho_Y_value - 1,
                                                                            self.max_ortho_Y_value + 1)

                                self.ortho_chart_widgets[1].axis_x.setRange(
                                    current_time - self.currentProfileScale, current_time)

                    if (fQF_Z):
                        self.ortho_Z_numbers.append(channel_value)

                        if len(self.ortho_Z_numbers) > ortho_numbers_threshold:  # Adjust this threshold as needed
                            self.ortho_Z_numbers = self.ortho_Z_numbers[
                                                   -ortho_numbers_threshold:]  # Keep the last 1000 elements

                        if (time.time() - self.update_display_time_ortho_Z) > 0.15:
                            self.update_display_time_ortho_Z = time.time()

                            if self.ortho_chart_widgets[2].series_Obj.count() > 1:
                                self.max_ortho_Z_value = max(self.ortho_Z_numbers)
                                self.min_ortho_Z_value = min(self.ortho_Z_numbers)

                                self.ui.lcdNumber_Channel_Z.display(formatted_channel_value)

                                self.ortho_chart_widgets[2].axis_y.setRange(self.min_ortho_Z_value - 1,
                                                                            self.max_ortho_Z_value + 1)

                                self.ortho_chart_widgets[2].axis_x.setRange(
                                    current_time - self.currentProfileScale, current_time)

    def update_gps_chart(self):

        if not self.start_timer_Profile or self.ProfileView != ProfileViewState.PROFILE_VIEW_GPS:
            return

        if not gps_antenna_on:
            return

        gps_numbers_threshold = int(self.currentProfileScale * 100)

        while len(self.alist_gps_data) > 0:
            gps_data = self.alist_gps_data[0]
            del self.alist_gps_data[0]

            gps_data = re.sub('\r\n', '', gps_data)

            st_GPS = gps_data.split(",")

            current_time = float(st_GPS[0])

            if len(st_GPS) > 11:
                # gga:utctime
                # gga_utctime = st_GPS[2]

                # gga:latitude
                gga_lat = st_GPS[3]

                # gga:longitude
                gga_lon = st_GPS[5]

                # gga:msl_altitude
                gga_alt = st_GPS[10]

            try:
                gga_lat_value = float(gga_lat.strip())
                gga_lon_value = float(gga_lon.strip())
                gga_alt_value = float(gga_alt.strip())
            except ValueError:
                print("GPS Data Error")
                return

            self.gps_Lat_numbers.append(gga_lat_value)
            self.gps_Lon_numbers.append(gga_lon_value)
            self.gps_Alt_numbers.append(gga_alt_value)

            if (time.time() - self.update_display_time_gps_lat) > 0.15:
                self.update_display_time_gps_lat = time.time()

                if self.gps_chart_widgets[0].series_Obj.count() > 1:
                    self.max_gps_Lat_value = max(self.gps_Lat_numbers)
                    self.min_gps_Lat_value = min(self.gps_Lat_numbers)

                    if len(self.gps_Lat_numbers) > gps_numbers_threshold:  # Adjust this threshold as needed
                        # Keep the last 1000 elements
                        self.gps_Lat_numbers = self.gps_Lat_numbers[-gps_numbers_threshold:]

                    self.gps_chart_widgets[0].axis_y.setRange(self.min_gps_Lat_value - 1,
                                                              self.max_gps_Lat_value + 1)
                    self.gps_chart_widgets[0].axis_x.setRange(
                        current_time - self.currentProfileScale, current_time)

                    self.ui.lcdNumber_GPS_Lat.display(f"{gga_lat_value:.0f}")

                if self.gps_chart_widgets[1].series_Obj.count() > 1:
                    self.max_gps_Lon_value = max(self.gps_Lon_numbers)
                    self.min_gps_Lon_value = min(self.gps_Lon_numbers)

                    if len(self.gps_Lon_numbers) > gps_numbers_threshold:  # Adjust this threshold as needed
                        # Keep the last 1000 elements
                        self.gps_Lon_numbers = self.gps_Lon_numbers[-gps_numbers_threshold:]

                    self.gps_chart_widgets[1].axis_y.setRange(self.min_gps_Lon_value - 1,
                                                              self.max_gps_Lon_value + 1)
                    self.gps_chart_widgets[1].axis_x.setRange(
                        current_time - self.currentProfileScale, current_time)

                    self.ui.lcdNumber_GPS_Lon.display(f"{gga_lon_value:.0f}")

                if self.gps_chart_widgets[2].series_Obj.count() > 1:
                    self.max_gps_Alt_value = max(self.gps_Alt_numbers)
                    self.min_gps_Alt_value = min(self.gps_Alt_numbers)

                    if len(self.gps_Alt_numbers) > gps_numbers_threshold:  # Adjust this threshold as needed
                        # Keep the last 1000 elements
                        self.gps_Alt_numbers = self.gps_Alt_numbers[-gps_numbers_threshold:]

                    self.gps_chart_widgets[2].axis_y.setRange(self.min_gps_Alt_value - 1,
                                                              self.max_gps_Alt_value + 1)
                    self.gps_chart_widgets[2].axis_x.setRange(
                        current_time - self.currentProfileScale, current_time)

                    self.ui.lcdNumber_GPS_Alt.display(f"{gga_alt_value:.0f}")

    def update_laser_chart(self):

        if not self.start_timer_Profile or self.ProfileView != ProfileViewState.PROFILE_VIEW_LASER:
            return

        laser_numbers_threshold = int(self.currentProfileScale * 50)

        while len(self.alist_laser_data) > 0:
            laser_data = self.alist_laser_data[0]
            del self.alist_laser_data[0]

            laser_data = re.sub('\r\n', '', laser_data)

            st_laser = laser_data.split(",")

            current_time = float(st_laser[0])

            if len(st_laser) > 1:
                try:
                    laser_value = float(st_laser[1].strip())
                except ValueError:
                    print("Laser Data Error")
                    return

            self.Laser_numbers.append(laser_value)

            if (time.time() - self.update_display_time_laser) > 0.15:
                self.update_display_time_laser = time.time()

                if self.series_Laser.count() > 1:
                    self.max_laser_value = max(self.Laser_numbers)
                    self.min_laser_value = min(self.Laser_numbers)

                    if len(self.Laser_numbers) > laser_numbers_threshold:  # Adjust this threshold as needed
                        # Keep the last 1000 elements
                        self.Laser_numbers = self.Laser_numbers[-laser_numbers_threshold:]

                    self.axis_y_Laser.setRange(self.min_laser_value - 1,
                                               self.max_laser_value + 1)
                    self.axis_x_Laser.setRange(
                        current_time - self.currentProfileScale, current_time)

                    self.ui.lcdNumber_MaxLaser.display(f"{self.max_laser_value:.0f}")
                    self.ui.lcdNumber_CurrentLaser.display(f"{laser_value:.0f}")
                    self.ui.lcdNumber_MinLaser.display(f"{self.min_laser_value:.0f}")

    def update_ra4500_chart(self):

        if not self.start_timer_Profile or self.ProfileView != ProfileViewState.PROFILE_VIEW_RA4500:
            return

        ra4500_numbers_threshold = int(self.currentProfileScale * 25)

        while len(self.alist_ra4500_data) > 0:
            ra4500_data = self.alist_ra4500_data[0]
            del self.alist_ra4500_data[0]

            ra4500_data = re.sub('\r\n', '', ra4500_data)

            st_ra4500 = ra4500_data.split(",")

            current_time = float(st_ra4500[0])

            if len(st_ra4500) > 1:
                try:
                    ra4500_value = float(st_ra4500[1].strip())
                except ValueError:
                    print("ra4500 Data Error")
                    return

            self.RA4500_numbers.append(ra4500_value)

            if (time.time() - self.update_display_time_ra4500) > 0.15:
                self.update_display_time_ra4500 = time.time()

                if self.series_RA4500.count() > 1:
                    self.max_ra4500_value = max(self.RA4500_numbers)
                    self.min_ra4500_value = min(self.RA4500_numbers)

                    if len(self.RA4500_numbers) > ra4500_numbers_threshold:  # Adjust this threshold as needed
                        # Keep the last 1000 elements
                        self.RA4500_numbers = self.RA4500_numbers[-ra4500_numbers_threshold:]

                    self.axis_y_RA4500.setRange(self.min_ra4500_value - 1,
                                                self.max_ra4500_value + 1)
                    self.axis_x_RA4500.setRange(
                        current_time - self.currentProfileScale, current_time)

                    self.ui.lcdNumber_MaxRA4500.display(f"{self.max_ra4500_value:.0f}")
                    self.ui.lcdNumber_CurrentRA4500.display(f"{ra4500_value:.0f}")
                    self.ui.lcdNumber_MinRA4500.display(f"{self.min_ra4500_value:.0f}")

    def update_adhat_chart(self):

        if not self.start_timer_Profile or self.ProfileView != ProfileViewState.PROFILE_VIEW_ADHAT:
            return

        adhat_numbers_threshold = int(self.currentProfileScale * 10)

        while len(self.alist_adhat_data) > 0:
            adhat_data = self.alist_adhat_data[0]
            del self.alist_adhat_data[0]

            adhat_data = re.sub('\r\n', '', adhat_data)

            st_adhat = adhat_data.split(",")

            current_time = float(st_adhat[0])

            if len(st_adhat) > 1:
                try:
                    adhat_value = float(st_adhat[1].strip())
                except ValueError:
                    print("adhat Data Error")
                    return

            self.ADHAT_numbers.append(adhat_value)

            if (time.time() - self.update_display_time_adhat) > 0.15:
                self.update_display_time_adhat = time.time()

                if self.series_ADHAT.count() > 1:
                    self.max_adhat_value = max(self.ADHAT_numbers)
                    self.min_adhat_value = min(self.ADHAT_numbers)

                    if len(self.ADHAT_numbers) > adhat_numbers_threshold:  # Adjust this threshold as needed
                        # Keep the last 1000 elements
                        self.ADHAT_numbers = self.ADHAT_numbers[-adhat_numbers_threshold:]

                    self.axis_y_ADHAT.setRange(self.min_adhat_value - 1,
                                               self.max_adhat_value + 1)
                    self.axis_x_ADHAT.setRange(
                        current_time - self.currentProfileScale, current_time)

                    self.ui.lcdNumber_MaxADHAT.display(f"{self.max_adhat_value:.0f}")
                    self.ui.lcdNumber_CurrentADHAT.display(f"{adhat_value:.0f}")
                    self.ui.lcdNumber_MinADHAT.display(f"{self.min_adhat_value:.0f}")

    def check_difference(self, current_value, min_value, max_value):
        # Calculate the percentage differences
        if min_value != 0:
            diff_min = abs(current_value - min_value) / abs(min_value) * 100
        else:
            diff_min = float('inf')  # Handle division by zero

        if max_value != 0:
            diff_max = abs(current_value - max_value) / abs(max_value) * 100
        else:
            diff_max = float('inf')  # Handle division by zero

        # Check if any difference exceeds 300%
        flag = diff_min > 300 or diff_max > 300

        return flag

    def check_format(self, input_string):
        # Define the regular expression pattern
        pattern = r'^\d+\.\d+$'

        # Check if the input string matches the pattern
        if re.match(pattern, input_string):
            return input_string
        else:
            return None

    def remove_special_sequences(self, input_string):
        # Define the regular expression pattern
        pattern = r'\\x\w{3}'

        # Use re.sub to replace occurrences of the pattern with an empty string
        cleaned_string = re.sub(pattern, '', input_string)

        return cleaned_string

    def extract_part(self, input_string):
        # Define the regular expression pattern
        pattern = r'\d+\.(\d+\.\d+)'

        # Search for the pattern in the input string
        match = re.search(pattern, input_string)

        # If a match is found, extract the desired part
        if match:
            return match.group(1)
        else:
            return None

    def is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def extract_numbers(self, text):
        # Define the regex pattern to capture all sequences of digits
        pattern = r'\d+'

        # Find all occurrences of the pattern
        matches = re.findall(pattern, text)

        # Convert the found matches to integers
        numbers = [int(match) for match in matches]

        return numbers

    def extract_value(self, text, key):
        # Define the regex pattern dynamically using the key
        pattern = fr"{re.escape(key)} (\S+)"

        # Search for the pattern in the text
        match = re.search(pattern, text)

        # If a match is found, return the captured group (the value)
        if match:
            return match.group(1)

        # Return None if no match is found
        return None

    def extract_environment(self, text, key):

        if text.find("Auto Optimization Mode On") != -1:
            return "Auto"

        text_no_whitespace = ''.join(text.split())

        # Remove the word "Environment"
        formated_text = text_no_whitespace.replace("Environment", "")

        # Define the regex pattern to capture the environment description
        pattern = re.escape(key) + r"(.*?)]"

        # Search for the pattern in the text
        match = re.search(pattern, formated_text)

        # If a match is found, return the captured group (the environment description)
        if match:
            return match.group(1).strip()

        # Return None if no match is found
        return ""

    def extract_raw_substring(self, input_string):
        # Find the position of the first '!' character
        exclamation_index = input_string.find('!')
        if exclamation_index != -1:
            # Return the substring starting from the '!' character
            return input_string[exclamation_index:]
        return ""

    def serialPortConfig(self):
        if platform != "win32":
            available_ports = self.auto_detect_serial_unix()
        else:
            available_ports = self.auto_detect_serial_win()

        for port in available_ports:

            if platform == "win32":
                port_name = port.name
            else:
                port_name = port

            self.serialPortList.append(port_name)

    def auto_detect_serial_unix(self):
        '''try to auto-detect serial ports on posix based OS'''
        preferred_list = ['*']
        glist = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyAMA*') + glob.glob(
            '/dev/ttyS*')
        ret = []

        # try preferred ones first
        for d in glist:
            for preferred in preferred_list:
                if fnmatch.fnmatch(d, preferred):
                    # ret.append(port(d))
                    ret.append(d)
        if len(ret) > 0:
            return ret
        # now the rest
        for d in glist:
            # ret.append(port(d))
            ret.append(d)
        return ret

    def auto_detect_serial_win(self):
        ports = serial.tools.list_ports.comports(include_links=False)
        return ports

    def connectSignalsAndSlots(self):

        # pushButton_ProfileView
        self.ui.pushButton_ProfileView.is_on = False
        self.ui.pushButton_ProfileView.clicked.connect(self.on_button_click_ProfileView)

        #pushButton_Exit
        self.ui.pushButton_Exit.clicked.connect(self.on_button_click_Exit)

        #pushButton_ProfileScale
        self.profile_scale = [10, 30, 60, 120]
        self.profile_scale_counter_max = [1000, 2000, 3000, 5000]
        self.profile_scale_index = 0
        self.ui.pushButton_ProfileScale.clicked.connect(self.on_button_click_ProfileScale)

        #pushButton_Start_Profile
        self.ui.pushButton_Start_Profile.clicked.connect(self.on_button_click_Start_Profile)

        #pushButton_Stop_Profile
        self.ui.pushButton_Stop_Profile.clicked.connect(self.on_button_click_Stop_Profile)

        #pushButton_Channel
        self.profile_channel = [1, 2, 3, 4, 5]
        self.profile_channel_index = 0
        self.ui.pushButton_Channel.clicked.connect(self.on_button_click_Channel)

        self.alist_quspin_data = []
        self.alist_gps_data = []
        self.alist_ra4500_data = []
        self.alist_adhat_data = []
        self.alist_laser_data = []

        self.createProfile_Mag()

        self.createProfile_Ortho()

        self.createProfile_GPS()

        self.createProfile_RA4500()

        self.createProfile_ADHAT()

        self.createProfile_Laser()

    def createProfile_Mag(self):
        # Create Mag QChart and QChartView

        self.chart_Mag = QChart()
        self.chart_Mag_view = QChartView(self.chart_Mag)
        self.chart_Mag_view.setRenderHint(QPainter.Antialiasing)

        self.chart_Mag.legend().hide()

        # Add the chart view to the layout
        self.ui.horizontalLayout_ProfileMag.addWidget(self.chart_Mag_view)

        # Create QLineSeries
        self.series_Mag = QLineSeries()

        # Add the series to the chart
        self.chart_Mag.addSeries(self.series_Mag)

        # Create axes
        self.axis_x_Mag = QValueAxis()
        self.axis_y_Mag = QValueAxis()

        # Set max min mag value
        self.mag_numbers = []
        self.max_Mag_value = 0
        self.min_Mag_value = 0

        # Set range for axes
        self.axis_x_Mag.setTickCount(10)  # Display a tick every 5 seconds for 1 minute

        # Add axes to the chart
        self.chart_Mag.addAxis(self.axis_x_Mag, Qt.AlignBottom)
        self.chart_Mag.addAxis(self.axis_y_Mag, Qt.AlignLeft)

        # Attach axes to the series
        self.series_Mag.attachAxis(self.axis_x_Mag)
        self.series_Mag.attachAxis(self.axis_y_Mag)

    def createProfile_Ortho(self):
        # Set max min Ortho value
        self.ortho_X_numbers = []
        self.max_ortho_X_value = 0
        self.min_ortho_X_value = 0

        self.ortho_Y_numbers = []
        self.max_ortho_Y_value = 0
        self.min_ortho_Y_value = 0

        self.ortho_Z_numbers = []
        self.max_ortho_Z_value = 0
        self.min_ortho_Z_value = 0

        #self.ui.horizontalLayout_ProfileOrtho = QVBoxLayout(self)

        self.ortho_chart_widgets = []
        colors = [Qt.blue, Qt.red, Qt.green]

        self.ui.horizontalLayout_ProfileOrtho.setContentsMargins(0, 0, 0, 0)  # Set margins to 0
        self.ui.horizontalLayout_ProfileOrtho.setSpacing(0)  # Set spacing to 0

        for color in colors:
            chart_widget = ChartWidget(color)
            # Add the chart view to the layout
            self.ui.horizontalLayout_ProfileOrtho.addWidget(chart_widget)
            self.ortho_chart_widgets.append(chart_widget)

        self.setLayout(self.ui.horizontalLayout_ProfileOrtho)

    def createProfile_GPS(self):
        # Set max min Ortho value
        self.gps_Lat_numbers = []
        self.max_gps_Lat_value = 0
        self.min_gps_Lat_value = 0

        self.gps_Lon_numbers = []
        self.max_gps_Lon_value = 0
        self.min_gps_Lon_value = 0

        self.gps_Alt_numbers = []
        self.max_gps_Alt_value = 0
        self.min_gps_Alt_value = 0

        # self.ui.horizontalLayout_ProfileGPS = QVBoxLayout(self)

        self.series_max_count = 1000
        self.gps_chart_widgets = []
        colors = [Qt.blue, Qt.red, Qt.green]

        self.ui.horizontalLayout_ProfileGPS.setContentsMargins(0, 0, 0, 0)  # Set margins to 0
        self.ui.horizontalLayout_ProfileGPS.setSpacing(0)  # Set spacing to 0

        for color in colors:
            chart_widget = ChartWidget(color)
            # Add the chart view to the layout
            self.ui.horizontalLayout_ProfileGPS.addWidget(chart_widget)
            self.gps_chart_widgets.append(chart_widget)

        self.setLayout(self.ui.horizontalLayout_ProfileGPS)

    def createProfile_RA4500(self):
        # Create RA4500 QChart and QChartView

        self.chart_RA4500 = QChart()
        self.chart_RA4500_view = QChartView(self.chart_RA4500)
        self.chart_RA4500_view.setRenderHint(QPainter.Antialiasing)

        self.chart_RA4500.legend().hide()

        # Add the chart view to the layout
        self.ui.horizontalLayout_RA4500.addWidget(self.chart_RA4500_view)

        # Create QLineSeries
        self.series_RA4500 = QLineSeries()

        # Add the series to the chart
        self.chart_RA4500.addSeries(self.series_RA4500)

        # Create axes
        self.axis_x_RA4500 = QValueAxis()
        self.axis_y_RA4500 = QValueAxis()

        # Set max min RA4500 value
        self.RA4500_numbers = []
        self.max_RA4500_value = 0
        self.min_RA4500_value = 0

        # Set range for axes
        self.axis_x_RA4500.setTickCount(10)  # Display a tick every 5 seconds for 1 minute

        # Add axes to the chart
        self.chart_RA4500.addAxis(self.axis_x_RA4500, Qt.AlignBottom)
        self.chart_RA4500.addAxis(self.axis_y_RA4500, Qt.AlignLeft)

        # Attach axes to the series
        self.series_RA4500.attachAxis(self.axis_x_RA4500)
        self.series_RA4500.attachAxis(self.axis_y_RA4500)

    def createProfile_ADHAT(self):
        # Create ADHAT QChart and QChartView

        self.chart_ADHAT = QChart()
        self.chart_ADHAT_view = QChartView(self.chart_ADHAT)
        self.chart_ADHAT_view.setRenderHint(QPainter.Antialiasing)

        self.chart_ADHAT.legend().hide()

        # Add the chart view to the layout
        self.ui.horizontalLayout_ADHAT.addWidget(self.chart_ADHAT_view)

        # Create QLineSeries
        self.series_ADHAT = QLineSeries()

        # Add the series to the chart
        self.chart_ADHAT.addSeries(self.series_ADHAT)

        # Create axes
        self.axis_x_ADHAT = QValueAxis()
        self.axis_y_ADHAT = QValueAxis()

        # Set max min ADHAT value
        self.ADHAT_numbers = []
        self.max_ADHAT_value = 0
        self.min_ADHAT_value = 0

        # Set range for axes
        self.axis_x_ADHAT.setTickCount(10)  # Display a tick every 5 seconds for 1 minute

        # Add axes to the chart
        self.chart_ADHAT.addAxis(self.axis_x_ADHAT, Qt.AlignBottom)
        self.chart_ADHAT.addAxis(self.axis_y_ADHAT, Qt.AlignLeft)

        # Attach axes to the series
        self.series_ADHAT.attachAxis(self.axis_x_ADHAT)
        self.series_ADHAT.attachAxis(self.axis_y_ADHAT)

    def createProfile_Laser(self):
        # Create Laser QChart and QChartView

        self.chart_Laser = QChart()
        self.chart_Laser_view = QChartView(self.chart_Laser)
        self.chart_Laser_view.setRenderHint(QPainter.Antialiasing)

        self.chart_Laser.legend().hide()

        # Add the chart view to the layout
        self.ui.horizontalLayout_ProfileLaser.addWidget(self.chart_Laser_view)

        # Create QLineSeries
        self.series_Laser = QLineSeries()

        # Add the series to the chart
        self.chart_Laser.addSeries(self.series_Laser)

        # Create axes
        self.axis_x_Laser = QValueAxis()
        self.axis_y_Laser = QValueAxis()

        # Set max min Laser value
        self.Laser_numbers = []
        self.max_Laser_value = 0
        self.min_Laser_value = 0

        # Set range for axes
        self.axis_x_Laser.setTickCount(10)  # Display a tick every 5 seconds for 1 minute

        # Add axes to the chart
        self.chart_Laser.addAxis(self.axis_x_Laser, Qt.AlignBottom)
        self.chart_Laser.addAxis(self.axis_y_Laser, Qt.AlignLeft)

        # Attach axes to the series
        self.series_Laser.attachAxis(self.axis_x_Laser)
        self.series_Laser.attachAxis(self.axis_y_Laser)

    def auto_detect_instrument(self, port_name, inst_name):

        #ADHAT
        if inst_name.name_instrument == "ADHAT":
            if platform == "linux" or platform == "linux2":
                try:
                    ADC = ADS1263.ADS1263()

                    if (ADC.ADS1263_init_ADC1('ADS1263_50SPS') == -1):
                        return False
                    else:
                        return True

                except IOError as e:
                    print(e)
            else:
                return True

        baudrate = inst_name.inst_baudrate
        if baudrate == 0:
            return False

        print(inst_name.name_instrument + ": " + str(port_name) + " : " + str(baudrate))
        try:
            if platform == "linux" or platform == "linux2":
                ser = serial.Serial(port_name, baudrate, timeout=1)
            else:
                ser = serial.Serial(port_name.name, baudrate, timeout=1)

            ser.reset_input_buffer()

            #RA4500
            if inst_name.name_instrument == "RA4500":
                delimiter = b'\x10\x03'
                buffer = bytearray()

                byte = ser.read(300)

                if len(byte) == 0:
                    ser.close()
                    return False

                buffer += byte

                if delimiter in buffer:
                    ser.close()
                    return True
                else:
                    ser.close()
                    return False

            else:
                data = ser.read(300)

                str_data = data.decode(encoding="ascii", errors="ignore")

                print(str_data)

                if inst_name.name_instrument == "LASER":
                    if str_data.find("999999") != -1:
                        ser.close()
                        return True

                if inst_name.name_instrument == "QTFM_V2":
                    if str_data.find("re5)") != -1 or str_data.find("ri5)") != -1 or str_data.find("ra5)") != -1:
                        ser.close()
                        return True

                if str_data.find(inst_name.packetheader) != -1:
                    ser.close()
                    return True

                if inst_name.packetheader.find(',') != -1:
                    packet_ids = inst_name.packetheader.split(',')
                    if len(packet_ids) == 2:
                        if str_data.find(packet_ids[0]) != -1 and str_data.find(packet_ids[1]) != -1:
                            ser.close()
                            return True

                ser.close()
                return False



        except serial.SerialException as e:

            pass
        return False

    def init_quspin_chart(self):

        self.quspin_connect_time = time.time()
        self.update_display_time_mag = time.time()
        self.display_time_mag_wait = time.time()
        self.display_time_mag_pause = time.time()
        self.update_display_time_sensivity = time.time()
        self.update_display_time_ortho_X = time.time()
        self.update_display_time_ortho_Y = time.time()
        self.update_display_time_ortho_Z = time.time()

        # Create a QTimer to update quspin chart
        self.quspin_chart_timer = QTimer()
        self.quspin_chart_timer.timeout.connect(self.update_quspin_chart)
        self.quspin_chart_timer.start(100)  # Update every 100 ms

    def init_gps_chart(self):
        self.gps_connect_time = time.time()

        self.update_display_time_gps_lat = time.time()
        self.update_display_time_gps_lon = time.time()
        self.update_display_time_gps_alt = time.time()

        # Create a QTimer to update gps chart
        self.gps_chart_timer = QTimer()
        self.gps_chart_timer.timeout.connect(self.update_gps_chart)
        self.gps_chart_timer.start(100)  # Update every 100 ms

    def init_laser_chart(self):
        self.laser_connect_time = time.time()

        self.update_display_time_laser = time.time()

        # Create a QTimer to update gps chart
        self.laser_chart_timer = QTimer()
        self.laser_chart_timer.timeout.connect(self.update_laser_chart)
        self.laser_chart_timer.start(100)  # Update every 100 ms

    def init_ra4500_chart(self):
        self.ra4500_connect_time = time.time()

        self.update_display_time_ra4500 = time.time()

        # Create a QTimer to update gps chart
        self.ra4500_chart_timer = QTimer()
        self.ra4500_chart_timer.timeout.connect(self.update_ra4500_chart)
        self.ra4500_chart_timer.start(100)  # Update every 100 ms

    def init_adhat_chart(self):
        self.adhat_connect_time = time.time()

        self.update_display_time_adhat = time.time()

        # Create a QTimer to update gps chart
        self.adhat_chart_timer = QTimer()
        self.adhat_chart_timer.timeout.connect(self.update_adhat_chart)
        self.adhat_chart_timer.start(100)  # Update every 100 ms

    def on_button_click_Start_Profile(self):
        global profile_viewer_time

        #if self.start_timer_Profile == True:
        self.stop_Profile()

        if self.ProfileView == ProfileViewState.PROFILE_VIEW_MAG or self.ProfileView == ProfileViewState.PROFILE_VIEW_ORTHO:
            self.init_quspin_chart()

        elif self.ProfileView == ProfileViewState.PROFILE_VIEW_GPS:
            self.init_gps_chart()

        elif self.ProfileView == ProfileViewState.PROFILE_VIEW_LASER:
            self.init_laser_chart()

        elif self.ProfileView == ProfileViewState.PROFILE_VIEW_RA4500:
            self.init_ra4500_chart()

        elif self.ProfileView == ProfileViewState.PROFILE_VIEW_ADHAT:
            self.init_adhat_chart()

        self.start_timer_Profile = True

        if (profile_viewer_time > 0):
            self.profile_viewer_auto_off_timer = QTimer()
            self.profile_viewer_auto_off_timer.timeout.connect(self.on_button_click_Stop_Profile)
            self.profile_viewer_auto_off_timer.start(profile_viewer_time * 1000)

            # if self.ProfileView == ProfileViewState.PROFILE_VIEW_MAG or self.ProfileView == ProfileViewState.PROFILE_VIEW_ORTHO:
            #     self.profile_viewer_pause_on_timer = QTimer()
            #     self.profile_viewer_pause_on_timer.timeout.connect(self.pause_quspin_Profile_ON)
            #     self.profile_viewer_pause_on_timer.start(30 * 1000)

        current_time = datetime.datetime.now()
        str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
        print(str_local_time + ": Profile is ON")

    def pause_quspin_Profile_ON(self):

        self.profile_viewer_pause_off_timer = QTimer()
        self.profile_viewer_pause_off_timer.timeout.connect(self.pause_quspin_Profile_OFF)
        self.profile_viewer_pause_off_timer.start(1 * 1000)

        self.start_timer_Profile = False

        #print("Mag Chart Count: " + str(self.series_Mag.count()))

        # Quspin
        # self.alist_quspin_data.clear()
        # self.max_Mag_value = 0
        # self.min_Mag_value = 0
        # self.mag_numbers.clear()
        # self.ortho_X_numbers.clear()
        # self.ortho_Y_numbers.clear()
        # self.ortho_Z_numbers.clear()

        self.series_Mag.clear()
        self.ortho_chart_widgets[0].series_Obj.clear()
        self.ortho_chart_widgets[1].series_Obj.clear()
        self.ortho_chart_widgets[2].series_Obj.clear()

        if self.quspin_chart_timer:
            self.quspin_chart_timer.stop()

        # current_time = datetime.datetime.now()
        # str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
        # print(str_local_time + ": Profile Pause ON")

    def pause_quspin_Profile_OFF(self):
        global profile_viewer_time

        if self.profile_viewer_pause_off_timer:
            self.profile_viewer_pause_off_timer.stop()

        if self.quspin_chart_timer:
            self.quspin_chart_timer.start()

        self.start_timer_Profile = True

        # current_time = datetime.datetime.now()
        # str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
        # print(str_local_time + ": Profile Pause OFF")

    def on_button_click_Stop_Profile(self):

        if self.profile_viewer_auto_off_timer:
            self.profile_viewer_auto_off_timer.stop()

        # if self.profile_viewer_pause_off_timer:
        #     self.profile_viewer_pause_off_timer.stop()
        #
        # if self.profile_viewer_pause_on_timer:
        #     self.profile_viewer_pause_on_timer.stop()

        self.start_timer_Profile = False
        #self.stop_Profile()
        current_time = datetime.datetime.now()
        str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
        print(str_local_time + ": Profile is OFF")

    def on_button_click_Exit(self):
        self.close()

    def on_button_click_ProfileView(self):

        # Cycle through the enum states
        new_state = (self.ProfileView.value + 1) % len(ProfileViewState)
        self.ProfileView = ProfileViewState(new_state)

        self.start_timer_Profile = False
        self.stop_Profile()

        if self.ProfileView == ProfileViewState.PROFILE_VIEW_MAG:
            self.ui.pushButton_ProfileView.setText(
                QCoreApplication.translate("DataLogger_Profile", u"Profile\nView Mag", None))
            self.ui.tabWidget.setCurrentIndex(0)
        elif self.ProfileView == ProfileViewState.PROFILE_VIEW_ORTHO:
            self.ui.pushButton_ProfileView.setText(
                QCoreApplication.translate("DataLogger_Profile", u"Profile\nView Ortho", None))
            self.ui.tabWidget.setCurrentIndex(1)
        elif self.ProfileView == ProfileViewState.PROFILE_VIEW_GPS:
            self.ui.pushButton_ProfileView.setText(
                QCoreApplication.translate("DataLogger_Profile", u"Profile\nView GPS", None))
            self.ui.tabWidget.setCurrentIndex(2)
        elif self.ProfileView == ProfileViewState.PROFILE_VIEW_RA4500:
            self.ui.pushButton_ProfileView.setText(
                QCoreApplication.translate("DataLogger_Profile", u"Profile\nView RA4500", None))
            self.ui.tabWidget.setCurrentIndex(3)
        elif self.ProfileView == ProfileViewState.PROFILE_VIEW_LASER:
            self.ui.pushButton_ProfileView.setText(
                QCoreApplication.translate("DataLogger_Profile", u"Profile\nView Laser", None))
            self.ui.tabWidget.setCurrentIndex(4)
        elif self.ProfileView == ProfileViewState.PROFILE_VIEW_ADHAT:
            self.ui.pushButton_ProfileView.setText(
                QCoreApplication.translate("DataLogger_Profile", u"Profile\nView ADHAT", None))
            self.ui.tabWidget.setCurrentIndex(5)

    def on_button_click_ProfileScale(self):
        self.profile_scale_index = (self.profile_scale_index + 1) % len(self.profile_scale)

        # Update the button text
        new_text = f"Profile H\nScale {self.profile_scale[self.profile_scale_index]}"
        self.ui.pushButton_ProfileScale.setText(
            QCoreApplication.translate("DataLogger_Profile", new_text, None))

        self.currentProfileScale = self.profile_scale[self.profile_scale_index]
        self.series_max_count = self.profile_scale_counter_max[self.profile_scale_index]

        #if self.series_Mag.count() > self.series_max_count:
        self.series_Mag.clear()

        #if self.ortho_chart_widgets[0].series_Obj.count() > self.series_max_count:
        self.ortho_chart_widgets[0].series_Obj.clear()
        self.ortho_chart_widgets[1].series_Obj.clear()
        self.ortho_chart_widgets[2].series_Obj.clear()

    def on_button_click_Channel(self):
        self.profile_channel_index = (self.profile_channel_index + 1) % len(self.profile_channel)

        # Update the button text
        new_text = f"Channel {self.profile_channel[self.profile_channel_index]}"
        self.ui.pushButton_Channel.setText(
            QCoreApplication.translate("DataLogger_Profile", new_text, None))

    def KMAG4_process(self, reading):
        global synch_sysdate
        global last_KMAG4_utc_time
        global last_KMAG4_data
        global instrument_timestamp_enable

        if not synch_sysdate:
            return False

        if len(reading) > 0:

            str_data = reading
            str_data_clean = re.sub('\x00', '', str_data)

            str_data_clean = last_KMAG4_data + str_data_clean

            # print(str_data_clean)

            add_index = str_data_clean.rfind("$KMAG4")

            last_KMAG4_data = str_data_clean[add_index:]

            str_data_clean = str_data_clean[0:add_index]

            data_parts = str_data_clean.split("$KMAG4")

            for data_line in data_parts:

                if len(data_line) > 50:
                    data_clean = re.sub('\r\n', '', data_line)
                    data_line = "$KMAG4" + data_clean

                    st_KMAG4 = data_line.split(",")
                    str_utc_time = st_KMAG4[2]

                    if ('000000' not in str_utc_time) and (str_utc_time != ""):
                        last_KMAG4_utc_time = str_utc_time

                    # print(data_line)
                    if last_KMAG4_utc_time != "":
                        dataObj = raw_data_struct()
                        dataObj.utctime = last_KMAG4_utc_time
                        dataObj.raw_data = data_line

                        if instrument_timestamp_enable:
                            current_time = datetime.datetime.now()
                            str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                            dataObj.raw_data = dataObj.raw_data + "," + "instr_timestamp=" + str_local_time

                        alist_KMAG4.append(dataObj)
                        alist_KMAG4_BIN.append(dataObj)

            return True

        return False

    def KANA8_process(self, reading):
        global synch_sysdate
        global file_write_delay_sec
        global instrument_timestamp_enable

        if not synch_sysdate:
            return False

        str_data = reading
        str_data_clean = re.sub('\x00', '', str_data)

        if len(reading) > 0:
            dataObj = raw_data_struct()
            dataObj.utctime = self._timestamp()
            dataObj.raw_data = str_data_clean

            if instrument_timestamp_enable:
                current_time = datetime.datetime.now()
                str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                dataObj.raw_data = dataObj.raw_data + "," + "instr_timestamp=" + str_local_time

            alist_KANA8.append(dataObj)

            return True

        return False

    def laser_process(self, reading):
        global gga_timestamp
        global synch_sysdate
        global instrument_timestamp_enable
        #Eugene
        # global f_trigger
        # global last_trigger_time
        # global trigger_start_time



        if self.start_timer_Profile and self.ProfileView == ProfileViewState.PROFILE_VIEW_LASER:
            self.laser_profile_data(reading)

        if not synch_sysdate:
            return False

        # # Periodic trigger logic
        # current_time = time.time()
        # #print(f"Current Time: {current_time}, Last Trigger Time: {last_trigger_time}, Trigger Start Time: {trigger_start_time}, f_trigger: {f_trigger}")
        # if abs(current_time - last_trigger_time) >= 120:  # Every 2 minutes
        #     f_trigger = True
        #     trigger_start_time = current_time
        #     last_trigger_time = current_time  # Reset the trigger time
        #     print("Triggered")
        #
        # if f_trigger and (abs(current_time - trigger_start_time) >= 10):
        #     f_trigger = False  # Reset after 10 seconds
        #     #print(f"Current Time - Trigger Start: {current_time - trigger_start_time} (should be >= 10)")
        #     print("Reset Trigger")
        #
        # if f_trigger:
        #     reading = "999999"


            # ****  Raw Data Log *******************
        if len(reading) > 0:
            # print(reading)

            str_data = reading
            inst = self.instruments_config_array["LASER"]

            if inst.rawdata_log_enabled:
                if not inst.newFile:
                    current_time = datetime.datetime.now()
                    file_name = inst.name_instrument + current_time.strftime("_%Y-%m-%d %H_%M_%S") + ".log"

                    file_path = Logdirectory + file_name
                    print("CREATE LOG FILE: ", file_path)

                    inst.start_timer = time.time()

                    if os.path.isfile(file_path):
                        inst.newFile = open(file_path, "ab")
                    else:
                        inst.newFile = open(file_path, "wb")

                current_time = datetime.datetime.now()
                os_timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                temp_gga_timestamp = self.generate_timestamp(self.get_gga_timestamp(), 4, 0)

                record = ( f'os={os_timestamp} , gga={temp_gga_timestamp}, data={str_data}')

                inst.buffer.append(record + "\n")

                if abs(time.time() - inst.start_timer) > 2 * file_write_delay_sec:
                    inst.start_timer = time.time()

                if inst.newFile is not None and time.time() > inst.start_timer + file_write_delay_sec:
                    inst.start_timer = time.time()
                    inst.newFile.write("".join(inst.buffer).encode('utf-8'))
                    inst.newFile.flush()
                    inst.buffer.clear()



        if len(reading) > 0:

            if instrument_timestamp_enable:
                current_time = datetime.datetime.now()
                str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                reading = reading + "," + "instr_timestamp=" + str_local_time

            dataObj = raw_data_struct()
            dataObj.utctime = self.generate_timestamp(self.get_gga_timestamp(), 4, 0)
            dataObj.general_time =  dataObj.utctime
            dataObj.raw_data = reading

            alist_LASER.append(dataObj)
            return True

        return False

    def RA4500_process(self, delimitedMessage):
        global gga_timestamp
        global synch_sysdate
        global file_write_delay_sec
        global instrument_timestamp_enable

        # ****  Raw Data Log *******************
        if len(delimitedMessage) > 0:
            # print(reading)

            str_data = f"{' '.join(f'{byte:02x}' for byte in delimitedMessage)}\n"
            #print(str_data)
            inst = self.instruments_config_array["RA4500"]

            if inst.rawdata_log_enabled:
                if not inst.newFile:
                    current_time = datetime.datetime.now()
                    file_name = inst.name_instrument + current_time.strftime("_%Y-%m-%d %H_%M_%S") + ".log"

                    inst.start_timer = time.time()

                    file_path = Logdirectory + file_name
                    print("CREATE LOG FILE: ", file_path)

                    if os.path.isfile(file_path):
                        inst.newFile = open(file_path, "ab")
                    else:
                        inst.newFile = open(file_path, "wb")

                inst.buffer.append(str_data + "\n")

                if abs(time.time() - inst.start_timer) > 2 * file_write_delay_sec:
                    inst.start_timer = time.time()

                if inst.newFile is not None and time.time() > inst.start_timer + file_write_delay_sec:
                    inst.start_timer = time.time()
                    inst.newFile.write("".join(inst.buffer).encode('utf-8'))
                    inst.newFile.flush()
                    #print("".join(inst.buffer).encode('utf-8'))
                    inst.buffer.clear()

        #print(f"Data: {' '.join(f'{byte:02x}' for byte in delimitedMessage)}")

        # Calculate altitude in hex
        altitude_hex = ((delimitedMessage[3] & 0xFF) << 8) | (delimitedMessage[4] & 0xFF)

        # Check if altitude is negative (or out of valid range)
        if altitude_hex > 2500:
            altitude_hex = 0  # Convert to signed value or reset

        if self.start_timer_Profile and self.ProfileView == ProfileViewState.PROFILE_VIEW_RA4500:
            self.ra4500_profile_data(altitude_hex)

        statusByte = delimitedMessage[5]

        # Initialize status as a list to accumulate messages
        status = []

        # Bit 0 - Altitude
        if (statusByte & 0b00000001) != 0:
            status.append("Altitude Ascending")
        else:
            status.append("Altitude Descending")

        # Bit 1 - Self Test
        if (statusByte & 0b00000010) != 0:
            status.append("Self Test in progress")
        else:
            status.append("Normal operation")

        # Bit 2 - Status
        if (statusByte & 0b00000100) != 0:
            status.append("Unit Failure")
        else:
            status.append("Normal operation")

        # Bit 3 - Invalid
        if (statusByte & 0b00001000) != 0:
            status.append("Unlocked / Invalid output")
        else:
            status.append("Locked / Valid output")

        # Bit 4 - Strut
        if (statusByte & 0b00010000) != 0:
            status.append("De-asserted (In air)")
        else:
            status.append("Asserted (On ground)")

        # Convert altitude to a string with leading zeroes (4 digits)
        altitude_str = f"{altitude_hex:04d}"

        # Combine status messages into a string
        status_str = ", ".join(status) + ","

        # Convert altitude to a string with leading zeroes (4 digits)
        altitude_str = f"{altitude_hex:04d}"

        # Increment the message counter
        self.ra4500_msg_counter += 1
        formatted_counter = f"{self.ra4500_msg_counter:08d}"

        # Combine all components into the inData string
        data_RA4500 = f"{formatted_counter},{altitude_str},{', '.join(status)},"

        dataObj = raw_data_struct()
        dataObj.utctime = self.generate_timestamp(self.get_gga_timestamp(), 4, 0)
        dataObj.general_time = dataObj.utctime
        dataObj.raw_data = data_RA4500

        alist_RA4500.append(dataObj)

        return True

    def ADHAT_process(self, data_array):
        global last_adhat_timestamp
        global current_adhat_timestamp
        global adhat_rec_per_100ms
        global synch_sysdate
        global last_gga_time
        global file_write_delay_sec
        global instrument_timestamp_enable
        global counter_ADHAT
        global qtfm_semaphore
        global utc_hour_diff

        if self.start_timer_Profile and self.ProfileView == ProfileViewState.PROFILE_VIEW_ADHAT:
            self.adhat_profile_data(data_array)

        current_time = datetime.datetime.now()

            # ****  Raw Data Log *******************
        if len(data_array) > 0:
            inst = self.instruments_config_array["ADHAT"]

            if inst.rawdata_log_enabled:
                if not inst.newFile:
                    file_name = inst.name_instrument + current_time.strftime("_%Y-%m-%d %H_%M_%S") + ".log"

                    file_path = Logdirectory + file_name
                    print("CREATE LOG FILE: ", file_path)

                    inst.start_timer = time.time()

                    if os.path.isfile(file_path):
                        inst.newFile = open(file_path, "ab")
                    else:
                        inst.newFile = open(file_path, "wb")

                timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                for channel in range(0, 5):
                    if data_array[channel] != 0:
                        str_data = ("Channel " + str(channel + 1) + "," + f'{timestamp}, {data_array[channel]}')
                        inst.buffer.append(str_data + "\n")

                if abs(time.time() - inst.start_timer) > 2 * file_write_delay_sec:
                    inst.start_timer = time.time()

                if inst.newFile is not None and time.time() > inst.start_timer + file_write_delay_sec:
                    inst.start_timer = time.time()
                    inst.newFile.write("".join(inst.buffer).encode('utf-8'))
                    inst.newFile.flush()
                    inst.buffer.clear()

            if not synch_sysdate or not qtfm_semaphore:
                return False

        # Initialize ADHAT timestamps using GNSS reference
        if last_adhat_timestamp == 0:
            tmp_gga_timestamp = float(self.get_gga_timestamp())
            last_adhat_time = datetime.datetime.fromtimestamp(tmp_gga_timestamp).replace(
                minute=current_time.minute,
                second=current_time.second,
                microsecond=current_time.microsecond
            )
            last_adhat_timestamp = last_adhat_time.timestamp()
            current_adhat_timestamp = last_adhat_timestamp

            utc_hour_diff = abs(last_adhat_time.hour - current_time.hour)

            if (utc_hour_diff > 12):
                utc_hour_diff = 24 - utc_hour_diff

            print("UTC Hour Diff: ", utc_hour_diff)

            #print("ADHAT Timestamp: ", self.generate_timestamp(last_adhat_timestamp, 2, 0))
            #print("Local Time: ", current_time.strftime("%H:%M:%S.%f")[:-3])

        if len(data_array) > 0:
            adhat_line = ""
            for channel in range(0, 5):
                adhat_line += str(data_array[channel]) + ","

            if counter_ADHAT >= adhat_rec_per_100ms:
                counter_ADHAT = 0
                last_adhat_timestamp = round(last_adhat_timestamp + 0.1, 2)

            dataObj = raw_data_struct()
            dataObj.utctime = self.generate_timestamp(last_adhat_timestamp, 2, 0)
            adhat_time_step = 0.02

            str_crnt_adhat_timestamp = self.generate_timestamp(current_adhat_timestamp, 4, 0)
            dataObj.general_time = str_crnt_adhat_timestamp

            current_time = datetime.datetime.now()
            current_time_timestamp = current_time.timestamp()

            if current_time_timestamp - (
                    current_adhat_timestamp - datetime.timedelta(hours=utc_hour_diff).total_seconds()) > 0.1:
                #print("ADHAT Timestamp: ", dataObj.utctime)
                #print("Local Time: ", current_time.strftime("%H:%M:%S.%f")[:-3])
                current_adhat_timestamp = round(current_adhat_timestamp + 0.1, 3)
                last_adhat_timestamp = round(last_adhat_timestamp + 0.1, 2)
            elif (last_adhat_timestamp - datetime.timedelta(
                    hours=utc_hour_diff).total_seconds() - current_adhat_timestamp) > 0.1:
                #print("ADHAT Timestamp: ", dataObj.utctime)
                #print("Local Time: ", current_time.strftime("%H:%M:%S.%f")[:-3])
                current_adhat_timestamp = round(current_adhat_timestamp - 0.1, 3)
                last_adhat_timestamp = round(last_adhat_timestamp - 0.1, 2)


            dataObj.raw_data = str_crnt_adhat_timestamp + "," + adhat_line

            if instrument_timestamp_enable:
                current_time = datetime.datetime.now()
                str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                dataObj.raw_data = dataObj.raw_data + "," + "instr_timestamp=" + str_local_time

            alist_ADHAT.append(dataObj)
            counter_ADHAT = counter_ADHAT + 1
            current_adhat_timestamp = round(current_adhat_timestamp + adhat_time_step, 3)

            return True

        return False

    def gps_process(self, reading):
        global gga_timestamp
        global gps_date
        global synch_sysdate
        global last_gga_time
        global gga_utc_time
        global gps_day
        global gps_month
        global gps_year
        global gps_hour
        global gps_minute
        global gps_second
        global gps_microsecond
        global file_write_delay_sec
        global Logdirectory
        global gps_antenna_on
        global instrument_timestamp_enable
        global f_gpsTimeUnSynch   # GPS Time UnSynchronized

        if len(reading) > 0:
            #print(reading)
            inst = self.instruments_config_array["GPS"]
            str_data = reading

            if self.start_timer_Profile and self.ProfileView == ProfileViewState.PROFILE_VIEW_GPS and reading.find(
                    "GGA") != -1 and gps_antenna_on:
                self.gps_profile_data(reading)

            if self.connection_state == ConnectionState.YELLOW and synch_sysdate:
                self.ui.label_Status.setStyleSheet("background-color: green;")
                self.connection_state = ConnectionState.GREEN

            # ****  Raw Data Log *******************
            if inst.rawdata_log_enabled:
                if not inst.newFile:
                    current_time = datetime.datetime.now()
                    file_name = inst.name_instrument + current_time.strftime("_%Y-%m-%d %H_%M_%S") + ".log"

                    file_path = Logdirectory + file_name
                    print("CREATE LOG FILE: ", file_path)

                    inst.start_timer = time.time()

                    if os.path.isfile(file_path):
                        inst.newFile = open(file_path, "ab")
                    else:
                        inst.newFile = open(file_path, "wb")

                current_time = datetime.datetime.now()
                os_timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")

                record = (f'os={os_timestamp}, data={str_data}')

                inst.buffer.append(record + "\n")

                if abs(time.time() - inst.start_timer) > 2 * file_write_delay_sec:
                    inst.start_timer = time.time()

                if inst.newFile is not None and time.time() > inst.start_timer + file_write_delay_sec:
                    inst.start_timer = time.time()
                    inst.newFile.write("".join(inst.buffer).encode('utf-8'))
                    inst.newFile.flush()
                    inst.buffer.clear()

            # **************************************
            gps_parts = str_data.split("\n")

            for gps_line in gps_parts:
                # print(gps_line)
                gga_index = gps_line.find("GGA")
                if gga_index != -1:
                    gga_data = gps_line.split(',')
                    if len(gga_data) > 10:

                        gga_utc_time = gga_data[1]

                        if gga_utc_time == "":
                            self.ui.label_Error.setText(
                                QCoreApplication.translate("DataLogger_Profile",
                                                           u"GPS WITHOUT ANTENNA\nNO CSV FILE GENERATION", None))
                            gps_antenna_on = False
                            return

                        gga_lat = gga_data[3]

                        # gga:longitude
                        gga_lon = gga_data[5]

                        if gga_lat == "" or gga_lon == "":
                            self.ui.label_Error.setText(
                                QCoreApplication.translate("DataLogger_Profile",
                                                           u"GPS WITHOUT ANTENNA\nNO CSV FILE GENERATION", None))
                            gps_antenna_on = False
                            return

                        gps_hour = gga_utc_time[0] + gga_utc_time[1]
                        gps_minute = gga_utc_time[2] + gga_utc_time[3]
                        gps_second = gga_utc_time[4] + gga_utc_time[5]
                        gps_microsecond = gga_utc_time[7] + gga_utc_time[8]

                        gps_hour_int = int(gps_hour)
                        gps_minute_int = int(gps_minute)
                        gps_second_int = int(gps_second)

                        # Get the current OS time
                        os_time = datetime.datetime.now(datetime.UTC)
                        os_hour = os_time.hour
                        os_minute = os_time.minute
                        os_second = os_time.second

                        # Calculate absolute difference in seconds
                        time_difference = abs((gps_hour_int * 3600 + gps_minute_int * 60 + gps_second_int) -
                                              (os_hour * 3600 + os_minute * 60 + os_second))

                        # Set flag if the difference exceeds 2 seconds
                        f_gpsTimeUnSynch = time_difference > 3

                        if f_gpsTimeUnSynch and  synch_sysdate:
                            #print("GPS Time UnSynchronized: ", time_difference)
                            f_gpsTimeUnSynch = False
                            inst.serial.port_reset = True
                            return

                        try:
                            utc_Time_GPS = round(float(gga_utc_time), 2)
                        except ValueError:
                            print(f"GPS Data Error: {gga_utc_time}")
                            return
                            
                        if (utc_Time_GPS - last_gga_time) > 0.15 and last_gga_time != 0:
                            dataObj = raw_data_struct()
                            dataObj.utctime = str(last_gga_time + 0.1)
                            dataObj.raw_data = gps_line

                            if instrument_timestamp_enable:
                                current_time = datetime.datetime.now()
                                str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                                dataObj.raw_data = dataObj.raw_data + "," + "instr_timestamp=" + str_local_time

                            alist_GPS.append(dataObj)

                        # if (utc_Time_GPS - last_gga_time) > 1 and last_gga_time != 0:
                        #     print("Source GPS utc_Time_GPS:", str(utc_Time_GPS))
                        #     print("Source GPS last_gga_time:", str(last_gga_time))

                        last_gga_time = utc_Time_GPS

                        dataObj = raw_data_struct()
                        dataObj.utctime = last_gga_time
                        dataObj.raw_data = gps_line

                        if instrument_timestamp_enable:
                            current_time = datetime.datetime.now()
                            str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                            dataObj.raw_data = dataObj.raw_data + "," + "instr_timestamp=" + str_local_time

                        alist_GPS.append(dataObj)

                        # print(gga_timestamp)
                        if (synch_sysdate == True and int(gps_year) > 2020):
                            # datetime(year, month, day, hour, minute, second, microsecond)
                            # dt = datetime.datetime(2017, 11, 28, 23, 55, 59, 342380)
                            dt = datetime.datetime(int(gps_year), int(gps_month), int(gps_day), int(gps_hour),
                                                   int(gps_minute),
                                                   int(gps_second), int(gps_microsecond))

                            self.set_gga_timestamp(round(dt.timestamp() + float(int(gps_microsecond) / 100), 2))

                if gps_line.find("ZDA") != -1:
                    zda_data = gps_line.split(',')
                    # FIX BAD ZDA: $GNZDA,174122.10,24,00,00*7F
                    # CORRECT ZDA: $GNZDA,155034.30,22,10,2024,00,00*78
                    if len(zda_data) == 5:
                        current_time = datetime.datetime.now()
                        str_local_date = current_time.strftime(",%d,%m,%Y,")
                        gps_line = zda_data[0] + "," + zda_data[1] + str_local_date + "00,00*7F"
                        zda_data = gps_line.split(',')

                    if len(zda_data) > 5:
                        gga_utc_time = zda_data[1]
                        gps_day = zda_data[2]
                        gps_month = zda_data[3]
                        gps_year = zda_data[4]

                        if zda_data[1] == "":
                            self.ui.label_Error.setText(
                                QCoreApplication.translate("DataLogger_Profile",
                                                           u"GPS WITHOUT ANTENNA\nNO CSV FILE GENERATION", None))

                            gps_antenna_on = False
                            return

                        gps_hour = gga_utc_time[0] + gga_utc_time[1]
                        gps_minute = gga_utc_time[2] + gga_utc_time[3]
                        gps_second = gga_utc_time[4] + gga_utc_time[5]
                        gps_microsecond = gga_utc_time[7] + gga_utc_time[8]

                        if (synch_sysdate == False and int(gps_year) > 2020):
                            gps_date = "\'" + gps_year + "-" + gps_month + "-" + gps_day + " " + \
                                       gps_hour + ":" + gps_minute + ":" + gps_second + "\'"
                            print("Set system date: ", gps_date)
                            if platform != "win32":
                                os.system('sudo date -s %s' % gps_date)
                            synch_sysdate = True
                            dt = datetime.datetime(int(gps_year), int(gps_month), int(gps_day), int(gps_hour),
                                                   int(gps_minute),
                                                   int(gps_second), int(gps_microsecond))
                            self.set_gga_timestamp(round(dt.timestamp() + float(int(gps_microsecond) / 100), 2))

                if (synch_sysdate == True and int(gps_year) > 2020):
                    # datetime(year, month, day, hour, minute, second, microsecond)
                    # dt = datetime.datetime(2017, 11, 28, 23, 55, 59, 342380)
                    dt = datetime.datetime(int(gps_year), int(gps_month), int(gps_day), int(gps_hour), int(gps_minute),
                                           int(gps_second), int(gps_microsecond))

                    #gga_timestamp = round(dt.timestamp() + float(int(gps_microsecond) / 100), 2)

                    self.set_gga_timestamp(round(dt.timestamp() + float(int(gps_microsecond) / 100), 2))

                    # print("DT=", str(gga_timestamp))

            # $GNGGA, 174616.60, 4350.00102, N, 07918.61949, W, 1, 12, 0.54, 209.3, M, -36.0, M,, *72
            # $GNZDA, 174616.60, 29, 07, 2021, 00, 00 * 70
            # sudo date --set '2020-12-31 20:45:00'

    def set_gga_timestamp(self, value):
        global gga_timestamp
        gga_timestamp = value

    def get_gga_timestamp(self):
        global gga_timestamp
        return gga_timestamp

    def qtfm_process(self, reading):
        global qtfm_semaphore
        global last_qtfm_timestamp
        global current_qtfm_timestamp
        global synch_sysdate
        global gga_timestamp
        global qtfm_q_fid_counter
        global quspinVersion
        global counter_QTFM
        global qtfm_NoneDataFlag
        global quspin_speed_detect_flag
        global quspin_speed_detect_counter
        global quspin_speed_detect_value
        global quspin_speed_last_sq_num
        global last_sq_number
        global file_write_delay_sec
        global Logdirectory
        global instrument_timestamp_enable

        sq_number = 0

        if self.start_timer_Profile and (self.ProfileView == ProfileViewState.PROFILE_VIEW_MAG or
                                         self.ProfileView == ProfileViewState.PROFILE_VIEW_ORTHO):
            self.quspin_profile_data(reading)

        if not synch_sysdate:
            qtfm_q_fid_counter = 0
            qtfm_semaphore = False
            return False

        inst = self.instruments_config_array["QTFM_V2"]

        if quspinVersion == "2":
            qtfm_line_len = 39

        else:
            qtfm_line_len = 15

        if len(reading) > 0:

            #print(reading)

            str_data = reading

            # ****  Raw Data Log *******************
            if inst.rawdata_log_enabled:
                if not inst.newFile:
                    current_time = datetime.datetime.now()
                    file_name = inst.name_instrument + current_time.strftime("_%Y-%m-%d %H_%M_%S") + ".log"

                    file_path = Logdirectory + file_name
                    print("CREATE LOG FILE: ", file_path)

                    if os.path.isfile(file_path):
                        inst.newFile = open(file_path, "ab")
                    else:
                        inst.newFile = open(file_path, "wb")

                current_time = datetime.datetime.now()
                str_data = current_time.strftime("%H:%M:%S.%f")[:-3] + ": " + str_data
                inst.buffer.append(str_data + "\n")

                if abs(time.time() - inst.start_timer) > 2 * file_write_delay_sec:
                    inst.start_timer = time.time()

                if inst.newFile is not None and time.time() > inst.start_timer + file_write_delay_sec:
                    inst.start_timer = time.time()
                    inst.newFile.write("".join(inst.buffer).encode('utf-8'))
                    inst.newFile.flush()
                    inst.buffer.clear()

            qtfm_parts = str_data.split("\n")

            counter = 0

            for qtfm_line in qtfm_parts:

                if "nan" in qtfm_line:
                    qtfm_line_len = 30
                    if qtfm_NoneDataFlag == False:
                        print("Warning: Quspin No Data: " + qtfm_line)
                        qtfm_NoneDataFlag = True
                else:
                    if qtfm_NoneDataFlag == True:
                        qtfm_NoneDataFlag = False

                ###### Check sequence number ##################

                if ("#POF" in qtfm_line) == True:
                    continue

                if (">" in qtfm_line) == False:
                    print(" No > in = : " + qtfm_line)
                    continue

                char_sq_end = "s"
                if ("s" in qtfm_line) == False:
                    if ("v" in qtfm_line) == False:

                        print(" No s and v in = : " + qtfm_line)
                        continue
                    else:
                        char_sq_end = "v"

                index_sq_begin = qtfm_line.index(">") + 1
                index_sq_end = qtfm_line.index(char_sq_end)

                if (index_sq_begin > index_sq_end):
                    print(" Wrong data = : " + qtfm_line)
                    continue

                st_sq_number = qtfm_line[index_sq_begin:index_sq_end]

                try:
                    sq_number = round(float(st_sq_number), 2)
                except Exception as e:
                    current_time = datetime.datetime.now()
                    str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                    print(str_local_time + " Error Data = :  (" + str(e) + " )")

                if quspin_speed_last_sq_num == 0:
                    quspin_speed_last_sq_num = sq_number
                    return

                # Detect quspin speed value
                if quspin_speed_detect_flag is False:

                    if quspin_speed_detect_counter == 0:
                        quspin_speed_detect_value = sq_number - quspin_speed_last_sq_num
                        quspin_speed_last_sq_num = sq_number
                        quspin_speed_detect_counter += 1
                        return
                    else:
                        if quspin_speed_detect_value == sq_number - quspin_speed_last_sq_num:
                            quspin_speed_detect_counter += 1
                            quspin_speed_last_sq_num = sq_number
                        else:
                            quspin_speed_detect_counter == 0
                            quspin_speed_last_sq_num = 0

                    if quspin_speed_detect_counter > 5:
                        quspin_speed_detect_flag = True
                        self.set_serial_interval(quspin_speed_detect_value)
                        self.CurrentDataRate = quspin_speed_detect_value
                        print("Detect quspin data rate: " + str(quspin_speed_detect_value))

                    return

                else:
                    quspin_rec_per_100ms = int(float(100 / quspin_speed_detect_value))

                if ((len(alist_QTFM) > 100) and (last_sq_number != 0) and
                        ((sq_number - last_sq_number) != quspin_speed_detect_value)):
                    current_time = datetime.datetime.now()
                    str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                    print(str_local_time + " Lost sequence = : " + qtfm_line)
                    inst.serial.port_reset = True  #Eugene

                last_sq_number = sq_number

                #############################################################################

                if qtfm_semaphore == False:

                    if self.message_timer == 0:
                        self.message_timer = time.time()

                    self.message_count = self.message_count + 1

                    if (abs(time.time() - self.message_timer) > 2 * file_write_delay_sec):
                        self.message_timer = time.time()
                        self.message_count = 0

                    if time.time() > self.message_timer + 1:

                        if self.message_count > int(1000 / quspin_speed_detect_value) + 20:
                            inst.serial.port_reset = True
                        else:
                            qtfm_semaphore = True

                        # print("Quspin msg count: " + str(self.message_count))
                        self.message_count = 0
                        self.message_timer = time.time()
                    return False

                if (last_qtfm_timestamp == 0):
                    # last_qtfm_timestamp = round(float(gga_timestamp), 2)
                    current_time = datetime.datetime.now()

                    # Convert the GGA timestamp to a datetime object
                    tmp_gga_timestamp = float(self.get_gga_timestamp())
                    last_qtfm_time = datetime.datetime.fromtimestamp(tmp_gga_timestamp)

                    # Replace minute, second, and microsecond Eugene
                    last_qtfm_time = last_qtfm_time.replace(
                         minute=current_time.minute,
                         second=current_time.second,
                         microsecond=current_time.microsecond)

                    last_qtfm_timestamp = last_qtfm_time.timestamp()
                    current_qtfm_timestamp = last_qtfm_timestamp
                    #print("Quspin Timestamp: ", self.generate_timestamp(last_qtfm_timestamp, 2, 0))
                    #print("Local Time: ", current_time.strftime("%H:%M:%S.%f")[:-3])

                #############################################################################

                prefix = qtfm_line.find('!')
                index = qtfm_line.find('@')

                if prefix != -1:
                    if index != -1:
                        qtfm_line = qtfm_line.replace('@', ',')
                    else:
                        qtfm_line = qtfm_line + ","

                    qtfm_line = qtfm_line.replace('!', '')
                    qtfm_line = qtfm_line.replace('nan', '')

                    qtfm_line = qtfm_line.replace('\r', '')
                    qtfm_line = qtfm_line.replace('\n', '')

                    qtfm_q_fid_counter = int(qtfm_q_fid_counter + 1)
                    qtfm_line = str(qtfm_q_fid_counter) + "," + qtfm_line

                    if counter_QTFM >= quspin_rec_per_100ms:
                        counter_QTFM = 0
                        last_qtfm_timestamp = round(last_qtfm_timestamp + 0.1, 2)

                    dataObj = raw_data_struct()
                    # dataObj.utctime = generate_timestamp(last_qtfm_timestamp, 5, random.uniform(0.00001, 0.00009))
                    dataObj.utctime = self.generate_timestamp(last_qtfm_timestamp, 2, 0)
                    quspin_time_step = quspin_speed_detect_value / 1000
                    current_qtfm_timestamp = round(current_qtfm_timestamp + quspin_time_step, 3)
                    str_crnt_qtfm_timestamp = self.generate_timestamp(current_qtfm_timestamp, 4, 0)

                    dataObj.general_time = str_crnt_qtfm_timestamp
                    dataObj.raw_data = str_crnt_qtfm_timestamp + "," + qtfm_line

                    if instrument_timestamp_enable:
                        current_time = datetime.datetime.now()
                        str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                        dataObj.raw_data = dataObj.raw_data + "," + "instr_timestamp=" + str_local_time

                    #print("utctime: " + dataObj.utctime + " data: " + dataObj.raw_data)
                    alist_QTFM.append(dataObj)
                    if quspinVersion == "2":
                        # current_time = datetime.datetime.now()
                        # str_local_time = current_time.strftime("%H%M%S.%f")
                        # dataObj.utctime = generate_timestamp(float(str_local_time), 2, 0)
                        # dataObj.utctime = str_local_time
                        alist_QTFM_BIN.append(dataObj)
                    counter_QTFM = counter_QTFM + 1

                    # print(dataObj.utctime + "," + dataObj.raw_data)

                    # if (abs(last_qtfm_timestamp - gga_timestamp) > 2):
                    #     print("Debug 1 QTFM: ", last_qtfm_timestamp)
                    #     print("Debug 1 GPS : ", gga_timestamp)
                    #     last_qtfm_timestamp = gga_timestamp

    def closeEvent(self, event):
        global file_write_delay_sec
        global shutdown_process

        #self.msg_box = openMsgBox(self)

        file_write_delay_sec = 0
        shutdown_process = True
        for name, inst in self.instruments_config_array.items():
            if inst.serial is not None:
                inst.serial.stop()
                #inst.serial.wait() #Eugene

        self.dataLogger_proc.stop()
        self.dataLogger_proc.wait()

        # if inst.newFile is not None:
        #     inst.newFile.close()
        #     inst.newFile = None

        if self.quspin_chart_timer:
            self.quspin_chart_timer.stop()

        if self.adhat_chart_timer:
            self.adhat_chart_timer.stop()

        if self.dataOutput_timer:
            self.dataOutput_timer.stop()

        #if self.program_msg_q_timer:
        #self.program_msg_q_timer.stop()

        event.accept()

    def DataOutput_Process(self):
        global gps_day
        global gps_month
        global gps_year
        global gps_hour
        global gps_minute
        global last_bz2_utc_time
        global last_bz2_file_time
        global synch_sysdate
        global bz_buffer
        global dataOutput
        global instrument_timestamp_enable

        if not synch_sysdate:
            return False

        if not dataOutput.enabled:
            return False

        # example file name "2022-08-31T22-08-43UTC.base5200.mag_a.bin"

        if (dataOutput.file_change and (time.time() < last_bz2_file_time + 300)):
            return False

        if (dataOutput.file_change or dataOutput.newFile == 0):
            # file_name = gps_year + "-" + gps_month + "-" + gps_day + "T" + \
            #             gps_hour + "-" + gps_minute + "-" + gps_second + "UTC" + dataOutput.file_ext

            current_time = datetime.datetime.now()
            str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]

            file_name = current_time.strftime("%Y-%m-%dT%H-%M-%S") + "UTC" + dataOutput.file_ext + ".bz2"

            if platform == "win32":
                bz2_dir = "bz2\\"
            else:
                bz2_dir = Logdirectory + "bz2//"

            if not os.path.isdir(bz2_dir):
                os.mkdir(bz2_dir)

            file_path = bz2_dir + file_name

            if os.path.isfile(file_path):
                for index in range(100):
                    file_path = file_path + "_" + str(index + 1)
                    if not os.path.isfile(file_path):
                        break

            dataOutput.file_name = file_path

            dataOutput.newFile = bz2.BZ2File(file_path, "wb")

            dataOutput.file_change = False

            dataOutput.file_size = 0

            last_bz2_file_time = time.time()

            alist_QTFM_BIN.clear()
            alist_KMAG4_BIN.clear()

            print("Create bz2 file: " + file_path)

        ############ KMAG4 ##################################
        while len(alist_KMAG4_BIN) > 0:
            data_KMAG4 = alist_KMAG4_BIN[0]

            KMAG4data = data_KMAG4.raw_data

            # print(KMAG4data)

            resultData = ""

            # ######  KMAG4 #######
            # $KMAG4,298944020,194227.00,298944000,049732498,049732479,049732450,049732507,-025695,
            # +406543,-042956,+130428,+000003,-000002,+000013,-037287
            if len(KMAG4data) > 0 and KMAG4data.startswith('$KMAG4'):

                st_KMAG4 = KMAG4data.split(",")

                if len(st_KMAG4) > 7:

                    # :kmag4:utc_time
                    str_utc_time = st_KMAG4[2]

                    if ('000000' in str_utc_time) or (str_utc_time == ""):
                        del alist_KMAG4_BIN[0]
                        continue

                    else:

                        try:
                            utc_time = round(float(str_utc_time), 2)
                        except Exception as e:
                            current_time = datetime.datetime.now()
                            str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                            print(str_local_time + " Error Data = : " + str_utc_time + " (" + str(e) + " )")
                            del alist_KMAG4_BIN[0]
                            continue

                        # check data every 1 sec only
                        if (utc_time == 0) or (
                                utc_time % 1 > 0):  # should be not 000000000 or 194227.20, should be 194227.00
                            del alist_KMAG4_BIN[0]
                            continue

                    # print(str(utc_time))

                    # :kmag4:mag_a
                    if dataOutput.name_kmag4_channel == "mag_a":
                        resultData = st_KMAG4[4]
                    # :kmag4:mag_b
                    elif dataOutput.name_kmag4_channel == "mag_b":
                        resultData = st_KMAG4[5] + ","
                    # :kmag4:mag_c
                    elif dataOutput.name_kmag4_channel == "mag_c":
                        resultData = st_KMAG4[6] + ","
                    # :kmag4:mag_d
                    elif dataOutput.name_kmag4_channel == "mag_d":
                        resultData = st_KMAG4[7] + ","

            if len(resultData) > 0:

                if resultData[0] == '0':
                    resultData = resultData[1:]

                resultData = resultData[:5] + '.' + resultData[5:]
                mag_data = float(resultData)
                bin_data = struct.pack('f', mag_data)
                bz_buffer.append(bin_data)
                # dataOutput.newFile.write(bin_data)
                # dataOutput.newFile.flush()

                dataOutput.file_size += len(bin_data)

                if (dataOutput.file_size >= 1200):
                    dataOutput.file_change = True
                    dataOutput.newFile.write(b"".join(bz_buffer))
                    dataOutput.newFile.close()
                    # os.rename(dataOutput.file_name, dataOutput.file_name + ".bz2")
                    bz_buffer.clear()

                    return
                    # ofile = bz2.BZ2File("BinaryData", "wb")
                    # ofile.write(data)
                    # ofile.close()

            del alist_KMAG4_BIN[0]

        ############ QTFM GEN 2 ##################################
        while len(alist_QTFM_BIN) > 0:
            data_QTFM_BIN = alist_QTFM_BIN[0]

            QTFM_BINdata = data_QTFM_BIN.raw_data

            # print(QTFM_BINdata)

            resultData = ""

            # ######  QTFM_BIN #######
            # !23215.267_X-21148.606=@117>261249172s027v013

            if len(QTFM_BINdata) > 0:

                valid_mag = False
                if "_" in QTFM_BINdata:

                    valid_mag = True
                    QTFM_BINdata = QTFM_BINdata.replace("_", ",")

                elif "*" in QTFM_BINdata:

                    valid_mag = False
                    QTFM_BINdata = QTFM_BINdata.replace("*", ",")

                st_QTFM_BIN = QTFM_BINdata.split(",")

                if len(st_QTFM_BIN) > 2:
                    # :qtfm:utc_time
                    str_utc_time = data_QTFM_BIN.utctime

                    try:
                        utc_time = round(float(str_utc_time), 2)
                    except Exception as e:
                        current_time = datetime.datetime.now()
                        str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                        print(
                            str_local_time + " DataOutput_Process Error Data (str_utc_time) = : " + str_utc_time + " (" + str(
                                e) + " )")
                        del alist_QTFM_BIN[0]
                        continue

                    # check data every 1 sec only
                    if utc_time % 1 > 0.1:  # should be not 000000000 or 194227.20, should be 194227.00
                        del alist_QTFM_BIN[0]
                        utc_time == last_bz2_utc_time
                        continue

                    # check data every 1 sec only
                    if utc_time == last_bz2_utc_time:  # should be not 000000000 or 194227.20, should be 194227.00
                        del alist_QTFM_BIN[0]
                        utc_time == last_bz2_utc_time
                        continue

                    # qtfm: q_mag
                    resultData = st_QTFM_BIN[2]
                    last_bz2_utc_time = utc_time
                    # print("Record bz2 = : " + str_utc_time)

            if len(resultData) > 0:

                if resultData[0] == '0':
                    resultData = resultData[1:]

                # resultData = resultData[:5] + '.' + resultData[5:]

                try:
                    mag_data = float(resultData)
                except Exception as e:
                    current_time = datetime.datetime.now()
                    str_local_time = current_time.strftime("%H:%M:%S.%f")[:-3]
                    print(str_local_time + " DataOutput_Process Error Data (mag_data) = : " + str_utc_time + " (" + str(
                        e) + " )")
                    del alist_QTFM_BIN[0]
                    continue
                bin_data = struct.pack('f', mag_data)
                bz_buffer.append(bin_data)
                # dataOutput.newFile.write(bin_data)
                # dataOutput.newFile.flush()

                dataOutput.file_size += len(bin_data)

                if (dataOutput.file_size >= 1200):
                    dataOutput.file_change = True
                    dataOutput.newFile.write(b"".join(bz_buffer))
                    dataOutput.newFile.close()
                    bz_buffer.clear()
                    # os.rename(dataOutput.file_name, dataOutput.file_name + ".bz2")
                    # alist_QTFM_BIN.clear()
                    return
                    # ofile = bz2.BZ2File("BinaryData", "wb")
                    # ofile.write(data)c
                    # ofile.close()

            del alist_QTFM_BIN[0]

    class DataLogger_Process(QThread):

        def __init__(self):
            super().__init__()
            self.running = True
            self.dataLoggingBuffer = []
            self.dataLoggingFile = None
            self.os_time_change = False
            self.start_timer = None

        def run(self):

            while self.running:
                self.processDataLogging()

        def stop(self):
            self.running = False
            process_flag = True
            while len(alist_GPS) > 0 and process_flag:
                process_flag = self.processDataLogging()

            if len(self.dataLoggingBuffer) > 0:
                self.dataLoggingFile.flush()
                self.dataLoggingFile.write("".join(self.dataLoggingBuffer).encode('utf-8'))
                self.dataLoggingBuffer.clear()
                self.dataLoggingFile.flush()

            if self.dataLoggingFile:
                self.dataLoggingFile.close()

            self.wait()
            print("Stop Datalogger process")

        # def generate_timestamp(self, t=gga_timestamp, prec=2, add_time=0):
        #     s = time.strftime("%H%M%S", time.localtime(t + add_time))
        #     if prec > 0:
        #         s += ("%.9f" % ((t + add_time) % 1,))[1:2 + prec]
        #
        #         f = round(float(s), prec - 1)
        #
        #     return str(f)

        def generate_timestamp(self, base_timestamp, step, increment):
            # Calculate the new timestamp based on the base timestamp and the increment
            new_timestamp = base_timestamp + (step * increment)
            # Format the timestamp to the desired precision
            formatted_timestamp = time.strftime("%H%M%S", time.localtime(new_timestamp))
            if increment > 0:
                formatted_timestamp += f".{int((new_timestamp % 1) * 10 ** increment):0{increment}d}"
            return formatted_timestamp

        def processDataLogging(self):
            global synch_sysdate
            global sDataLogHeaderGPS
            global sDataLogHeaderQTFM
            global sDataLogHeaderKana8
            global sDataLogHeaderLaser
            global sDataLogHeaderRA4500
            global sDataLogHeaderADHAT
            global file_write_delay_sec
            global shutdown_process

            global last_valid_gps_value #Eugene

            data_size = 300

            last_GPS = ""
            last_KANA8 = ""
            last_KMAG4 = ""
            last_LASER = ""
            last_RA4500 = ""
            last_ADHAT = ""
            last_QTFM = ""

            if not isEnable_GPS or not isEnable_QTFM:
                return False

            if not synch_sysdate and shutdown_process is False:
                return False

            if synch_sysdate and not self.dataLoggingFile:
                current_time = datetime.datetime.now()
                file_name = "DataLogger" + current_time.strftime("_%Y-%m-%d %H_%M_%S") + ".csv"

                file_path = Logdirectory + file_name
                print("CREATE LOG FILE: ", file_path)

                self.start_timer = time.time()

                if os.path.isfile(file_path):

                    for i in range(1000):
                        temp_file_path = file_path + "_" + str(i + 1)

                        if not os.path.isfile(temp_file_path):
                            file_path = temp_file_path
                            break

                # print("PATH", file_path)

                self.dataLoggingFile = open(file_path, "wb")

                title = "count,date,time,"

                instr_time = ""
                instr_kmag4_label = ""
                instr_gga_label = ""
                instr_ra4500_label = ""
                instr_laser_label = ""
                instr_adhat_label = ""
                instr_qtfm_label = ""
                if instrument_timestamp_enable:
                    instr_time = "instr_time,"
                    instr_kmag4_label = ":kmag4:"
                    instr_gga_label = ":gga:"
                    instr_ra4500_label = ":ra4500:"
                    instr_laser_label = ":laser:"
                    instr_adhat_label = ":adhat:"
                    instr_qtfm_label = ":qtfm:"

                if isEnable_GPS:
                    sDataLogHeaderGPS = instr_gga_label + instr_time + dataLogHeaderGPS

                if isEnable_QTFM:

                    last_QTFM = default_QTFM
                    if quspinVersion == "2":
                        sDataLogHeaderQTFM = instr_qtfm_label + instr_time + dataLogQuspinHeaderV2
                    else:
                        sDataLogHeaderQTFM = instr_qtfm_label + instr_time + dataLogQuspinHeaderV1

                if isEnable_KMAG4:
                    sDataLogHeaderKana8 = instr_kmag4_label + instr_time + dataLogHeaderKMAG4

                if isEnable_LASER:
                    sDataLogHeaderLaser = instr_laser_label + instr_time + dataLogHeaderLaser

                if isEnable_RA4500:
                    sDataLogHeaderRA4500 = instr_ra4500_label + instr_time + dataLogHeaderRA4500

                if isEnable_ADHAT:
                    sDataLogHeaderADHAT = instr_adhat_label + instr_time + dataLogHeaderADHAT

                title = (title + sDataLogHeaderKana8 + sDataLogHeaderQTFM + sDataLogHeaderLaser +
                         sDataLogHeaderRA4500 + sDataLogHeaderADHAT + sDataLogHeaderGPS + "\r\n")

                self.dataLoggingFile.write(bytes(title, 'utf-8'))
                self.dataLoggingFile.flush()

            if (abs(time.time() - self.start_timer) > 2 * file_write_delay_sec) and (
                    self.os_time_change is False):
                self.start_timer = time.time()
                self.os_time_change = True
                #print("Change timer: " + str(self.start_timer))

                #print("GPS Timestamp: ", self.generate_timestamp(round(float(gga_timestamp), 2), 2, 0))
                #current_time = datetime.datetime.now()
                #print("Local Time: ", current_time.strftime("%H:%M:%S"))

            if isEnable_GPS and len(alist_GPS) < data_size and shutdown_process is False:
                sleep(0.9)
                return False

            gps_index = 0

            while gps_index < len(alist_GPS):
                gps_dataObj = alist_GPS[gps_index]

                if isEnable_ADHAT and len(alist_ADHAT) < data_size and shutdown_process is False:
                    sleep(0.2)
                    return False

                if isEnable_QTFM and len(alist_QTFM) < data_size and shutdown_process is False:
                    sleep(0.4)
                    return False

                if isEnable_QTFM and len(alist_QTFM) == 0 and shutdown_process is True:
                    alist_GPS.clear()
                    return False

                if isEnable_KMAG4 and len(alist_KMAG4) < data_size and shutdown_process is False:
                    return False

                fDataObjFoundCount = 1

                utc_Time_GPS = round(float(gps_dataObj.utctime), 2)
                last_GPS = str(gps_dataObj.raw_data)

                if len(alist_QTFM) > 0 and (float(alist_QTFM[0].utctime) - utc_Time_GPS) >= 0.10:
                    del alist_GPS[gps_index]
                    continue

                if len(alist_QTFM) > 0 and float(alist_QTFM[0].utctime) < 1.00 and utc_Time_GPS > 235958.8:
                    del alist_GPS[gps_index]
                    continue

                if len(alist_KMAG4) > 0 and (float(alist_KMAG4[0].utctime) - utc_Time_GPS) >= 0.10:
                    del alist_GPS[gps_index]
                    continue

                if len(alist_KMAG4) > 0 and float(alist_KMAG4[0].utctime) < 2.00 and utc_Time_GPS == 235959.9:
                    del alist_GPS[gps_index]
                    continue

                # if len(alist_QTFM) > 0 and (utc_Time_GPS - float(alist_QTFM[0].utctime)) > 0.11:
                #     del alist_QTFM[0]
                #     continue

                while (fDataObjFoundCount > 0):

                    fDataObjFoundCount = 0

                    # QTMF
                    qtfm_index = 0

                    while qtfm_index < len(alist_QTFM):
                        qtfm_dataObj = alist_QTFM[qtfm_index]
                        utc_Time_QTFM = round(float(qtfm_dataObj.utctime), 2)
                        # if abs(utc_Time_QTFM - utc_Time_GPS) >= 0 and abs(utc_Time_QTFM - utc_Time_GPS) <= 0.11:
                        if utc_Time_QTFM == utc_Time_GPS:
                            last_QTFM = str(qtfm_dataObj.raw_data)
                            general_Time_QTFM = round(float(qtfm_dataObj.general_time), 4)
                            fDataObjFoundCount = fDataObjFoundCount + 1
                            break
                        elif utc_Time_QTFM > utc_Time_GPS:
                            del alist_GPS[gps_index]
                            break
                        elif utc_Time_QTFM == 0.0 and utc_Time_GPS == 235959.9:
                            del alist_GPS[gps_index]
                            break
                        else:
                            # print("Synch problem: " + "GPS-" + str(utc_Time_GPS) + " QTFM-" + str(utc_Time_QTFM))
                            # del alist_GPS[gps_index]
                            last_QTFM = str(qtfm_dataObj.raw_data)
                            fDataObjFoundCount = fDataObjFoundCount + 1
                            break

                        qtfm_index += 1

                    # KMAG4
                    KMAG4_index = 0

                    while KMAG4_index < len(alist_KMAG4):
                        KMAG4_dataObj = alist_KMAG4[KMAG4_index]
                        utc_Time_KMAG4 = round(float(KMAG4_dataObj.utctime), 2)
                        # if abs(utc_Time_KMAG4 - utc_Time_GPS) >= 0 and abs(utc_Time_KMAG4 - utc_Time_GPS) <= 0.11:
                        if utc_Time_KMAG4 == utc_Time_GPS:
                            last_KMAG4 = str(KMAG4_dataObj.raw_data)
                            fDataObjFoundCount = fDataObjFoundCount + 1
                            break
                        elif utc_Time_KMAG4 > utc_Time_GPS:
                            del alist_GPS[gps_index]
                            break
                        elif utc_Time_KMAG4 == 0.0 and utc_Time_GPS == 235959.9:
                            del alist_GPS[gps_index]
                            break
                        else:
                            # print("Synch problem: " + "GPS-" + str(utc_Time_GPS) + " KMAG4-" + str(utc_Time_KMAG4))
                            # del alist_GPS[gps_index]
                            last_KMAG4 = str(KMAG4_dataObj.raw_data)
                            fDataObjFoundCount = fDataObjFoundCount + 1
                            break

                        KMAG4_index += 1

                    if fDataObjFoundCount > 0 and (last_KMAG4 != "" or last_QTFM != ""):

                        # ADHAT
                        adhat_index = 0

                        while adhat_index < len(alist_ADHAT):
                            adhat_dataObj = alist_ADHAT[adhat_index]
                            general_Time_QTFM = round(float(qtfm_dataObj.general_time), 4)
                            general_Time_ADHAT = round(float(adhat_dataObj.general_time), 4)
                            
                            if general_Time_ADHAT > general_Time_QTFM:
                                last_ADHAT = str(adhat_dataObj.raw_data)
                                fDataObjFoundCount = fDataObjFoundCount + 1
                                break

                            adhat_index += 1

                        # LASER
                        laser_index = 0

                        while laser_index < len(alist_LASER):
                            laser_dataObj = alist_LASER[laser_index]
                            general_Time_QTFM = round(float(qtfm_dataObj.general_time), 4)
                            general_Time_LASER = round(float(laser_dataObj.general_time), 4)

                            if general_Time_LASER > general_Time_QTFM:
                                last_LASER = str(laser_dataObj.raw_data)
                                fDataObjFoundCount = fDataObjFoundCount + 1
                                break

                            laser_index += 1

                        # RA4500
                        ra4500_index = 0

                        while ra4500_index < len(alist_RA4500):
                            ra4500_dataObj = alist_RA4500[ra4500_index]
                            general_Time_QTFM = round(float(qtfm_dataObj.general_time), 4)
                            general_Time_RA4500 = round(float(ra4500_dataObj.general_time), 4)

                            if general_Time_RA4500 > general_Time_QTFM:
                                last_RA4500 = str(ra4500_dataObj.raw_data)
                                fDataObjFoundCount = fDataObjFoundCount + 1
                                break

                            ra4500_index += 1

                        result_data = self.updateDataLogging(last_KMAG4, last_GPS, last_LASER, last_QTFM, last_RA4500,
                                                             last_ADHAT)

                        gps_diff = utc_Time_GPS - last_valid_gps_value
                        if 0.11 < gps_diff < 40:
                            print(f"last_GPS = {utc_Time_GPS}, last_valid_gps_value = {last_valid_gps_value}")

                        last_valid_gps_value = utc_Time_GPS

                        self.dataLoggingBuffer.append(result_data)

                        while len(alist_ADHAT) > 0 and abs(utc_Time_GPS - float(alist_ADHAT[0].utctime)) > 0.11:
                            del alist_ADHAT[0]

                        while len(alist_LASER) > 0 and abs(utc_Time_GPS - float(alist_LASER[0].utctime)) > 0.11:
                            del alist_LASER[0]

                        while len(alist_RA4500) > 0 and abs(utc_Time_GPS - float(alist_RA4500[0].utctime)) > 0.11:
                            del alist_RA4500[0]

                        if qtfm_index > 0:
                            del alist_QTFM[0:qtfm_index + 1]
                        elif len(alist_QTFM) > 0:
                            del alist_QTFM[0]

                        if KMAG4_index > 0:
                            del alist_KMAG4[0:KMAG4_index + 1]
                        elif len(alist_KMAG4) > 0:
                            del alist_KMAG4[0]

                    # print("Current timer: " + str(time.time()))

                    if time.time() > self.start_timer + file_write_delay_sec and self.dataLoggingFile:
                        #print("Write Data: " + str(time.time() - self.start_timer))
                        self.dataLoggingFile.flush()
                        self.start_timer = time.time()
                        self.dataLoggingFile.write("".join(self.dataLoggingBuffer).encode('utf-8'))
                        self.dataLoggingBuffer.clear()
            return True

        ############ PARSE DATA LOGGING
        # 	count			 date	time	:kmag4:internal_counter	:kmag4:utc_time	:kmag4:utc_1pps_indicator	:kmag4:mag_a	:kmag4:mag_b	:kmag4:mag_c	:kmag4:mag_d
        # 	:kmag4:fx	:kmag4:fy	:kmag4:fz	:kmag4:radar_altimeter_m	:kmag4:vlf_line_tot	:kmag4:vlf_line_quad	:kmag4:vlf_ortho_tot	:kmag4:vlf_ortho_quad	laser:altimeter_m
        # 	:gga:utctime	:gga:sats_in_use	:gga:hdop	:gga:msl_altitude	:gga:position_fix_indicator	:gga:latitude	:gga:ns_indicator	:gga:longitude	:gga:ew_indicator
        # 	1		      0	6/27/2020	42:58.1	106660	35:14.7	0	53814.6075	10705.4576	10705.4865	10705.4947	-475873	-92936	157090	1.860499155	14	12	13	-8
        # 	35:14.7	6	1.3	1179.792	1	44.48349569	N	103.781426	W	0	0
        #   QTFM 294772841,12
        #           Ch0         Ch1     Ch2        Ch3        Ch4      Ch5       Ch6      Ch7
        #   ADHAT 0.06924,  0.11050,  0.02674,  0.09264,  0.02120,  0.10958,  0.12744,  0.10065,
        def updateDataLogging(self, KMAG4data, GPS_GGAdata, LASERdata, QTFMdata, RA4500data, ADHATdata):
            resultData = ""

            global dataCounter
            global lastLaserHeight
            global instrument_timestamp_enable

            instr_label = "instr_timestamp="

            # 1. count
            dataCounter = dataCounter + 1
            resultData = str(dataCounter) + ","

            # 2-3. date-time
            current_time = datetime.datetime.now()

            resultData = resultData + current_time.strftime("%Y-%m-%d,%H:%M:%S") + ","
            # resultData = resultData + current_time.strftime("%Y-%m-%d") + ","

            ####### QTFM #######
            if len(QTFMdata) > 0:
                # print(QTFMdata)

                if instrument_timestamp_enable:
                    # Find the index of instr_label in QTFMdata
                    index = QTFMdata.find(instr_label)

                    # If instr_label is found, extract the substring and append to resultData
                    if index >= 0:
                        instr_timestamp = QTFMdata[index + len(instr_label):]  # Get substring after instr_label
                        resultData += instr_timestamp + ","

                if quspinVersion == "2":

                    valid_mag = False
                    if "_" in QTFMdata:

                        valid_mag = True
                        QTFMdata = QTFMdata.replace("_", "")

                    elif "*" in QTFMdata:

                        valid_mag = False
                        QTFMdata = QTFMdata.replace("*", "")

                    # vector channels= X, Y or Z
                    fQF_X = False
                    fQF_Y = False
                    fQF_Z = False
                    if "X" in QTFMdata:

                        fQF_X = True
                        QTFMdata = QTFMdata.replace("X", ",")

                    elif "Y" in QTFMdata:

                        fQF_Y = True
                        QTFMdata = QTFMdata.replace("Y", ",")

                    elif "Z" in QTFMdata:

                        fQF_Z = True
                        QTFMdata = QTFMdata.replace("Z", ",")

                    vector_valid = False
                    if "=" in QTFMdata:

                        vector_valid = True
                        QTFMdata = QTFMdata.replace("=", ",")

                    elif "?" in QTFMdata:

                        vector_valid = False
                        QTFMdata = QTFMdata.replace("?", ",")

                    # @ 022  datacounter...always 3 digits
                    QTFMdata = QTFMdata.replace("@", ",")

                    # > q_msclock
                    QTFMdata = QTFMdata.replace(">", ",")

                    # s094                      mag_sensitivity
                    QTFMdata = QTFMdata.replace("s", ",")

                    # v006              vector_synsitivy
                    QTFMdata = QTFMdata.replace("v", ",")

                    QTFMdata += ",0,0,0,0,0,"  # just in case for missing data s and v

                    st_QTFM_Data = QTFMdata.split(",")

                    # # !40217.160_Y-19851.060? @ 022 > 223344s094v006
                    # # 213206.70, 40217.160, -19851.060, 022, 223344, 094, 006
                    # # !49848.021_X13161.090= @ 051 > 281804s026
                    # # !49848.732_Y-42072.421= @ 053 > 281836s023
                    # # !49849.945_Z-13197.614= @ 055 > 281868s023
                    # # Q_FID, Q_MSCLOCK, Q_DATACOUNT, Q_MAG_VALID, Q_MAG, Q_MAG_SENS, QF_VALID, QF_X, QF_Y, QF_Z, QF_SENS
                    # # 36208, 1273168, 11, TRUE, 44616.337, , TRUE, 14591.127, , ,
                    # # 36209, 1273200, 13, TRUE, 44615.524, , TRUE, , -36690.126, ,
                    # # 36210, 1273232, 15, TRUE, 44614.93, , TRUE, , , 8788.719,

                    # 21. qtfm:utctime
                    resultData += st_QTFM_Data[0] + ","

                    # qtfm: q_fid
                    resultData += st_QTFM_Data[1] + ","

                    # 22.qtfm: q_msclock
                    resultData += st_QTFM_Data[6] + ","

                    # 23. qtfm: q_datacount
                    resultData += st_QTFM_Data[5] + ","

                    # 24.qtfm: q_mag_valid
                    if (valid_mag):
                        resultData += "TRUE" + ","
                    else:
                        resultData += "FALSE" + ","

                    # 25. qtfm: q_mag
                    resultData += st_QTFM_Data[2] + ","

                    # 26. qtfm: q_mag_sens
                    resultData += st_QTFM_Data[4] + ","

                    # 27.qtfm: qf_valid
                    if (vector_valid):
                        resultData += "TRUE" + ","
                    else:
                        resultData += "FALSE" + ","

                    # if st_QTFM_Data[1]=="nan":
                    # st_QTFM_Data[1] = " "

                    # 28.qtfm:qf_x
                    if (fQF_X):
                        resultData += st_QTFM_Data[3] + ","
                    else:
                        resultData += ","

                    # 29. qtfm: qf_y
                    if (fQF_Y):
                        resultData += st_QTFM_Data[3] + ","
                    else:
                        resultData += ","

                    # 30. qtfm: qf_z
                    if (fQF_Z):
                        resultData += st_QTFM_Data[3] + ","
                    else:
                        resultData += ","

                    # 31.qtfm: qf_sens
                    resultData += st_QTFM_Data[7] + ","

                else:  # quspinVersion == "1":
                    st_QTFM_Data = QTFMdata.split(",")

                    if len(st_QTFM_Data) > 2:
                        # 12. QTFM Timestamp
                        if len(st_QTFM_Data[1]) > 0:
                            resultData += st_QTFM_Data[0] + ","
                        else:
                            resultData += ","

                        # 12. QTFM 0
                        resultData += st_QTFM_Data[1] + ","

                        # 13. QTFM 1
                        resultData += st_QTFM_Data[2] + ","

            #######  KMAG4 #######
            if len(KMAG4data) > 0:

                st_KMAG4 = KMAG4data.split(",")

                if instrument_timestamp_enable:
                    # Find the index of instr_label in QTFMdata
                    index = KMAG4data.find(instr_label)

                    # If instr_label is found, extract the substring and append to resultData
                    if index >= 0:
                        instr_timestamp = KMAG4data[index + len(instr_label):]  # Get substring after instr_label
                        resultData += instr_timestamp + ","

                if len(st_KMAG4) > 7:
                    # 4. kmag4:internal_counter
                    resultData += st_KMAG4[1] + ","

                    # 5. :kmag4:utc_time
                    resultData += st_KMAG4[2] + ","
                    # 6. :kmag4:utc_1pps_indicator
                    resultData += st_KMAG4[3] + ","
                    # 7. :kmag4:mag_a
                    resultData += st_KMAG4[4] + ","
                    # 8. :kmag4:mag_b
                    resultData += st_KMAG4[5] + ","
                    # 9. :kmag4:mag_c
                    resultData += st_KMAG4[6] + ","
                    # 10. :kmag4:mag_d
                    resultData += st_KMAG4[7] + ","

                    if len(st_KMAG4) > 15:
                        # 11. :kmag4:fx
                        resultData += st_KMAG4[8] + ","
                        # 12. :kmag4:fy
                        resultData += st_KMAG4[9] + ","
                        # 13. :kmag4:fz
                        resultData += st_KMAG4[10] + ","
                        # 14. :kmag4:radar_altimeter_m
                        altGL = 0.0012192 * float(
                            st_KMAG4[11])  # mult for Kroums to m (6.25 V on radalt represents 762 m)
                        resultData += str(altGL) + ","

                        # 15. :kmag4:vlf_line_tot
                        resultData += st_KMAG4[12] + ","
                        # 16. :kmag4:vlf_line_quad
                        resultData += st_KMAG4[13] + ","
                        # 17. :kmag4:vlf_ortho_tot
                        resultData += st_KMAG4[14] + ","
                        # 18. :kmag4:vlf_ortho_quad
                        resultData += st_KMAG4[15].trim() + ","

            ###### LASER ######
            # Altimeter Type LASER
            # 20. :laser:altimeter_m
            if len(LASERdata) > 0:

                LASERdata = LASERdata.replace("m", "")

                st_Laser = LASERdata.split(",")

                if instrument_timestamp_enable:
                    # Find the index of instr_label in QTFMdata
                    index = LASERdata.find(instr_label)

                    # If instr_label is found, extract the substring and append to resultData
                    if index >= 0:
                        instr_timestamp = LASERdata[index + len(instr_label):]  # Get substring after instr_label
                        resultData += instr_timestamp + ","

                if st_Laser[0] != "999999":
                    lastLaserHeight = st_Laser[0]
                    resultData += st_Laser[0] + ","
                else:

                    resultData += "-1" + ","

            ###### RA4500 ######
            # Altimeter Type RA4500
            # "ra4500:radar_altimeter_m,ra4500:radar_status,"
            if len(RA4500data) > 0:
                st_RA4500 = RA4500data.split(",")

                if instrument_timestamp_enable:
                    # Find the index of instr_label in QTFMdata
                    index = RA4500data.find(instr_label)

                    # If instr_label is found, extract the substring and append to resultData
                    if index >= 0:
                        instr_timestamp = RA4500data[index + len(instr_label):]  # Get substring after instr_label
                        resultData += instr_timestamp + ","

                resultData += st_RA4500[1] + "," + st_RA4500[2] + ","

            ###### ADHAT ######
            # Altimeter Type ADHAT
            # 20. :adhat:altimeter_m
            if len(ADHATdata) > 5:

                if instrument_timestamp_enable:
                    # Find the index of instr_label in QTFMdata
                    index = ADHATdata.find(instr_label)

                    # If instr_label is found, extract the substring and append to resultData
                    if index >= 0:
                        instr_timestamp = ADHATdata[index + len(instr_label):]  # Get substring after instr_label
                        resultData += instr_timestamp + ","

                st_ADHAT = ADHATdata.split(",")
                # Ch0
                resultData += st_ADHAT[1] + ","
                # Ch1
                resultData += st_ADHAT[2] + ","
                # Ch2
                resultData += st_ADHAT[3] + ","
                # Ch3
                resultData += st_ADHAT[4] + ","
                # Ch4
                resultData += st_ADHAT[5] + ","

            ###### GPS ######
            if len(GPS_GGAdata) > 0:

                st_GPS = GPS_GGAdata.split(",")

                if len(st_GPS) > 10:

                    if instrument_timestamp_enable:
                        # Find the index of instr_label in QTFMdata
                        index = GPS_GGAdata.find(instr_label)

                        # If instr_label is found, extract the substring and append to resultData
                        if index >= 0:
                            instr_timestamp = GPS_GGAdata[index + len(instr_label):]  # Get substring after instr_label
                            resultData += instr_timestamp + ","

                    # 21. :gga:utctime
                    resultData += st_GPS[1] + ","
                    # 22.:gga:sats_in_use
                    resultData += st_GPS[7] + ","
                    # 23.:gga:hdop
                    resultData += st_GPS[8] + ","
                    # 24.:gga:msl_altitude
                    resultData += st_GPS[9] + ","
                    # 25.:gga:position_fix_indicator
                    resultData += st_GPS[6] + ","
                    # 26.:gga:latitude
                    resultData += st_GPS[2] + ","
                    # 27.:gga:ns_indicator
                    resultData += st_GPS[3] + ","
                    # 28. :gga:longitude
                    resultData += st_GPS[4] + ","
                    # 29.:gga:longitude	:gga:ew_indicator
                    resultData += st_GPS[5]

            result_clean = re.sub('\r\n', '', resultData)
            return result_clean + "\n"

    def DataOutput_Init(self):
        config_object = configparser.ConfigParser()
        config_object.read(config_PI_file)

        dataoutput_param = DataOutput()

        config_DataOutput = config_object["DATA_OUTPUT"]

        if config_DataOutput["disabled"].strip() == "false":
            dataoutput_param.enabled = True

        dataoutput_param.file_ext = config_DataOutput["outputfile"].strip()  # e.g .base5200.mag_a.bin

        dataoutput_param.name_kmag4_channel = config_DataOutput["kmag4_channel"].strip()  # mag_a

        return dataoutput_param


class raw_data_struct:
    def __init__(self):
        self.utctime = 0
        self.general_time = 0
        self.raw_data = 0


if __name__ == "__main__":
    print("====== START Profile DataLogger =======================")
    print("VERSION 3.1.78 March 6, 2025")
    app = QApplication(sys.argv)
    widget = DataLogger_Profile()
    widget.show()
    sys.exit(app.exec())
