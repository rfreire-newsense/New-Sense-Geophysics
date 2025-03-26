# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_tiny.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLCDNumber, QLabel,
    QLayout, QMainWindow, QPushButton, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_DataLogger_Profile(object):
    def setupUi(self, DataLogger_Profile):
        if not DataLogger_Profile.objectName():
            DataLogger_Profile.setObjectName(u"DataLogger_Profile")
        DataLogger_Profile.resize(2050, 1081)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DataLogger_Profile.sizePolicy().hasHeightForWidth())
        DataLogger_Profile.setSizePolicy(sizePolicy)
        DataLogger_Profile.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        DataLogger_Profile.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.centralwidget = QWidget(DataLogger_Profile)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 0, 1921, 780))
        self.horizontalLayout_Tab = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_Tab.setObjectName(u"horizontalLayout_Tab")
        self.horizontalLayout_Tab.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.horizontalLayoutWidget_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab_ProfileMag = QWidget()
        self.tab_ProfileMag.setObjectName(u"tab_ProfileMag")
        self.verticalLayoutWidget_4 = QWidget(self.tab_ProfileMag)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(0, 0, 111, 41))
        self.verticalLayout_MaxMag = QHBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_MaxMag.setObjectName(u"verticalLayout_MaxMag")
        self.verticalLayout_MaxMag.setContentsMargins(0, 0, 0, 0)
        self.label_MaxMag = QLabel(self.verticalLayoutWidget_4)
        self.label_MaxMag.setObjectName(u"label_MaxMag")
        self.label_MaxMag.setMaximumSize(QSize(50, 30))
        self.label_MaxMag.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_MaxMag.addWidget(self.label_MaxMag)

        self.lcdNumber_MaxMag = QLCDNumber(self.verticalLayoutWidget_4)
        self.lcdNumber_MaxMag.setObjectName(u"lcdNumber_MaxMag")
        self.lcdNumber_MaxMag.setMaximumSize(QSize(50, 30))
        self.lcdNumber_MaxMag.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_MaxMag.setDigitCount(6)

        self.verticalLayout_MaxMag.addWidget(self.lcdNumber_MaxMag)

        self.verticalLayoutWidget_7 = QWidget(self.tab_ProfileMag)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(0, 70, 111, 41))
        self.verticalLayout_CurrentMag = QHBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_CurrentMag.setObjectName(u"verticalLayout_CurrentMag")
        self.verticalLayout_CurrentMag.setContentsMargins(0, 0, 0, 0)
        self.label_CurrentMag = QLabel(self.verticalLayoutWidget_7)
        self.label_CurrentMag.setObjectName(u"label_CurrentMag")
        self.label_CurrentMag.setMaximumSize(QSize(50, 30))
        self.label_CurrentMag.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_CurrentMag.addWidget(self.label_CurrentMag)

        self.lcdNumber_CurrentMag = QLCDNumber(self.verticalLayoutWidget_7)
        self.lcdNumber_CurrentMag.setObjectName(u"lcdNumber_CurrentMag")
        self.lcdNumber_CurrentMag.setMaximumSize(QSize(50, 30))
        self.lcdNumber_CurrentMag.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_CurrentMag.setDigitCount(6)

        self.verticalLayout_CurrentMag.addWidget(self.lcdNumber_CurrentMag)

        self.verticalLayoutWidget_6 = QWidget(self.tab_ProfileMag)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(0, 140, 111, 41))
        self.verticalLayout_MinMag = QHBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_MinMag.setObjectName(u"verticalLayout_MinMag")
        self.verticalLayout_MinMag.setContentsMargins(0, 0, 0, 0)
        self.label_MinMag = QLabel(self.verticalLayoutWidget_6)
        self.label_MinMag.setObjectName(u"label_MinMag")
        self.label_MinMag.setMaximumSize(QSize(50, 30))
        self.label_MinMag.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_MinMag.addWidget(self.label_MinMag)

        self.lcdNumber_MinMag = QLCDNumber(self.verticalLayoutWidget_6)
        self.lcdNumber_MinMag.setObjectName(u"lcdNumber_MinMag")
        self.lcdNumber_MinMag.setMaximumSize(QSize(50, 30))
        self.lcdNumber_MinMag.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_MinMag.setDigitCount(6)

        self.verticalLayout_MinMag.addWidget(self.lcdNumber_MinMag)

        self.horizontalLayoutWidget_12 = QWidget(self.tab_ProfileMag)
        self.horizontalLayoutWidget_12.setObjectName(u"horizontalLayoutWidget_12")
        self.horizontalLayoutWidget_12.setGeometry(QRect(120, 0, 671, 271))
        self.horizontalLayout_ProfileMag = QHBoxLayout(self.horizontalLayoutWidget_12)
        self.horizontalLayout_ProfileMag.setObjectName(u"horizontalLayout_ProfileMag")
        self.horizontalLayout_ProfileMag.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab_ProfileMag, "")
        self.tab_ProfileOrtho = QWidget()
        self.tab_ProfileOrtho.setObjectName(u"tab_ProfileOrtho")
        self.verticalLayoutWidget_8 = QWidget(self.tab_ProfileOrtho)
        self.verticalLayoutWidget_8.setObjectName(u"verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(0, 70, 111, 41))
        self.verticalLayout_Channel_Y = QHBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_Channel_Y.setObjectName(u"verticalLayout_Channel_Y")
        self.verticalLayout_Channel_Y.setContentsMargins(0, 0, 0, 0)
        self.label_Channel_Y = QLabel(self.verticalLayoutWidget_8)
        self.label_Channel_Y.setObjectName(u"label_Channel_Y")
        self.label_Channel_Y.setMaximumSize(QSize(50, 30))
        self.label_Channel_Y.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 0, 0);")

        self.verticalLayout_Channel_Y.addWidget(self.label_Channel_Y)

        self.lcdNumber_Channel_Y = QLCDNumber(self.verticalLayoutWidget_8)
        self.lcdNumber_Channel_Y.setObjectName(u"lcdNumber_Channel_Y")
        self.lcdNumber_Channel_Y.setMaximumSize(QSize(50, 30))
        self.lcdNumber_Channel_Y.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_Channel_Y.setDigitCount(7)

        self.verticalLayout_Channel_Y.addWidget(self.lcdNumber_Channel_Y)

        self.verticalLayoutWidget_9 = QWidget(self.tab_ProfileOrtho)
        self.verticalLayoutWidget_9.setObjectName(u"verticalLayoutWidget_9")
        self.verticalLayoutWidget_9.setGeometry(QRect(0, 0, 111, 41))
        self.verticalLayout_Channel_X = QHBoxLayout(self.verticalLayoutWidget_9)
        self.verticalLayout_Channel_X.setObjectName(u"verticalLayout_Channel_X")
        self.verticalLayout_Channel_X.setContentsMargins(0, 0, 0, 0)
        self.label_Channel_X = QLabel(self.verticalLayoutWidget_9)
        self.label_Channel_X.setObjectName(u"label_Channel_X")
        self.label_Channel_X.setMaximumSize(QSize(50, 30))
        self.label_Channel_X.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(0, 85, 255);")

        self.verticalLayout_Channel_X.addWidget(self.label_Channel_X)

        self.lcdNumber_Channel_X = QLCDNumber(self.verticalLayoutWidget_9)
        self.lcdNumber_Channel_X.setObjectName(u"lcdNumber_Channel_X")
        self.lcdNumber_Channel_X.setMaximumSize(QSize(50, 30))
        self.lcdNumber_Channel_X.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_Channel_X.setDigitCount(7)

        self.verticalLayout_Channel_X.addWidget(self.lcdNumber_Channel_X)

        self.horizontalLayoutWidget_10 = QWidget(self.tab_ProfileOrtho)
        self.horizontalLayoutWidget_10.setObjectName(u"horizontalLayoutWidget_10")
        self.horizontalLayoutWidget_10.setGeometry(QRect(120, 0, 671, 271))
        self.horizontalLayout_ProfileOrtho = QVBoxLayout(self.horizontalLayoutWidget_10)
        self.horizontalLayout_ProfileOrtho.setSpacing(0)
        self.horizontalLayout_ProfileOrtho.setObjectName(u"horizontalLayout_ProfileOrtho")
        self.horizontalLayout_ProfileOrtho.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_ProfileOrtho.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget_10 = QWidget(self.tab_ProfileOrtho)
        self.verticalLayoutWidget_10.setObjectName(u"verticalLayoutWidget_10")
        self.verticalLayoutWidget_10.setGeometry(QRect(0, 140, 111, 41))
        self.verticalLayout_Channel_Z = QHBoxLayout(self.verticalLayoutWidget_10)
        self.verticalLayout_Channel_Z.setObjectName(u"verticalLayout_Channel_Z")
        self.verticalLayout_Channel_Z.setContentsMargins(0, 0, 0, 0)
        self.label_Channel_Z = QLabel(self.verticalLayoutWidget_10)
        self.label_Channel_Z.setObjectName(u"label_Channel_Z")
        self.label_Channel_Z.setMaximumSize(QSize(50, 30))
        self.label_Channel_Z.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(0, 170, 0);")

        self.verticalLayout_Channel_Z.addWidget(self.label_Channel_Z)

        self.lcdNumber_Channel_Z = QLCDNumber(self.verticalLayoutWidget_10)
        self.lcdNumber_Channel_Z.setObjectName(u"lcdNumber_Channel_Z")
        self.lcdNumber_Channel_Z.setMaximumSize(QSize(50, 30))
        self.lcdNumber_Channel_Z.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_Channel_Z.setDigitCount(7)

        self.verticalLayout_Channel_Z.addWidget(self.lcdNumber_Channel_Z)

        self.tabWidget.addTab(self.tab_ProfileOrtho, "")
        self.tab_ProfileGPS = QWidget()
        self.tab_ProfileGPS.setObjectName(u"tab_ProfileGPS")
        self.verticalLayoutWidget_12 = QWidget(self.tab_ProfileGPS)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(0, 140, 111, 41))
        self.verticalLayout_GPS_Alt = QHBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_GPS_Alt.setObjectName(u"verticalLayout_GPS_Alt")
        self.verticalLayout_GPS_Alt.setContentsMargins(0, 0, 0, 0)
        self.label_GPS_Alt = QLabel(self.verticalLayoutWidget_12)
        self.label_GPS_Alt.setObjectName(u"label_GPS_Alt")
        self.label_GPS_Alt.setMaximumSize(QSize(50, 30))
        self.label_GPS_Alt.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(0, 170, 0);")

        self.verticalLayout_GPS_Alt.addWidget(self.label_GPS_Alt)

        self.lcdNumber_GPS_Alt = QLCDNumber(self.verticalLayoutWidget_12)
        self.lcdNumber_GPS_Alt.setObjectName(u"lcdNumber_GPS_Alt")
        self.lcdNumber_GPS_Alt.setMaximumSize(QSize(50, 30))
        self.lcdNumber_GPS_Alt.setStyleSheet(u"font: 700 16pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_GPS_Alt.setDigitCount(7)

        self.verticalLayout_GPS_Alt.addWidget(self.lcdNumber_GPS_Alt)

        self.verticalLayoutWidget_13 = QWidget(self.tab_ProfileGPS)
        self.verticalLayoutWidget_13.setObjectName(u"verticalLayoutWidget_13")
        self.verticalLayoutWidget_13.setGeometry(QRect(0, 70, 111, 41))
        self.verticalLayout_GPS_Lon = QHBoxLayout(self.verticalLayoutWidget_13)
        self.verticalLayout_GPS_Lon.setObjectName(u"verticalLayout_GPS_Lon")
        self.verticalLayout_GPS_Lon.setContentsMargins(0, 0, 0, 0)
        self.label_GPS_Lon = QLabel(self.verticalLayoutWidget_13)
        self.label_GPS_Lon.setObjectName(u"label_GPS_Lon")
        self.label_GPS_Lon.setMaximumSize(QSize(50, 30))
        self.label_GPS_Lon.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 0, 0);")

        self.verticalLayout_GPS_Lon.addWidget(self.label_GPS_Lon)

        self.lcdNumber_GPS_Lon = QLCDNumber(self.verticalLayoutWidget_13)
        self.lcdNumber_GPS_Lon.setObjectName(u"lcdNumber_GPS_Lon")
        self.lcdNumber_GPS_Lon.setMaximumSize(QSize(50, 30))
        self.lcdNumber_GPS_Lon.setStyleSheet(u"font: 700 16pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_GPS_Lon.setDigitCount(7)

        self.verticalLayout_GPS_Lon.addWidget(self.lcdNumber_GPS_Lon)

        self.horizontalLayoutWidget_13 = QWidget(self.tab_ProfileGPS)
        self.horizontalLayoutWidget_13.setObjectName(u"horizontalLayoutWidget_13")
        self.horizontalLayoutWidget_13.setGeometry(QRect(120, 0, 671, 271))
        self.horizontalLayout_ProfileGPS = QVBoxLayout(self.horizontalLayoutWidget_13)
        self.horizontalLayout_ProfileGPS.setSpacing(0)
        self.horizontalLayout_ProfileGPS.setObjectName(u"horizontalLayout_ProfileGPS")
        self.horizontalLayout_ProfileGPS.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_ProfileGPS.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget_16 = QWidget(self.tab_ProfileGPS)
        self.verticalLayoutWidget_16.setObjectName(u"verticalLayoutWidget_16")
        self.verticalLayoutWidget_16.setGeometry(QRect(0, 0, 111, 41))
        self.verticalLayout_GPS_Lat = QHBoxLayout(self.verticalLayoutWidget_16)
        self.verticalLayout_GPS_Lat.setObjectName(u"verticalLayout_GPS_Lat")
        self.verticalLayout_GPS_Lat.setContentsMargins(0, 0, 0, 0)
        self.label_GPS_Lat = QLabel(self.verticalLayoutWidget_16)
        self.label_GPS_Lat.setObjectName(u"label_GPS_Lat")
        self.label_GPS_Lat.setMaximumSize(QSize(50, 30))
        self.label_GPS_Lat.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(0, 85, 255);")

        self.verticalLayout_GPS_Lat.addWidget(self.label_GPS_Lat)

        self.lcdNumber_GPS_Lat = QLCDNumber(self.verticalLayoutWidget_16)
        self.lcdNumber_GPS_Lat.setObjectName(u"lcdNumber_GPS_Lat")
        self.lcdNumber_GPS_Lat.setMaximumSize(QSize(50, 30))
        self.lcdNumber_GPS_Lat.setStyleSheet(u"font: 700 16pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_GPS_Lat.setDigitCount(7)

        self.verticalLayout_GPS_Lat.addWidget(self.lcdNumber_GPS_Lat)

        self.tabWidget.addTab(self.tab_ProfileGPS, "")
        self.tab_Profile_RA4500 = QWidget()
        self.tab_Profile_RA4500.setObjectName(u"tab_Profile_RA4500")
        self.verticalLayoutWidget_17 = QWidget(self.tab_Profile_RA4500)
        self.verticalLayoutWidget_17.setObjectName(u"verticalLayoutWidget_17")
        self.verticalLayoutWidget_17.setGeometry(QRect(0, 0, 111, 41))
        self.verticalLayout_MaxRA4500 = QHBoxLayout(self.verticalLayoutWidget_17)
        self.verticalLayout_MaxRA4500.setObjectName(u"verticalLayout_MaxRA4500")
        self.verticalLayout_MaxRA4500.setContentsMargins(0, 0, 0, 0)
        self.label_MaxRA4500 = QLabel(self.verticalLayoutWidget_17)
        self.label_MaxRA4500.setObjectName(u"label_MaxRA4500")
        self.label_MaxRA4500.setMaximumSize(QSize(50, 30))
        self.label_MaxRA4500.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_MaxRA4500.addWidget(self.label_MaxRA4500)

        self.lcdNumber_MaxRA4500 = QLCDNumber(self.verticalLayoutWidget_17)
        self.lcdNumber_MaxRA4500.setObjectName(u"lcdNumber_MaxRA4500")
        self.lcdNumber_MaxRA4500.setMaximumSize(QSize(50, 30))
        self.lcdNumber_MaxRA4500.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_MaxRA4500.setDigitCount(6)

        self.verticalLayout_MaxRA4500.addWidget(self.lcdNumber_MaxRA4500)

        self.verticalLayoutWidget_18 = QWidget(self.tab_Profile_RA4500)
        self.verticalLayoutWidget_18.setObjectName(u"verticalLayoutWidget_18")
        self.verticalLayoutWidget_18.setGeometry(QRect(0, 70, 111, 41))
        self.verticalLayout_CurrentRA4500 = QHBoxLayout(self.verticalLayoutWidget_18)
        self.verticalLayout_CurrentRA4500.setObjectName(u"verticalLayout_CurrentRA4500")
        self.verticalLayout_CurrentRA4500.setContentsMargins(0, 0, 0, 0)
        self.label_CurrentRA4500 = QLabel(self.verticalLayoutWidget_18)
        self.label_CurrentRA4500.setObjectName(u"label_CurrentRA4500")
        self.label_CurrentRA4500.setMaximumSize(QSize(50, 30))
        self.label_CurrentRA4500.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_CurrentRA4500.addWidget(self.label_CurrentRA4500)

        self.lcdNumber_CurrentRA4500 = QLCDNumber(self.verticalLayoutWidget_18)
        self.lcdNumber_CurrentRA4500.setObjectName(u"lcdNumber_CurrentRA4500")
        self.lcdNumber_CurrentRA4500.setMaximumSize(QSize(50, 30))
        self.lcdNumber_CurrentRA4500.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_CurrentRA4500.setDigitCount(6)

        self.verticalLayout_CurrentRA4500.addWidget(self.lcdNumber_CurrentRA4500)

        self.verticalLayoutWidget_19 = QWidget(self.tab_Profile_RA4500)
        self.verticalLayoutWidget_19.setObjectName(u"verticalLayoutWidget_19")
        self.verticalLayoutWidget_19.setGeometry(QRect(0, 140, 111, 41))
        self.verticalLayout_MinRA4500 = QHBoxLayout(self.verticalLayoutWidget_19)
        self.verticalLayout_MinRA4500.setObjectName(u"verticalLayout_MinRA4500")
        self.verticalLayout_MinRA4500.setContentsMargins(0, 0, 0, 0)
        self.label_MinRA4500 = QLabel(self.verticalLayoutWidget_19)
        self.label_MinRA4500.setObjectName(u"label_MinRA4500")
        self.label_MinRA4500.setMaximumSize(QSize(50, 30))
        self.label_MinRA4500.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_MinRA4500.addWidget(self.label_MinRA4500)

        self.lcdNumber_MinRA4500 = QLCDNumber(self.verticalLayoutWidget_19)
        self.lcdNumber_MinRA4500.setObjectName(u"lcdNumber_MinRA4500")
        self.lcdNumber_MinRA4500.setMaximumSize(QSize(50, 30))
        self.lcdNumber_MinRA4500.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_MinRA4500.setDigitCount(6)

        self.verticalLayout_MinRA4500.addWidget(self.lcdNumber_MinRA4500)

        self.horizontalLayoutWidget_14 = QWidget(self.tab_Profile_RA4500)
        self.horizontalLayoutWidget_14.setObjectName(u"horizontalLayoutWidget_14")
        self.horizontalLayoutWidget_14.setGeometry(QRect(120, 0, 671, 271))
        self.horizontalLayout_RA4500 = QHBoxLayout(self.horizontalLayoutWidget_14)
        self.horizontalLayout_RA4500.setObjectName(u"horizontalLayout_RA4500")
        self.horizontalLayout_RA4500.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab_Profile_RA4500, "")
        self.tab_Profile_Laser = QWidget()
        self.tab_Profile_Laser.setObjectName(u"tab_Profile_Laser")
        self.verticalLayoutWidget_20 = QWidget(self.tab_Profile_Laser)
        self.verticalLayoutWidget_20.setObjectName(u"verticalLayoutWidget_20")
        self.verticalLayoutWidget_20.setGeometry(QRect(0, 0, 111, 41))
        self.verticalLayout_MaxLaser = QHBoxLayout(self.verticalLayoutWidget_20)
        self.verticalLayout_MaxLaser.setObjectName(u"verticalLayout_MaxLaser")
        self.verticalLayout_MaxLaser.setContentsMargins(0, 0, 0, 0)
        self.label_MaxLaser = QLabel(self.verticalLayoutWidget_20)
        self.label_MaxLaser.setObjectName(u"label_MaxLaser")
        self.label_MaxLaser.setMaximumSize(QSize(50, 30))
        self.label_MaxLaser.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_MaxLaser.addWidget(self.label_MaxLaser)

        self.lcdNumber_MaxLaser = QLCDNumber(self.verticalLayoutWidget_20)
        self.lcdNumber_MaxLaser.setObjectName(u"lcdNumber_MaxLaser")
        self.lcdNumber_MaxLaser.setMaximumSize(QSize(50, 30))
        self.lcdNumber_MaxLaser.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_MaxLaser.setDigitCount(6)

        self.verticalLayout_MaxLaser.addWidget(self.lcdNumber_MaxLaser)

        self.verticalLayoutWidget_21 = QWidget(self.tab_Profile_Laser)
        self.verticalLayoutWidget_21.setObjectName(u"verticalLayoutWidget_21")
        self.verticalLayoutWidget_21.setGeometry(QRect(0, 70, 111, 41))
        self.verticalLayout_CurrentLaser = QHBoxLayout(self.verticalLayoutWidget_21)
        self.verticalLayout_CurrentLaser.setObjectName(u"verticalLayout_CurrentLaser")
        self.verticalLayout_CurrentLaser.setContentsMargins(0, 0, 0, 0)
        self.label_CurrentLaser = QLabel(self.verticalLayoutWidget_21)
        self.label_CurrentLaser.setObjectName(u"label_CurrentLaser")
        self.label_CurrentLaser.setMaximumSize(QSize(50, 30))
        self.label_CurrentLaser.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_CurrentLaser.addWidget(self.label_CurrentLaser)

        self.lcdNumber_CurrentLaser = QLCDNumber(self.verticalLayoutWidget_21)
        self.lcdNumber_CurrentLaser.setObjectName(u"lcdNumber_CurrentLaser")
        self.lcdNumber_CurrentLaser.setMaximumSize(QSize(50, 30))
        self.lcdNumber_CurrentLaser.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_CurrentLaser.setDigitCount(6)

        self.verticalLayout_CurrentLaser.addWidget(self.lcdNumber_CurrentLaser)

        self.verticalLayoutWidget_22 = QWidget(self.tab_Profile_Laser)
        self.verticalLayoutWidget_22.setObjectName(u"verticalLayoutWidget_22")
        self.verticalLayoutWidget_22.setGeometry(QRect(0, 140, 111, 41))
        self.verticalLayout_MinLaser = QHBoxLayout(self.verticalLayoutWidget_22)
        self.verticalLayout_MinLaser.setObjectName(u"verticalLayout_MinLaser")
        self.verticalLayout_MinLaser.setContentsMargins(0, 0, 0, 0)
        self.label_MinLaser = QLabel(self.verticalLayoutWidget_22)
        self.label_MinLaser.setObjectName(u"label_MinLaser")
        self.label_MinLaser.setMaximumSize(QSize(50, 30))
        self.label_MinLaser.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_MinLaser.addWidget(self.label_MinLaser)

        self.lcdNumber_MinLaser = QLCDNumber(self.verticalLayoutWidget_22)
        self.lcdNumber_MinLaser.setObjectName(u"lcdNumber_MinLaser")
        self.lcdNumber_MinLaser.setMaximumSize(QSize(50, 30))
        self.lcdNumber_MinLaser.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_MinLaser.setDigitCount(6)

        self.verticalLayout_MinLaser.addWidget(self.lcdNumber_MinLaser)

        self.horizontalLayoutWidget_9 = QWidget(self.tab_Profile_Laser)
        self.horizontalLayoutWidget_9.setObjectName(u"horizontalLayoutWidget_9")
        self.horizontalLayoutWidget_9.setGeometry(QRect(120, 0, 671, 271))
        self.horizontalLayout_ProfileLaser = QHBoxLayout(self.horizontalLayoutWidget_9)
        self.horizontalLayout_ProfileLaser.setObjectName(u"horizontalLayout_ProfileLaser")
        self.horizontalLayout_ProfileLaser.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab_Profile_Laser, "")
        self.tab_Profile_ADHAT = QWidget()
        self.tab_Profile_ADHAT.setObjectName(u"tab_Profile_ADHAT")
        self.verticalLayoutWidget_51 = QWidget(self.tab_Profile_ADHAT)
        self.verticalLayoutWidget_51.setObjectName(u"verticalLayoutWidget_51")
        self.verticalLayoutWidget_51.setGeometry(QRect(0, 140, 111, 41))
        self.verticalLayout_MinADHAT = QHBoxLayout(self.verticalLayoutWidget_51)
        self.verticalLayout_MinADHAT.setObjectName(u"verticalLayout_MinADHAT")
        self.verticalLayout_MinADHAT.setContentsMargins(0, 0, 0, 0)
        self.label_MinADHAT = QLabel(self.verticalLayoutWidget_51)
        self.label_MinADHAT.setObjectName(u"label_MinADHAT")
        self.label_MinADHAT.setMaximumSize(QSize(50, 30))
        self.label_MinADHAT.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_MinADHAT.addWidget(self.label_MinADHAT)

        self.lcdNumber_MinADHAT = QLCDNumber(self.verticalLayoutWidget_51)
        self.lcdNumber_MinADHAT.setObjectName(u"lcdNumber_MinADHAT")
        self.lcdNumber_MinADHAT.setMaximumSize(QSize(50, 30))
        self.lcdNumber_MinADHAT.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_MinADHAT.setDigitCount(6)

        self.verticalLayout_MinADHAT.addWidget(self.lcdNumber_MinADHAT)

        self.verticalLayoutWidget_52 = QWidget(self.tab_Profile_ADHAT)
        self.verticalLayoutWidget_52.setObjectName(u"verticalLayoutWidget_52")
        self.verticalLayoutWidget_52.setGeometry(QRect(0, 70, 111, 41))
        self.verticalLayout_CurrentADHAT = QHBoxLayout(self.verticalLayoutWidget_52)
        self.verticalLayout_CurrentADHAT.setObjectName(u"verticalLayout_CurrentADHAT")
        self.verticalLayout_CurrentADHAT.setContentsMargins(0, 0, 0, 0)
        self.label_CurrentADHAT = QLabel(self.verticalLayoutWidget_52)
        self.label_CurrentADHAT.setObjectName(u"label_CurrentADHAT")
        self.label_CurrentADHAT.setMaximumSize(QSize(50, 30))
        self.label_CurrentADHAT.setStyleSheet(u"font: 700 10pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_CurrentADHAT.addWidget(self.label_CurrentADHAT)

        self.lcdNumber_CurrentADHAT = QLCDNumber(self.verticalLayoutWidget_52)
        self.lcdNumber_CurrentADHAT.setObjectName(u"lcdNumber_CurrentADHAT")
        self.lcdNumber_CurrentADHAT.setMaximumSize(QSize(50, 30))
        self.lcdNumber_CurrentADHAT.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_CurrentADHAT.setDigitCount(6)

        self.verticalLayout_CurrentADHAT.addWidget(self.lcdNumber_CurrentADHAT)

        self.horizontalLayoutWidget_25 = QWidget(self.tab_Profile_ADHAT)
        self.horizontalLayoutWidget_25.setObjectName(u"horizontalLayoutWidget_25")
        self.horizontalLayoutWidget_25.setGeometry(QRect(120, 0, 671, 271))
        self.horizontalLayout_ADHAT = QHBoxLayout(self.horizontalLayoutWidget_25)
        self.horizontalLayout_ADHAT.setObjectName(u"horizontalLayout_ADHAT")
        self.horizontalLayout_ADHAT.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget_53 = QWidget(self.tab_Profile_ADHAT)
        self.verticalLayoutWidget_53.setObjectName(u"verticalLayoutWidget_53")
        self.verticalLayoutWidget_53.setGeometry(QRect(0, 0, 111, 41))
        self.verticalLayout_MaxADHAT = QHBoxLayout(self.verticalLayoutWidget_53)
        self.verticalLayout_MaxADHAT.setObjectName(u"verticalLayout_MaxADHAT")
        self.verticalLayout_MaxADHAT.setContentsMargins(0, 0, 0, 0)
        self.label_MaxADHAT = QLabel(self.verticalLayoutWidget_53)
        self.label_MaxADHAT.setObjectName(u"label_MaxADHAT")
        self.label_MaxADHAT.setMaximumSize(QSize(50, 30))
        self.label_MaxADHAT.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_MaxADHAT.addWidget(self.label_MaxADHAT)

        self.lcdNumber_MaxADHAT = QLCDNumber(self.verticalLayoutWidget_53)
        self.lcdNumber_MaxADHAT.setObjectName(u"lcdNumber_MaxADHAT")
        self.lcdNumber_MaxADHAT.setMaximumSize(QSize(50, 30))
        self.lcdNumber_MaxADHAT.setStyleSheet(u"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.lcdNumber_MaxADHAT.setDigitCount(6)

        self.verticalLayout_MaxADHAT.addWidget(self.lcdNumber_MaxADHAT)

        self.tabWidget.addTab(self.tab_Profile_ADHAT, "")

        self.horizontalLayout_Tab.addWidget(self.tabWidget)

        self.horizontalLayoutWidget_7 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_7.setObjectName(u"horizontalLayoutWidget_7")
        self.horizontalLayoutWidget_7.setGeometry(QRect(1575, 783, 339, 297))
        self.verticalLayout_7 = QVBoxLayout(self.horizontalLayoutWidget_7)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_ProfileView = QPushButton(self.horizontalLayoutWidget_7)
        self.pushButton_ProfileView.setObjectName(u"pushButton_ProfileView")
        sizePolicy.setHeightForWidth(self.pushButton_ProfileView.sizePolicy().hasHeightForWidth())
        self.pushButton_ProfileView.setSizePolicy(sizePolicy)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush2 = QBrush(QColor(255, 255, 255, 128))
        brush2.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        brush3 = QBrush(QColor(255, 255, 255, 128))
        brush3.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush3)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        brush4 = QBrush(QColor(255, 255, 255, 135))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush5 = QBrush(QColor(255, 255, 255, 128))
        brush5.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush5)
#endif
        self.pushButton_ProfileView.setPalette(palette)
        self.pushButton_ProfileView.setAutoFillBackground(False)
        self.pushButton_ProfileView.setStyleSheet(u"             QPushButton {\n"
"                 background-color: black;\n"
"                 border: none;\n"
"                 color: white;\n"
"                 font: 700 16pt \\\"Segoe UI\\\";\n"
"                 border-image: url(buttons_grey.png);\n"
"             }\n"
"             QPushButton:hover {\n"
"                 background-color: #333;\n"
"             }\n"
"             QPushButton:pressed {\n"
"                border-image: url(buttons_grey_p.png);\n"
"             }")
        self.pushButton_ProfileView.setCheckable(False)

        self.verticalLayout_7.addWidget(self.pushButton_ProfileView)

        self.pushButton_Exit = QPushButton(self.horizontalLayoutWidget_7)
        self.pushButton_Exit.setObjectName(u"pushButton_Exit")
        sizePolicy.setHeightForWidth(self.pushButton_Exit.sizePolicy().hasHeightForWidth())
        self.pushButton_Exit.setSizePolicy(sizePolicy)
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush6 = QBrush(QColor(255, 255, 255, 128))
        brush6.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush6)
#endif
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        brush7 = QBrush(QColor(255, 255, 255, 128))
        brush7.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush7)
#endif
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush8 = QBrush(QColor(255, 255, 255, 128))
        brush8.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush8)
#endif
        self.pushButton_Exit.setPalette(palette1)
        self.pushButton_Exit.setStyleSheet(u"             QPushButton {\n"
"                 background-color: black;\n"
"                 border: none;\n"
"                 color: white;\n"
"                 font: 700 16pt \\\"Segoe UI\\\";\n"
"                 border-image: url(buttons_grey.png);\n"
"             }\n"
"             QPushButton:hover {\n"
"                 background-color: #333;\n"
"             }\n"
"             QPushButton:pressed {\n"
"                border-image: url(buttons_grey_p.png);\n"
"             }")

        self.verticalLayout_7.addWidget(self.pushButton_Exit)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 783, 406, 299))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_Start_Profile = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_Start_Profile.setObjectName(u"pushButton_Start_Profile")
        sizePolicy.setHeightForWidth(self.pushButton_Start_Profile.sizePolicy().hasHeightForWidth())
        self.pushButton_Start_Profile.setSizePolicy(sizePolicy)
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette2.setBrush(QPalette.Active, QPalette.Text, brush)
        palette2.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush9 = QBrush(QColor(255, 255, 255, 128))
        brush9.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Active, QPalette.PlaceholderText, brush9)
#endif
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        brush10 = QBrush(QColor(255, 255, 255, 128))
        brush10.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush10)
#endif
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush11 = QBrush(QColor(255, 255, 255, 128))
        brush11.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette2.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush11)
#endif
        self.pushButton_Start_Profile.setPalette(palette2)
        self.pushButton_Start_Profile.setStyleSheet(u"             QPushButton {\n"
"                 background-color: black;\n"
"                 border: none;\n"
"                 color: white;\n"
"                 font: 700 16pt \\\"Segoe UI\\\";\n"
"                 border-image: url(buttons_grey.png);\n"
"             }\n"
"             QPushButton:hover {\n"
"                 background-color: #333;\n"
"             }\n"
"             QPushButton:pressed {\n"
"                border-image: url(buttons_grey_p.png);\n"
"             }")
        self.pushButton_Start_Profile.setCheckable(True)

        self.verticalLayout_3.addWidget(self.pushButton_Start_Profile)

        self.pushButton_Stop_Profile = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_Stop_Profile.setObjectName(u"pushButton_Stop_Profile")
        sizePolicy.setHeightForWidth(self.pushButton_Stop_Profile.sizePolicy().hasHeightForWidth())
        self.pushButton_Stop_Profile.setSizePolicy(sizePolicy)
        palette3 = QPalette()
        palette3.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette3.setBrush(QPalette.Active, QPalette.Text, brush)
        palette3.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush12 = QBrush(QColor(255, 255, 255, 128))
        brush12.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Active, QPalette.PlaceholderText, brush12)
#endif
        palette3.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette3.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        brush13 = QBrush(QColor(255, 255, 255, 128))
        brush13.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush13)
#endif
        palette3.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette3.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette3.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush14 = QBrush(QColor(255, 255, 255, 128))
        brush14.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette3.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush14)
#endif
        self.pushButton_Stop_Profile.setPalette(palette3)
        self.pushButton_Stop_Profile.setStyleSheet(u"             QPushButton {\n"
"                 background-color: black;\n"
"                 border: none;\n"
"                 color: white;\n"
"                 font: 700 16pt \\\"Segoe UI\\\";\n"
"                 border-image: url(buttons_grey.png);\n"
"             }\n"
"             QPushButton:hover {\n"
"                 background-color: #333;\n"
"             }\n"
"             QPushButton:pressed {\n"
"                border-image: url(buttons_grey_p.png);\n"
"             }")

        self.verticalLayout_3.addWidget(self.pushButton_Stop_Profile)

        self.horizontalLayoutWidget_11 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_11.setObjectName(u"horizontalLayoutWidget_11")
        self.horizontalLayoutWidget_11.setGeometry(QRect(403, 780, 381, 150))
        self.horizontalLayout_10 = QHBoxLayout(self.horizontalLayoutWidget_11)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.pushButton_ProfileScale = QPushButton(self.horizontalLayoutWidget_11)
        self.pushButton_ProfileScale.setObjectName(u"pushButton_ProfileScale")
        sizePolicy.setHeightForWidth(self.pushButton_ProfileScale.sizePolicy().hasHeightForWidth())
        self.pushButton_ProfileScale.setSizePolicy(sizePolicy)
        palette4 = QPalette()
        palette4.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette4.setBrush(QPalette.Active, QPalette.Text, brush)
        palette4.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette4.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush15 = QBrush(QColor(255, 255, 255, 128))
        brush15.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Active, QPalette.PlaceholderText, brush15)
#endif
        palette4.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette4.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette4.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        brush16 = QBrush(QColor(255, 255, 255, 128))
        brush16.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush16)
#endif
        palette4.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette4.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette4.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette4.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette4.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush17 = QBrush(QColor(255, 255, 255, 128))
        brush17.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush17)
#endif
        self.pushButton_ProfileScale.setPalette(palette4)
        self.pushButton_ProfileScale.setStyleSheet(u"             QPushButton {\n"
"                 background-color: black;\n"
"                 border: none;\n"
"                 color: white;\n"
"                 font: 700 16pt \\\"Segoe UI\\\";\n"
"                 border-image: url(buttons_grey.png);\n"
"             }\n"
"             QPushButton:hover {\n"
"                 background-color: #333;\n"
"             }\n"
"             QPushButton:pressed {\n"
"                border-image: url(buttons_grey_p.png);\n"
"             }")

        self.horizontalLayout_10.addWidget(self.pushButton_ProfileScale)

        self.verticalLayoutWidget_15 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_15.setObjectName(u"verticalLayoutWidget_15")
        self.verticalLayoutWidget_15.setGeometry(QRect(1230, 790, 339, 141))
        self.verticalLayout_15 = QVBoxLayout(self.verticalLayoutWidget_15)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.label_Status = QLabel(self.verticalLayoutWidget_15)
        self.label_Status.setObjectName(u"label_Status")
        sizePolicy.setHeightForWidth(self.label_Status.sizePolicy().hasHeightForWidth())
        self.label_Status.setSizePolicy(sizePolicy)
        self.label_Status.setStyleSheet(u"background-color: black;")

        self.verticalLayout_15.addWidget(self.label_Status)

        self.verticalLayoutWidget_23 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_23.setObjectName(u"verticalLayoutWidget_23")
        self.verticalLayoutWidget_23.setGeometry(QRect(1230, 940, 339, 141))
        self.verticalLayout_16 = QVBoxLayout(self.verticalLayoutWidget_23)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_Error = QLabel(self.verticalLayoutWidget_23)
        self.label_Error.setObjectName(u"label_Error")
        sizePolicy.setHeightForWidth(self.label_Error.sizePolicy().hasHeightForWidth())
        self.label_Error.setSizePolicy(sizePolicy)
        self.label_Error.setStyleSheet(u"background-color: black;\n"
"font: 700 18pt \"Segoe UI\";\n"
"color: rgb(255,0, 0);")

        self.verticalLayout_16.addWidget(self.label_Error)

        self.horizontalLayoutWidget_15 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_15.setObjectName(u"horizontalLayoutWidget_15")
        self.horizontalLayoutWidget_15.setGeometry(QRect(400, 930, 381, 150))
        self.horizontalLayout_11 = QHBoxLayout(self.horizontalLayoutWidget_15)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.pushButton_Channel = QPushButton(self.horizontalLayoutWidget_15)
        self.pushButton_Channel.setObjectName(u"pushButton_Channel")
        self.pushButton_Channel.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_Channel.sizePolicy().hasHeightForWidth())
        self.pushButton_Channel.setSizePolicy(sizePolicy)
        palette5 = QPalette()
        palette5.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette5.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette5.setBrush(QPalette.Active, QPalette.Text, brush)
        palette5.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette5.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette5.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush17 = QBrush(QColor(255, 255, 255, 128))
        brush17.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Active, QPalette.PlaceholderText, brush17)
        # endif
        palette5.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette5.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette5.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        brush18 = QBrush(QColor(255, 255, 255, 128))
        brush18.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush18)
        # endif
        palette5.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette5.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette5.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush19 = QBrush(QColor(255, 255, 255, 128))
        brush19.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette5.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush19)
        # endif
        self.pushButton_Channel.setPalette(palette5)
        self.pushButton_Channel.setStyleSheet(u"             QPushButton {\n"
                                              "                 background-color: black;\n"
                                              "                 border: none;\n"
                                              "                 color: white;\n"
                                              "                 font: 700 16pt \\\"Segoe UI\\\";\n"
                                              "                 border-image: url(buttons_grey.png);\n"
                                              "             }\n"
                                              "             QPushButton:hover {\n"
                                              "                 background-color: #333;\n"
                                              "             }\n"
                                              "             QPushButton:pressed {\n"
                                              "                border-image: url(buttons_grey_p.png);\n"
                                              "             }")

        self.horizontalLayout_11.addWidget(self.pushButton_Channel)

        DataLogger_Profile.setCentralWidget(self.centralwidget)

        self.retranslateUi(DataLogger_Profile)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(DataLogger_Profile)
    # setupUi

    def retranslateUi(self, DataLogger_Profile):
        DataLogger_Profile.setWindowTitle(QCoreApplication.translate("DataLogger_Profile", u"QuspinTestFormat_MainWindow", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_MaxMag.setText(QCoreApplication.translate("DataLogger_Profile", u"MAX", None))
        self.label_CurrentMag.setText(QCoreApplication.translate("DataLogger_Profile", u"MAG\n"
"Value", None))
        self.label_MinMag.setText(QCoreApplication.translate("DataLogger_Profile", u"MIN", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ProfileMag), QCoreApplication.translate("DataLogger_Profile", u"Profile Mag", None))
        self.label_Channel_Y.setText(QCoreApplication.translate("DataLogger_Profile", u"Ch Y", None))
        self.label_Channel_X.setText(QCoreApplication.translate("DataLogger_Profile", u"Ch X", None))
        self.label_Channel_Z.setText(QCoreApplication.translate("DataLogger_Profile", u"Ch Z", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ProfileOrtho), QCoreApplication.translate("DataLogger_Profile", u"Profile Ortho", None))
        self.label_GPS_Alt.setText(QCoreApplication.translate("DataLogger_Profile", u"Alt", None))
        self.label_GPS_Lon.setText(QCoreApplication.translate("DataLogger_Profile", u"Lon", None))
        self.label_GPS_Lat.setText(QCoreApplication.translate("DataLogger_Profile", u"Lat", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ProfileGPS), QCoreApplication.translate("DataLogger_Profile", u"Profile GPS", None))
        self.label_MaxRA4500.setText(QCoreApplication.translate("DataLogger_Profile", u"MAX", None))
        self.label_CurrentRA4500.setText(QCoreApplication.translate("DataLogger_Profile", u"RA4500\n"
"Value", None))
        self.label_MinRA4500.setText(QCoreApplication.translate("DataLogger_Profile", u"MIN", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Profile_RA4500), QCoreApplication.translate("DataLogger_Profile", u"Profile RA4500", None))
        self.label_MaxLaser.setText(QCoreApplication.translate("DataLogger_Profile", u"MAX", None))
        self.label_CurrentLaser.setText(QCoreApplication.translate("DataLogger_Profile", u"LASER\n"
"Value", None))
        self.label_MinLaser.setText(QCoreApplication.translate("DataLogger_Profile", u"MIN", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Profile_Laser), QCoreApplication.translate("DataLogger_Profile", u"Profile Laser", None))
        self.label_MinADHAT.setText(QCoreApplication.translate("DataLogger_Profile", u"MIN", None))
        self.label_CurrentADHAT.setText(QCoreApplication.translate("DataLogger_Profile", u"ADHAT\n"
"Value", None))
        self.label_MaxADHAT.setText(QCoreApplication.translate("DataLogger_Profile", u"MAX", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Profile_ADHAT), QCoreApplication.translate("DataLogger_Profile", u"Profile ADHAT", None))
        self.pushButton_ProfileView.setText(QCoreApplication.translate("DataLogger_Profile", u"MAG\n"
"View", None))
        self.pushButton_Exit.setText(QCoreApplication.translate("DataLogger_Profile", u"Exit", None))
        self.pushButton_Start_Profile.setText(QCoreApplication.translate("DataLogger_Profile", u"Start\n"
"Profile", None))
        self.pushButton_Stop_Profile.setText(QCoreApplication.translate("DataLogger_Profile", u"Stop\n"
"Profile", None))
        self.pushButton_ProfileScale.setText(QCoreApplication.translate("DataLogger_Profile", u"Profile H\n"
"Scale 10", None))
        self.label_Status.setText("")
        self.label_Error.setText("")
    # retranslateUi

