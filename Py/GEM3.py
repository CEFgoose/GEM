#!/usr/bin/env python
import os
import sys
from os import chdir
from os.path import join
import argparse
import json
import tempCSS
import subprocess
import logging
import re
from enum import Enum, auto
from datetime import datetime
from PyQt5.QtCore import QDate
import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, QSize
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QStatusBar,
    QMenuBar,
    QMenu,
    QAction,
    QRadioButton,
    QCalendarWidget
)
from PyQt5.QtWidgets import QPushButton, QMessageBox, QTabWidget


# ###### CREDITS ###### #
__author__ = "Chris Gousset"
__copyright__ = "N/A"
__credits__ = ["Louis Morales", "Zack LaVergne"]
__license__ = "N/A"
__version__ = "2.1pyi"
__maintainer__ = "Chris Gousset"
__email__ = "chris.gousset@kaart.com"
__status__ = "Development"

# ###### DEBUG STUFF ###### #
##logging.basicConfig(level=logging.DEBUG)
##logger = logging.getLogger(__name__)
##

# ###### RESOURCE PATH TO IMAGE FILES IN COMPILED APP ###### #
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# ###### IMPORT PARSER STUFF ###### #

class MapCSSParseExceptionType(Enum):
    UNKNOWN = auto()
    UNKNOWN_USER = auto()


class MapCSSParseException(Exception):
    """
    Thrown when there is an issue parsing the mapcss
    """
    
    def __init__(
        self,
        message: str,
        exception_type:
        MapCSSParseExceptionType = MapCSSParseExceptionType.UNKNOWN,
    ):
        self.exception_type = exception_type
        super().__init__(message)


# ###### ABSTRACT TABLE MODEL SETUP ###### #
class TABMOD(QAbstractTableModel):
    def __init__(
        self, GEMarray, headers=[], parent=None,
    ):
        QAbstractTableModel.__init__(self, parent)
        self.GEMarraydata = GEMarray
        self.headers = headers
        self.thumbSize = 64

    def resizePixmap(self, mult):
        self.thumbSize = self.thumbSize * mult
        self.reset()

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def rowCount(self, parent):
        return 50

    def columnCount(self, parent):
        return 4

    def data(self, index, role):
        row = index.row()
        column = index.column()
        value = self.GEMarraydata[row][column]
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if column == 0:
                try:
                    value = self.GEMarraydata[row][column]
                    self.dataChanged.emit(index, index)
                    return str(value)
                except Exception as e:
                    logger.exception(e)
            if column == 1:
                try:
                    value = self.GEMarraydata[row][column]
                    self.dataChanged.emit(index, index)
                    return str(value)
                except Exception as e:
                    logger.exception(e)
        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            column = index.column()

            if column == 2:
                pix = QtGui.QPixmap(25, 15)
                value = self.GEMarraydata[row][column]
                pix.fill(value)
                self.dataChanged.emit(index, index)
                icon = QtGui.QIcon(pix)

                return icon

            if column == 3:
                Sicon = self.GEMarraydata[row][column]
                self.dataChanged.emit(index, index)
                return Sicon

    def setData(self, index, value, role: int):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if column == 0:
                try:
                    value = self.GEMarraydata[row][column]
                    self.dataChanged.emit(index, index)
                    return str(value)
                except Exception as e:
                    logger.exception(e)
            if column == 1:
                try:
                    value = self.GEMarraydata[row][column]
                    self.dataChanged.emit(index, index)
                    return str(value)
                except Exception as e:
                    logger.exception(e)
        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            column = index.column()
            if column == 2:
                pix = QtGui.QPixmap(25, 15)
                value = self.GEMarraydata[row][column]
                pix.fill(value)

                self.dataChanged.emit(index, index)
                icon = QtGui.QIcon(pix)
                return icon
            if column == 3:
                Sicon = self.GEMarraydata[row][column]
                self.dataChanged.emit(index, index)
                return Sicon
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section < len(self.headers):
                    return self.headers[section]


# ###### GLOBAL VARIABLE SETUP ###### #

''' Here we make an instance of the abstract table model, set a boolean for the
old/new style mapcss parser and setup a clear Qcolor used to fill in the empty places of the edito table'''
Model = TABMOD
OLDSTYLE = True
clear = QtGui.QColor(0, 0, 0, 0)

# ###### EDITOR INFO CLASS SETUP ###### #

class EDITORINFO(object):
    def __init__(self):
        self.NAME = ""
        self.UID = ""
        self.USERNAME = ""
        self.TITLE = ""
        self.GITACCESS = False
        self.LINECOLORTEXT = ""
        self.NODECOLORTEXT = ""
        self.LINECOLORUI = ""
        self.NODECOLORUI = ""
        self.ICONSIZE = 10
        self.LINEWIDTH = 5
        self.ICONSHAPE = ""
        self.ICONSHAPELINK = ""

# ####### MAIN WINDOW CLASS ####### #
class MAINWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(720, 300, 700, 640)
        self.setWindowTitle("GEM - GUI Editor for Mapcss")
        self.MWHOME(self)
        self.output_file_dir = os.path.expanduser("~/Documents")

    def MWHOME(self, MAINWindow):
        self.TITLE = ""
        self.ADMINPASS = "**********"
        self.ISOLATEUSERON = False
        self.TIMECHECKON = False
        self.repoGO = False
        self.GOREMOVEALL = False
        self.CALENDAROPEN = False
        self.SEARCHDATES = ""
        self.GOREMOVEALL = False
        self.FINSHEDUSERBLOCK = ""
        self.BLOCK = ""
        self.TEAMNAMETEXT = ""
        self.SETUPENTRYBLOCK = ""
        self.SETTINGBLOCK = ""
        self.NODEENTRYBLOCK = ""
        self.WAYENTRYBLOCK = ""
        self.MASTEROUTPUTBLOCK = ""
        self.WHITE = "#FFFFFF"
        self.EDITORNODECOLORUI = "#FFFFFF"
        self.TEAMLINECOLORTEXT = "#47D608"
        self.TEAMNODECOLORTEXT = "orange"
        self.TEAMLINECOLORUI = "#47D608"
        self.TEAMNODECOLORUI = "#ffaa00"
        self.LINEWIDTH = 5
        self.ICONSIZE = 10
        self.TEAMICONSHAPE = "Circle"
        self.FOLDER = os.getcwd()
        self.NRSELECT = ""
        self.GUMSELECT = ""
        self.GUMusercount = 0
        self.usercount = 0
        self.tempcount = 1
        self.TEMPUSERS = {}
        for j in range(100):
            self.TEMPUSERS[str(j)] = 0
        self.ADDUSERS = []
        self.filters = ""
        self.select_filters = "MAPCSS (*.mapcss)"
        self.directory = os.getcwd()
        self.SELTEXT = ""
        self.TEMPEDITORICONSHAPE = ""
        self.TEMPLINECOLORTEXT = ""
        self.TEMPNODECOLORTEXT = ""
        self.GOEDIT = False


##        self.CIRCLE=("/Users/imac25/Desktop/bitmaps/circle.png")
##        self.SQUARE=("/Users/imac25/Desktop/bitmaps/square.png")
##        self.TRIANGLE =("/Users/imac25/Desktop/bitmaps/triangle.png")
##        self.PENTAGON=("/Users/imac25/Desktop/bitmaps/pentagon.png")
##        self.HEXAGON =( "/Users/imac25/Desktop/bitmaps/hexagon.png")
##        self.HEPTAGON=("/Users/imac25/Desktop/bitmaps/heptagon.png")
##        self.OCTAGON=("/Users/imac25/Desktop/bitmaps/octagon.png")
##        self.NONAGON =("/Users/imac25/Desktop/bitmaps/nonagon.png")
##        self.DECAGON=("/Users/imac25/Desktop/bitmaps/decagon.png")
##        self.KAARTICON=("/Users/imac25/Desktop/bitmaps/Kaart.png")
##        self.GEMICON=("/Users/imac25/Desktop/bitmaps/GEM3.png")         
        self.CIRCLE = resource_path('circle.png')
        self.SQUARE = resource_path('square.png')
        self.TRIANGLE = resource_path('triangle.png')
        self.PENTAGON = resource_path('pentagon.png')
        self.HEXAGON = resource_path('hexagon.png')
        self.HEPTAGON = resource_path('heptagon.png')
        self.OCTAGON = resource_path('octagon.png')
        self.NONAGON = resource_path('nonagon.png')
        self.DECAGON = resource_path('decagon.png')
        self.KAARTICON = resource_path('Kaart.png')
        self.GEMICON = resource_path('GEM3.png')


        
        self.TABS = QTabWidget(self)
        self.TABS.resize(690, 580)
        self.TABS.move(5, 55)
        self.TAB1 = QWidget()
        self.TAB2 = QWidget()
        self.TABS.addTab(self.TAB1, "GEM")
        self.PULLUSER = ""
        
 # ######## LINK BUTTONS ####### #

        self.KAARTBUTTON = QPushButton(self)
        kaart  = QtGui.QIcon(self.KAARTICON)
        self.KAARTBUTTON.setIcon(kaart)
        self.KAARTBUTTON.resize(60, 60)
        self.KAARTBUTTON.move(0, 0)
        size = QSize(40, 40) 
        self.KAARTBUTTON.setIconSize(size) 
        self.KAARTBUTTON.clicked.connect(self.KAARTBUTTON_clicked)

        self.GEMBUTTON = QPushButton(self)
        gem  = QtGui.QIcon(self.GEMICON)
        self.GEMBUTTON.setIcon(gem)
        self.GEMBUTTON.resize(60, 60)
        self.GEMBUTTON.move(55, 0)
        size = QSize(40, 40) 
        self.GEMBUTTON.setIconSize(size) 
        self.GEMBUTTON.clicked.connect(self.GEMBUTTON_clicked)        
        # ###############################TABLE BUTTONS############################## #

        self.TABLE = QtWidgets.QTableView(self.TAB1)
        self.TABLE.resize(400, 470)
        self.TABLE.move(255, 20)
        self.TABLE.clicked.connect(self.SETNR)

        self.REMOVE = QtWidgets.QPushButton(self.TAB1)
        self.REMOVE.setText("REMOVE")
        self.REMOVE.resize(110, 25)
        self.REMOVE.move(250, 490)
        self.REMOVE.clicked.connect(self.REMOVE_clicked)

        self.REMOVEALL = QPushButton(self.TAB1)
        self.REMOVEALL.setText("REMOVE ALL")
        self.REMOVEALL.resize(110, 25)
        self.REMOVEALL.move(250, 515)
        self.REMOVEALL.clicked.connect(self.REMOVEALL_clicked)

        self.EXPORT = QPushButton(self.TAB1)
        self.EXPORT.setText("EXPORT")
        self.EXPORT.resize(110, 25)
        self.EXPORT.move(350, 515)
        self.EXPORT.clicked.connect(self.EXPORT_clicked)

        self.IMPORT = QPushButton(self.TAB1)
        self.IMPORT.setText("IMPORT")
        self.IMPORT.resize(110, 25)
        self.IMPORT.move(350, 490)
        self.IMPORT.clicked.connect(self.IMPORTGO)

        self.RESTACK = QPushButton(self.TAB1)
        self.RESTACK.setText("RESTACK")
        self.RESTACK.resize(110, 25)
        self.RESTACK.move(550, 490)
        self.RESTACK.clicked.connect(self.RESTACK_clicked)

        self.ISOLATE = QPushButton(self.TAB1)
        self.ISOLATE.setText("ISOLATE")
        self.ISOLATE.resize(110, 25)
        self.ISOLATE.move(550, 515)
        self.ISOLATE.clicked.connect(self.ISOLATE_clicked)


        self.MOVEUP = QPushButton(self.TAB1)
        self.MOVEUP.setText("MOVE UP")
        self.MOVEUP.resize(110, 25)
        self.MOVEUP.move(450, 490)
        self.MOVEUP.clicked.connect(self.MOVEUP_clicked)

        self.MOVEDOWN = QPushButton(self.TAB1)
        self.MOVEDOWN.setText("MOVE DOWN")
        self.MOVEDOWN.resize(110, 25)
        self.MOVEDOWN.move(450, 515)
        self.MOVEDOWN.clicked.connect(self.MOVEDOWN_clicked)


        # ##############################TEAM SETTINGS######################## #
        self.groupBox = QtWidgets.QGroupBox(self.TAB1)

        self.groupBox.setGeometry(QtCore.QRect(5, 20, 245, 40))

        self.TEAMNAMELABEL = QtWidgets.QLabel(self.groupBox)
        self.TEAMNAMELABEL.setText("Team Name")
        self.TEAMNAMELABEL.resize(250, 20)
        self.TEAMNAMELABEL.move(10, 5)

        self.TEAMNAME = QtWidgets.QLineEdit(self.groupBox)
        self.TEAMNAME.resize(130, 20)
        self.TEAMNAME.move(105, 8)
        # ##############################HIGHLIGHT SETTINGS################### #
        self.groupBox3 = QtWidgets.QGroupBox(self.TAB1)
        self.groupBox3.setGeometry(QtCore.QRect(5, 65, 245, 120))

        self.NOTUPLOADEDLABEL = QtWidgets.QLabel(self.groupBox3)
        self.NOTUPLOADEDLABEL.setText("Highlight non-uploaded additions")
        self.NOTUPLOADEDLABEL.resize(250, 20)
        self.NOTUPLOADEDLABEL.move(10, 5)

        self.TEAMLINECOLOR = QPushButton(self.groupBox3)
        self.TEAMLINECOLOR.setText("LINE COLOR")
        self.TEAMLINECOLOR.resize(110, 25)
        self.TEAMLINECOLOR.move(3, 30)
        self.TEAMLINECOLOR.clicked.connect(self.TEAMLINECOLOR_clicked)

        self.TEAMLINECOLORICON = QtWidgets.QLabel(self.groupBox3)
        self.TEAMLINECOLORICON.move(110, 37)
        self.pix = QtGui.QPixmap(15, 15)
        self.pix.fill(QColor(self.WHITE))
        self.TEAMLINECOLORICON.setPixmap(self.pix)

        self.LINEWIDTHLABEL = QtWidgets.QLabel(self.groupBox3)
        self.LINEWIDTHLABEL.setText("Line Width")
        self.LINEWIDTHLABEL.resize(250, 20)
        self.LINEWIDTHLABEL.move(130, 34)

        self.TEAMLINEWIDTHSPIN = QtWidgets.QSpinBox(self.groupBox3)
        self.TEAMLINEWIDTHSPIN.setRange(1, 20)
        self.TEAMLINEWIDTHSPIN.setValue(self.LINEWIDTH)
        self.TEAMLINEWIDTHSPIN.move(200, 34)

        self.TEAMNODECOLOR = QPushButton(self.groupBox3)
        self.TEAMNODECOLOR.setText("NODE COLOR")
        self.TEAMNODECOLOR.resize(110, 25)
        self.TEAMNODECOLOR.move(3, 55)
        self.TEAMNODECOLOR.clicked.connect(self.TEAMNODECOLOR_clicked)

        self.TEAMNODECOLORICON = QtWidgets.QLabel(self.groupBox3)
        self.TEAMNODECOLORICON.move(110, 62)
        self.pix = QtGui.QPixmap(15, 15)
        self.pix.fill(QColor(self.WHITE))
        self.TEAMNODECOLORICON.setPixmap(self.pix)

        self.ICONSIZELABEL = QtWidgets.QLabel(self.groupBox3)
        self.ICONSIZELABEL.setText("Node Size")
        self.ICONSIZELABEL.resize(250, 20)
        self.ICONSIZELABEL.move(130, 59)

        self.TEAMICONSIZESPIN = QtWidgets.QSpinBox(self.groupBox3)
        self.TEAMICONSIZESPIN.setRange(10, 50)
        self.TEAMICONSIZESPIN.setValue(self.ICONSIZE)
        self.TEAMICONSIZESPIN.move(200, 60)

        self.ICONSHAPELABEL = QtWidgets.QLabel(self.groupBox3)
        self.ICONSHAPELABEL.setText("Node Shape:")
        self.ICONSHAPELABEL.resize(250, 20)
        self.ICONSHAPELABEL.move(10, 84)

        self.TEAMNODESHAPEICON = QtWidgets.QPushButton(self.groupBox3)
        self.TEAMNODESHAPEICON.move(90, 80)
        self.TEAMNODESHAPEICON.resize(35, 30)


        self.TEAMICONSHAPEBOX = QtWidgets.QPushButton(self.groupBox3)
        self.TEAMICONSHAPEBOX.resize(130, 25)
        self.TEAMICONSHAPEBOX.setText("SELECT SHAPE")
        self.TEAMICONSHAPEBOX.move(115
                                   , 80)
        self.TEAMICONSHAPEBOX.clicked.connect(lambda: self.EDITORSHAPESELECT("TEAM"))
        # ##############################EDITOR SETTINGS###################### #

        self.groupBox2 = QtWidgets.QGroupBox(self.TAB1)
        self.groupBox2.setGeometry(QtCore.QRect(5, 190, 245, 220))

        self.EDITSETTINGSLABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITSETTINGSLABEL.setText("Editor Settings:")
        self.EDITSETTINGSLABEL.resize(250, 20)
        self.EDITSETTINGSLABEL.move(10, 5)

        self.EDITNAMELABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITNAMELABEL.setText("Editor Name")
        self.EDITNAMELABEL.resize(250, 20)
        self.EDITNAMELABEL.move(10, 25)

        self.EDITORNAME = QtWidgets.QLineEdit(self.groupBox2)
        self.EDITORNAME.resize(130, 20)
        self.EDITORNAME.move(105, 25)

        self.EDITIDLABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITIDLABEL.setText("Editor User ID")
        self.EDITIDLABEL.resize(250, 20)
        self.EDITIDLABEL.move(10, 50)

        self.EDITORID = QtWidgets.QLineEdit(self.groupBox2)
        self.EDITORID.resize(130, 20)
        self.EDITORID.move(105, 50)

        self.ADD = QPushButton(self.groupBox2)
        self.ADD.setText("ADD")
        self.ADD.resize(80, 25)
        self.ADD.move(5, 75)
        self.ADD.clicked.connect(self.ADD_clicked)

        self.CLEAR = QPushButton(self.groupBox2)
        self.CLEAR.setText("CLEAR")
        self.CLEAR.resize(80, 25)
        self.CLEAR.move(83, 75)
        self.CLEAR.clicked.connect(self.CLEAR_clicked)

        self.EDIT = QPushButton(self.groupBox2)
        self.EDIT.setText("EDIT")
        self.EDIT.resize(80, 25)
        self.EDIT.move(160, 75)
        self.EDIT.clicked.connect(self.EDIT_clicked)

        self.EDITORLINECOLOR = QPushButton(self.groupBox2)
        self.EDITORLINECOLOR.setText("LINE COLOR")
        self.EDITORLINECOLOR.resize(110, 25)
        self.EDITORLINECOLOR.move(5, 105)
        self.EDITORLINECOLOR.clicked.connect(self.EDITORLINECOLOR_clicked)

        self.EDITORLINECOLORICON = QtWidgets.QLabel(self.groupBox2)
        self.EDITORLINECOLORICON.move(115, 112)
        self.pix = QtGui.QPixmap(15, 15)
        self.pix.fill(QColor(self.WHITE))
        self.EDITORLINECOLORICON.setPixmap(self.pix)

        self.EDITORLINEWIDTHLABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITORLINEWIDTHLABEL.setText("Line Width")
        self.EDITORLINEWIDTHLABEL.resize(75, 20)
        self.EDITORLINEWIDTHLABEL.move(135, 110)

        self.EDITORLINEWIDTHSPIN = QtWidgets.QSpinBox(self.groupBox2)
        self.EDITORLINEWIDTHSPIN.setRange(1, 20)
        self.EDITORLINEWIDTHSPIN.setValue(self.LINEWIDTH)
        self.EDITORLINEWIDTHSPIN.move(200, 110)

        self.EDITORNODECOLOR = QPushButton(self.groupBox2)
        self.EDITORNODECOLOR.setText("NODE COLOR")
        self.EDITORNODECOLOR.resize(110, 25)
        self.EDITORNODECOLOR.move(5, 134)
        self.EDITORNODECOLOR.clicked.connect(self.EDITORNODECOLOR_clicked)

        self.EDITORNODECOLORICON = QtWidgets.QLabel(self.groupBox2)
        self.EDITORNODECOLORICON.move(115, 141)
        self.pix = QtGui.QPixmap(15, 15)
        self.pix.fill(QColor(self.WHITE))
        self.EDITORNODECOLORICON.setPixmap(self.pix)

        self.EDITORNODESIZELABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITORNODESIZELABEL.setText("Node Size")
        self.EDITORNODESIZELABEL.resize(75, 20)
        self.EDITORNODESIZELABEL.move(135, 137)

        self.EDITORNODESIZESPIN = QtWidgets.QSpinBox(self.groupBox2)
        self.EDITORNODESIZESPIN.setRange(10, 50)
        self.EDITORNODESIZESPIN.setValue(10)
        self.EDITORNODESIZESPIN.move(200, 137)

        self.TOGGLELABEL = QtWidgets.QLabel(self.groupBox2)
        self.TOGGLELABEL.setText("Toggle UID in Style Settings menu")
        self.TOGGLELABEL.resize(250, 15)
        self.TOGGLELABEL.move(12, 165)

        self.TOGGLECHECK = QtWidgets.QCheckBox(self.groupBox2)
        self.TOGGLECHECK.move(220, 165)

        self.EDITORICONSHAPELABEL = QtWidgets.QLabel(self.groupBox2)
        self.EDITORICONSHAPELABEL.setText("Node Shape:")
        self.EDITORICONSHAPELABEL.resize(250, 20)
        self.EDITORICONSHAPELABEL.move(12, 190)

        self.EDITORNODESHAPEICON = QtWidgets.QPushButton(self.groupBox2)
        self.EDITORNODESHAPEICON.move(90, 185)
        self.EDITORNODESHAPEICON.resize(35, 30)


        self.EDITORICONSHAPEBOX = QtWidgets.QPushButton(self.groupBox2)
        self.EDITORICONSHAPEBOX.resize(130, 25)
        self.EDITORICONSHAPEBOX.setText("SELECT SHAPE")
        self.EDITORICONSHAPEBOX.move(115, 185)
        self.EDITORICONSHAPEBOX.clicked.connect(lambda: self.EDITORSHAPESELECT("EDITOR"))

## ################ TIME SEARCH ############### ##
        self.TIMEBox = QtWidgets.QGroupBox(self.TAB1)
        self.TIMEBox.setGeometry(QtCore.QRect(5, 415, 245, 128))
  
        self.TIMESEARCHLABEL = QtWidgets.QLabel(self.TIMEBox)
        self.TIMESEARCHLABEL.setText("Time Search:")
        self.TIMESEARCHLABEL.resize(250, 20)
        self.TIMESEARCHLABEL.move(12, 5)
        
        self.STARTDATELABEL = QtWidgets.QLabel(self.TIMEBox)
        self.STARTDATELABEL.setText("Start Date:")
        self.STARTDATELABEL.resize(250, 20)
        self.STARTDATELABEL.move(12, 30)
        
        self.STARTDATE = QtWidgets.QLineEdit(self.TIMEBox)
        self.STARTDATE.resize(120, 20)
        self.STARTDATE.setText("")
        self.STARTDATE.move(95, 30)

        self.STARTDATESELECT =QRadioButton(self.TIMEBox)
        self.STARTDATESELECT.move(222, 31)

        self.ENDDATELABEL = QtWidgets.QLabel(self.TIMEBox)
        self.ENDDATELABEL.setText("End Date:")
        self.ENDDATELABEL.resize(250, 20)
        self.ENDDATELABEL.move(12, 55)
        
        self.ENDDATE = QtWidgets.QLineEdit(self.TIMEBox)
        self.ENDDATE.resize(120, 20)
        self.ENDDATE.setText("")
        self.ENDDATE.move(95, 55)

        self.ENDDATESELECT =QRadioButton(self.TIMEBox)
        self.ENDDATESELECT.move(222, 56)
           
        self.SET = QPushButton(self.TIMEBox)
        self.SET.setText("SET DATES")
        self.SET.resize(125, 25)
        self.SET.move(0,75)
        self.SET.clicked.connect(self.SETSEARCHDATES)
        
        self.RESET = QPushButton(self.TIMEBox)
        self.RESET.setText("CLEAR DATES")
        self.RESET.resize(125, 25)
        self.RESET.move(120, 75)
        self.RESET.clicked.connect(self.CLEARSEARCHDATES)
                
        self.CAL = QPushButton(self.TIMEBox)
        self.CAL.setText("OPEN CALENDAR")
        self.CAL.resize(155, 25)
        self.CAL.move(90, 1)
        self.CAL.clicked.connect(self.CHOOSEDATE)


        self.TIMETOGGLELABEL = QtWidgets.QLabel(self.TIMEBox)
        self.TIMETOGGLELABEL.setText("Toggle Timestamp Search on/off:")
        self.TIMETOGGLELABEL.resize(250, 20)
        self.TIMETOGGLELABEL.move(12, 100)

        self.TIMECHECK =  QtWidgets.QCheckBox(self.TIMEBox)
        self.TIMECHECK.move(222, 102)
        self.TIMECHECK.toggled.connect(self.TIMECHECKTOGGLED)


        self.retranslateUi(MAINWindow)

        # ####################### RETRANSLATE UI ########################## #

    def retranslateUi(self, MAINWindow):

        self.GEMheaders = [
            "NAME ",
            "UID ",
            "LINE COLOR",
            "NODE ",
        ]
        self.rowcount = 50
        self.colcount = 4
        self.GEMarray = [
            [str(""), str(""), QtGui.QColor(clear), QtGui.QColor(clear),
             ]
            for j in range(self.rowcount)
        ]
        self.tablemodel = Model(self.GEMarray, self.GEMheaders, self)
        self.TABLE.setModel(self.tablemodel)
        self.TABLE.resizeRowsToContents()
        self.TABLE.resizeColumnsToContents()

    # ######################## RESORUCE PATH TO IMAGE FILES IN COMPILED APP #################### #
    def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception as e:
            logger.exception(e)
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    # ###### CLOSE EVENT ###### #
    def closeEvent(self, event):
        self.ISOLATEUSERON = False
        self.TIMECHECKON = False
        try:
            self.EXPORT_clicked()
        except:
                pass
        self.setParent(None)
        self.deleteLater()
        self.close()
# ####### LINK BUTTONS ######## #

    def KAARTBUTTON_clicked(self):
        url = ("http://kaartgroup.com/")
        if sys.platform=='win32':
            os.startfile(url)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', url])
        else:
            try:
                subprocess.Popen(['xdg-open', url])
            except OSError:
               pass

    def GEMBUTTON_clicked(self):
        url = ("https://gem.kaart.com/")
        if sys.platform=='win32':
            os.startfile(url)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', url])
        else:
            try:
                subprocess.Popen(['xdg-open', url])
            except OSError:
               pass
        
# ######### TIME SEARCH FUNCTIONS ######## #
    def CHOOSEDATE(self):
        if self.CALENDAROPEN == False:
            self.CAL.setText("CLOSE CALANDER")
            self.calendar = QCalendarWidget(self)
            self.calendar.move(260, 380)
            self.calendar.resize(300, 200)
            self.calendar.setGridVisible(True)
            self.calendar.show()
            self.calendar.clicked.connect(self.SETSTARTDATE)
            self.CALENDAROPEN = True
            self.TAB1.repaint()
        else:
            self.calendar.close()
            self.CAL.setText("OPEN CALANDER")
            self.CALENDAROPEN = False
            self.TAB1.repaint()


        
    def SETSTARTDATE(self,qDate):
        MONTH = qDate.month()
        DAY = qDate.day()
        if MONTH < 10:
            MONTH = "0%s"%(MONTH)
        if DAY < 10:
            DAY = "0%s"%(DAY)
        if self.STARTDATESELECT.isChecked():
              self.STARTDATE.setText('{0}-{1}-{2}'.format(qDate.year(), MONTH, DAY))
              self.STARTDATE.repaint()
        elif self.ENDDATESELECT.isChecked():
              self.ENDDATE.setText('{0}-{1}-{2}'.format(qDate.year(), MONTH, DAY))
              self.ENDDATE.repaint()
              
    def SETSEARCHDATES(self):
        if self.STARTDATE.text()!= "":
            if self.ENDDATE.text()!= "":
                self.SEARCHDATES  = ("%s/%s"%(self.STARTDATE.text(),self.ENDDATE.text()))
            else:
                self.SEARCHDATES = "%s/"%(self.STARTDATE.text())
        else:
            pass

    def CLEARSEARCHDATES(self):
        self.SEARCHDATES = ""
        self.STARTDATE.setText("")
        self.STARTDATE.repaint()
        self.ENDDATE.setText("")
        self.ENDDATE.repaint()
        self.STARTDATESELECT.setChecked(False)
        self.STARTDATESELECT.repaint()
        self.ENDDATESELECT.setChecked(False)
        self.ENDDATESELECT.repaint()
        





        

    # ########################   GEM: EDITOR FUNCTIONS   ###################### #
    def TIMECHECKTOGGLED(self):
        if self.TIMECHECK.isChecked():
            self.TIMECHECKON = True
            self.EXPORT_clicked()
        else:
            self.TIMECHECKON = False
            self.EXPORT_clicked()
    
    def ISOLATE_clicked(self):
       if self.NRSELECT != "":
           if self.ISOLATEUSERON == True:
                self.ISOLATEUSERON = False
                self.SHOWUSER = ""
                self.ISOLATE.setText("ISOLATE")
                self.ISOLATE.repaint()
                self.EXPORT_clicked()
           else:
               self.SHOWUSER = self.TEMPUSERS[str(self.NRSELECT)]
               self.ISOLATEUSERON = True
               self.ISOLATE.setText("SHOW ALL")
               self.ISOLATE.repaint()
               self.EXPORT_clicked()

    '''
    RESTACK clears the editor table, creates a temporary dict called restack users, then itterates through
    the tempusers array. Tempusers still contains empty slots where the user may have removed editors from the
    table, so restack checks each item in tempusers to make sure it isn't an empty value,
    then repopulates all values from every valid editor instance into back into the editor table,
    then each valid editor instance is added to the restackusers dict. At the end of the itteration,
    tempusers is cleared and replaced with the values from restackusers (which now contains no empty values)
    '''
    def RESTACK_clicked(self):
        for i in range(50):
            self.GEMarray[i][0] = ""
            self.GEMarray[i][1] = ""
            self.GEMarray[i][2] = clear
            self.GEMarray[i][3] = clear
            count = 0
            self.RESTACKUSERS = {}
        for i in self.TEMPUSERS.values():
            if i != "" and type(i) != int:
                self.GEMarray[count][0] = i.NAME
                self.GEMarray[count][1] = i.UID
                self.GEMarray[count][2] = i.LINECOLORUI
                self.GEMarray[count][3] = i.icon
                self.RESTACKUSERS[str(count)] = i
                count += 1
                self.usercount = count
        self.TEMPUSERS = {}
        self.TEMPUSERS = self.RESTACKUSERS


    '''
    MOVEUP defines the selected cell and corresponding editor instance as "MOVEFROM"
    and the cell above it as "MOVETO".
    It then checks to see if the "MOVETO" cell is in the tempusers dict,
    in order to determine if it is an empty cell in the table or not.
    If the MOVETO cell is empty, all "MOVEFROM" editor info is moved to the MOVETO line in the table
    and that editors instance is moved to the corresopnding index of the tempusers array.
    If the MOVETO cell is not empty, then the table and array positions of the two editor
    instances in question are swapped with each other.
    '''
    def MOVEUP_clicked(self):
        if self.NRSELECT != "":
            MOVETO = int(int(self.NRSELECT) - 1)
            MOVEFROM = int(self.NRSELECT)
            if MOVETO != int(-1):
                if str(MOVETO) in self.TEMPUSERS.keys():
                    if self.TEMPUSERS[str(MOVETO)] == 0:
                        self.GEMarray[(MOVETO)][0] = self.TEMPUSERS[
                            str(MOVEFROM)
                        ].NAME
                        self.GEMarray[(MOVETO)][1] = self.TEMPUSERS[
                            str(MOVEFROM)
                        ].UID
                        self.GEMarray[(MOVETO)][2] = self.TEMPUSERS[
                            str(MOVEFROM)
                        ].LINECOLORUI
                        self.GEMarray[(MOVETO)][3] = self.TEMPUSERS[
                            str(MOVEFROM)
                        ].icon
                        self.GEMarray[(MOVEFROM)][0] = ""
                        self.GEMarray[(MOVEFROM)][1] = ""
                        self.GEMarray[(MOVEFROM)][2] = clear
                        self.GEMarray[(MOVEFROM)][3] = clear
                        self.TEMPUSERS[str(MOVETO)] = self.TEMPUSERS[str(MOVEFROM)]
                        self.TEMPUSERS[str(MOVEFROM)] = 0
                        self.SETNR()

                    else:
                        if str(MOVEFROM) in self.TEMPUSERS.keys():
                            self.MOVETOUSER = self.TEMPUSERS[str(MOVEFROM)]
                            self.MOVEFROMUSER = self.TEMPUSERS[str(MOVETO)]
                            self.GEMarray[(MOVEFROM)][0] = self.MOVEFROMUSER.NAME
                            self.GEMarray[(MOVEFROM)][1] = self.MOVEFROMUSER.UID
                            self.GEMarray[(MOVEFROM)][
                                2
                            ] = self.MOVEFROMUSER.LINECOLORUI
                            self.GEMarray[(MOVEFROM)][3] = self.MOVEFROMUSER.icon
                            self.GEMarray[(MOVETO)][0] = self.MOVETOUSER.NAME
                            self.GEMarray[(MOVETO)][1] = self.MOVETOUSER.UID
                            self.GEMarray[(MOVETO)][2] = self.MOVETOUSER.LINECOLORUI
                            self.GEMarray[(MOVETO)][3] = self.MOVETOUSER.icon
                            self.TEMPUSERS[str(MOVETO)] = self.MOVETOUSER
                            self.TEMPUSERS[str(MOVEFROM)] = self.MOVEFROMUSER
                            self.SETNR()


    '''
    MOVEDOWN works the same way as MOVEUP but in reverse.
    '''
    def MOVEDOWN_clicked(self):
        if self.NRSELECT != "":
            MOVETO = int(int(self.NRSELECT) + 1)
            MOVEFROM = int(self.NRSELECT)

            if str(MOVETO) in self.TEMPUSERS.keys():
                if self.TEMPUSERS[str(MOVETO)] == 0:
                    self.GEMarray[(MOVETO)][0] = self.TEMPUSERS[str(MOVEFROM)].NAME
                    self.GEMarray[(MOVETO)][1] = self.TEMPUSERS[str(MOVEFROM)].UID
                    self.GEMarray[(MOVETO)][2] = self.TEMPUSERS[
                        str(MOVEFROM)
                    ].LINECOLORUI
                    self.GEMarray[(MOVETO)][3] = self.TEMPUSERS[str(MOVEFROM)].icon
                    self.GEMarray[(MOVEFROM)][0] = ""
                    self.GEMarray[(MOVEFROM)][1] = ""
                    self.GEMarray[(MOVEFROM)][2] = clear
                    self.GEMarray[(MOVEFROM)][3] = clear
                    self.TEMPUSERS[str(MOVETO)] = self.TEMPUSERS[str(MOVEFROM)]
                    self.TEMPUSERS[str(MOVEFROM)] = 0
                    self.SETNR()
                else:
                    self.MOVETOUSER = self.TEMPUSERS[str(MOVEFROM)]
                    self.MOVEFROMUSER = self.TEMPUSERS[str(MOVETO)]
                    self.GEMarray[(MOVEFROM)][0] = self.MOVEFROMUSER.NAME
                    self.GEMarray[(MOVEFROM)][1] = self.MOVEFROMUSER.UID
                    self.GEMarray[(MOVEFROM)][2] = self.MOVEFROMUSER.LINECOLORUI
                    self.GEMarray[(MOVEFROM)][3] = self.MOVEFROMUSER.icon
                    self.GEMarray[(MOVETO)][0] = self.MOVETOUSER.NAME
                    self.GEMarray[(MOVETO)][1] = self.MOVETOUSER.UID
                    self.GEMarray[(MOVETO)][2] = self.MOVETOUSER.LINECOLORUI
                    self.GEMarray[(MOVETO)][3] = self.MOVETOUSER.icon
                    self.TEMPUSERS[str(MOVETO)] = self.MOVETOUSER
                    self.TEMPUSERS[str(MOVEFROM)] = self.MOVEFROMUSER
                    self.SETNR()
    '''
    EDITORLINECOLOR opens the hex color picker dialog. "color.name" to my knowledge the only way to
    get the hex value of the chosen color string format, however it is returned
    as an array of comma seprated characters, hence "colr += str(i)"to reconstruct it into a usable string.
    The pyqt5 can accept the natve color picker output "color" as a Qcolor for the editor table,
    however a string version of the hex color value is also needed for the final .Mapcss output.
    If no new color is chosen and the picker closed, the picker returns the value of the color black, so the line
    "if colr != "#000000":" checks to see if a new color was actually chosen bbefore changing the color values
    in the table and editor array.
    All of the color picker functions work in this way.
    '''
    def EDITORLINECOLOR_clicked(self):
        color = QtWidgets.QColorDialog.getColor()
        clr = color.name()
        colr = ""
        for i in clr:
            colr += str(i)

        if colr != "#000000":
            if self.NRSELECT != "":
                self.TEMPUSERS[str(self.NRSELECT)].LINECOLORTEXT = colr
                self.TEMPUSERS[str(self.NRSELECT)].LINECOLORUI = color
                self.pix.fill(QColor(self.TEMPUSERS[str(self.NRSELECT)].LINECOLORUI))
                self.EDITORLINECOLORICON.setPixmap(self.pix)
                self.GEMarray[self.NRSELECT][2] = QtGui.QColor(
                    self.TEMPUSERS[str(self.NRSELECT)].LINECOLORUI
                )
            else:
                self.TEMPLINECOLORTEXT = colr
                self.TEMPLINECOLORUI = color
                self.pix.fill(QColor(self.TEMPLINECOLORUI))
                self.EDITORLINECOLORICON.setPixmap(self.pix)
                self.EDITORLINECOLORICON.repaint()

    def EDITORNODECOLOR_clicked(self):
        color = QtWidgets.QColorDialog.getColor()
        clr = color.name()
        colr = ""
        for i in clr:
            colr += str(i)
        if colr != "#000000":
            if self.NRSELECT != "":
                self.TEMPUSERS[str(self.NRSELECT)].NODECOLORTEXT = colr
                self.TEMPUSERS[str(self.NRSELECT)].NODECOLORUI = color
                self.pix.fill(QColor(self.TEMPUSERS[str(self.NRSELECT)].NODECOLORUI))
                self.EDITORNODECOLORICON.setPixmap(self.pix)
                self.EDITORNODECOLORDISPLAY(self.NRSELECT)

            else:
                self.TEMPNODECOLORTEXT = colr
                self.TEMPNODECOLORUI = color
                self.pix.fill(QColor(self.TEMPNODECOLORUI))
                self.EDITORNODECOLORICON.setPixmap(self.pix)
                self.EDITORNODECOLORICON.repaint()

    # ###########################   TEAM FUNCTIONS   #############################

    def TEAMLINECOLOR_clicked(self):
        color = QtWidgets.QColorDialog.getColor()

        clr = color.name()
        colr = ""
        for i in clr:
            colr += str(i)
        if colr != "#000000":
            self.TEAMLINECOLORTEXT = colr
            self.TEAMLINECOLORUI = color
            self.pix.fill(QColor(self.TEAMLINECOLORUI))
            self.TEAMLINECOLORICON.setPixmap(self.pix)

    def TEAMNODECOLOR_clicked(self):
        color = QtWidgets.QColorDialog.getColor()
        clr = color.name()
        colr = ""
        for i in clr:
            colr += str(i)
        if colr != "#000000":
            self.TEAMNODECOLORTEXT = colr
            self.TEAMNODECOLORUI = color
            self.pix.fill(QColor(self.TEAMNODECOLORUI))
            self.TEAMNODECOLORICON.setPixmap(self.pix)
    '''
    ADD creates a new editor instance from the values entered in the editor info field,
    then adds that instance to the editor array and updates the editor table with the new information.
    ADD and UPDATE share the same button, the line (if self.NRSELECT == "":)
    determines if an exisitng editor has been selected. If an existing editor is selected,
    it will use the UPDATE (lower) half of the function, and no editor on the table is selected,
    it will use the ADD (upper) half of the function.
    '''
    def ADD_clicked(self):
# ###### ADD ###### #
        if self.NRSELECT == "":
            'retrieve editor name and uid from text fields'
            ENAME = self.EDITORNAME.text()
            ENAME = ENAME.strip()
            EUID = self.EDITORID.text()
            EUID = EUID.strip()
            '''use .strip to make sure they are valid string values,
               and if they pass, create a editor instance by that editor name. '''
            if ENAME and EUID.strip():
                ECLASS = EDITORINFO()
                ECLASS.NAME = ENAME
                ECLASS.UID = EUID
                '''use the same method to check if line, node color & shape have been selected for the
                new user. If no new colors or shapes are chosen, default values for new editors are entered
                '''
                if self.TEMPLINECOLORTEXT.strip():
                    ECLASS.LINECOLORTEXT = self.TEMPLINECOLORTEXT
                    ECLASS.LINECOLORUI = self.TEMPLINECOLORUI
                else:
                    ECLASS.LINECOLORTEXT = "#b600ff"
                    ECLASS.LINECOLORUI = QColor(ECLASS.LINECOLORTEXT)


                if self.TEMPNODECOLORTEXT.strip():
                    ECLASS.NODECOLORTEXT = self.TEMPNODECOLORTEXT
                    ECLASS.NODECOLORUI = QColor(self.TEMPNODECOLORUI)
                else:
                    ECLASS.NODECOLORTEXT = "#4648ff"
                    ECLASS.NODECOLORUI = QColor("#4648ff")

                if self.TEMPEDITORICONSHAPE.strip():

                    ECLASS.ICONSHAPE = self.TEMPEDITORICONSHAPE
                else:
                    ECLASS.ICONSHAPE = "circle"
                    
                ECLASS.LINEWIDTH = str(self.EDITORLINEWIDTHSPIN.value())
                ECLASS.ICONSIZE = str(self.EDITORNODESIZESPIN.value())

                '''
                check that the current usercount matches the tempuser array count,
                then add one to the count so that the new info will be placed
                in the bottom most open line of the editor table. if there are no keys in the tempuser array,
                we know the table is empty, so we can add the new info to the first line of the editor table
                and the first position in the tempusers array (0).
                '''
                if str(self.usercount) in self.TEMPUSERS.keys():
                    if self.TEMPUSERS[str(self.usercount)] != 0:
                        self.usercount += 1
         
                'Add the new info to the appropriate position in the editor table and tempuser array'

                self.TEMPUSERS[str(self.usercount)] = ECLASS
                self.GEMarray[self.usercount][0] = str(ECLASS.NAME)
                self.GEMarray[self.usercount][1] = str(ECLASS.UID)
                self.GEMarray[self.usercount][2] = QColor(ECLASS.LINECOLORUI)
                '''
                 call the EDITORNODECOLORDISPLAY function,
                 which repaints the corresponding QIcons in the editor table
                 with the newly selected color value.
                '''
                self.EDITORNODECOLORDISPLAY((self.usercount))
                'Add the new editor instance to the addusers array for later export'
                self.ADDUSERS.append(ECLASS)
                'clear the entry fields in the editor section after adding them to the table'
                self.EDITORNAME.setText("")
                self.EDITORID.setText("")
                self.EDITORNAME.repaint()
                self.EDITORID.repaint()
                'add one to the usercount so the next entry will go into the next open line in the table'
                self.usercount += 1
                ' clear the colors displayed in the editor info entry field'
                self.pix.fill(QColor(self.WHITE))
                self.EDITORNODECOLORICON.setPixmap(self.pix)
                self.EDITORLINECOLORICON.setPixmap(self.pix)
                self.EDITORNODECOLORICON.repaint()
                self.EDITORLINECOLORICON.repaint()
                shape = QtGui.QIcon("")
                self.EDITORNODESHAPEICON.setIcon(shape)
                self.EDITORNODESHAPEICON.repaint()
                ECLASS=""
                self.TEMPEDITORICONSHAPE=""
                self.TEMPLINECOLORTEXT = ""
                self.TEMPNODECOLORTEXT = ""
                self.TABLE.resizeColumnsToContents()
                self.TABLE.resizeRowsToContents()
# ###### UPDATE ###### #
        '''
        if NRSELECT is not a null value, then we know it is an existing editor being updated.
        The only difference from ADD is that we simply update the chosen line of the editor table
        as well as the tempuser and ADDUSER arrays with the new selected values. When the update is complete,
        the button text is reset to "ADD" which is the default.
        '''
        if self.NRSELECT != "":
            ENAME = self.EDITORNAME.text()
            ENAME = ENAME.strip()
            EUID = self.EDITORID.text()
            EUID = EUID.strip()
            if ENAME and EUID.strip():
                self.TEMPUSERS[str(self.EDITORSELECT)].NAME = ENAME
                self.TEMPUSERS[str(self.EDITORSELECT)].UID = EUID
##                self.TEMPUSERS[
##                    str(self.EDITORSELECT)
##                ].ICONSHAPE = self.EDITORICONSHAPEBOX.currentText()
                self.TEMPUSERS[str(self.EDITORSELECT)].LINEWIDTH = str(
                    self.EDITORLINEWIDTHSPIN.value()
                )
                self.TEMPUSERS[str(self.EDITORSELECT)].ICONSIZE = str(
                    self.EDITORNODESIZESPIN.value()
                )

                if self.GOEDIT is True:
                    self.GEMarray[self.EDITORSELECT][0] = str(
                        self.TEMPUSERS[str(self.EDITORSELECT)].NAME
                    )
                    self.GEMarray[self.EDITORSELECT][1] = str(
                        self.TEMPUSERS[str(self.EDITORSELECT)].UID
                    )
                    self.EDITORNODECOLORDISPLAY(self.EDITORSELECT)
                else:
                    self.GEMarray[self.usercount][0] = str(
                        self.TEMPUSERS[str(self.EDITORSELECT)].NAME
                    )
                    self.GEMarray[self.usercount][1] = str(
                        self.TEMPUSERS[str(self.EDITORSELECT)].UID
                    )
                    self.EDITORNODECOLORDISPLAY((self.usercount))

                self.EDITORNAME.setText("")
                self.EDITORID.setText("")
                self.EDITORNAME.repaint()
                self.EDITORID.repaint()
                self.NRSELECT = ""
                self.EDITORSELECT = None
                self.ADD.setText("ADD")
                self.pix.fill(QColor(self.WHITE))
                shape = QtGui.QIcon("")
                self.EDITORNODESHAPEICON.setIcon(shape)
                self.EDITORNODESHAPEICON.repaint()
                self.EDITORNODECOLORICON.setPixmap(self.pix)
                self.EDITORLINECOLORICON.setPixmap(self.pix)
                self.EDITORLINECOLORICON.repaint()
                self.EDITORNODECOLORICON.repaint()
                self.TABLE.resizeColumnsToContents()
                self.TABLE.resizeRowsToContents()
                self.NRSELECT = ""
                self.EXPORT_clicked()
   

    def GETEDITORSHAPETEXT(self):
        '''
        on EDIT, The GETEDITORSHAPETEXT finds the node highlight shape for the selected editor in the table
        and sets the QComboBox in the editor info field to the corresponding value
        '''       
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "circle":
            self.EDITORICONSHAPEBOX.setCurrentIndex(0)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "triangle":
            self.EDITORICONSHAPEBOX.setCurrentIndex(1)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "square":
            self.EDITORICONSHAPEBOX.setCurrentIndex(2)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "pentagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(3)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "hexagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(4)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "heptagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(5)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "octagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(6)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "nonagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(7)
            self.EDITORICONSHAPEBOX.repaint()
        if self.TEMPUSERS[str(self.NRSELECT)].ICONSHAPE == "decagon":
            self.EDITORICONSHAPEBOX.setCurrentIndex(8)
            self.EDITORICONSHAPEBOX.repaint()


# ###### SELECTORS ###### #
    '''
    These functions are self explanitory. They connect to the signal from the corresponding combo boxes and
    set new node highlight shapes for the team or editor based on the new selection.
    '''
    def TEAMSHAPESELECT(self):
        self.TEAMICONSHAPE = self.TEAMICONSHAPEBOX.currentText()

    def EDITORSHAPESELECT(self,SELECT):
        self.dialog =  EDITORiconWindow(SELECT)
        self.dialog.show()
        
    # ############################   EXPORT BLOCK   ############################ #

    
    def EXPORT_clicked(self):
      if self.TEAMNAME.text() != "":
        self.RESTACK_clicked()
        self.ADDUSERS = []
        if self.ISOLATEUSERON == True:
            self.ADDUSERS.append(self.SHOWUSER)
        else:    
            for i in self.TEMPUSERS.values():
                self.ADDUSERS.append(i)
        'retrieve a few more values we need from the appropriate entry fields'
        
        self.ICONSIZE = str(self.TEAMICONSIZESPIN.value())
        self.LINEWIDTH = str(self.TEAMLINEWIDTHSPIN.value())
        self.TEAMNAMETEXT = str(self.TEAMNAME.text())
        
        'set the file name for the new export and meta block title using the corresponding team name'
        
        self.FILENAME = str("Kaart_QC_%s.mapcss"%(self.TEAMNAMETEXT))
        self.TITLE = "QC Styles For %s Team"%(self.TEAMNAMETEXT)

        'Use regexs to find the appropriate placeholder variables int he templateCSS blocks'
        
        FINDUSERNAME = re.compile('(?:|)USERNAME(?:|\W)')
        FINDUSERID = re.compile('(?:|)USERID(?:|\W)')
        FINDUSERNODESIZE = re.compile('(?:|)USERNODESIZE(?:|\W)')
        FINDUSERNODECOLOR = re.compile('(?:|)USERNODECOLOR(?:|\W)')
        FINDUSERNODESHAPE = re.compile('(?:|)USERNODESHAPE(?:|\W)')
        FINDUSERWAYWIDTH = re.compile('(?:|)USERWAYWIDTH(?:|\W)')
        FINDUSERWAYCOLOR = re.compile('(?:|)USERWAYCOLOR(?:|\W)')
        
        FINDNOTUPNODESIZE = re.compile('(?:|)NOTUPNODESIZE(?:|\W)')
        FINDNOTUPNODECOLOR = re.compile('(?:|)NOTUPNODECOLOR(?:|\W)')
        
        FINDNOTUPNODESHAPE = re.compile('(?:|)NOTUPNODESHAPE(?:|\W)')
        FINDNOTUPWAYCOLOR = re.compile('(?:|)NOTUPWAYCOLOR(?:|\W)')
        FINDNOTUPWAYWIDTH = re.compile('(?:|)NOTUPWAYWIDTH(?:|\W)')
        FINDTIMESEARCH = re.compile('(?:|)SEARCHTIME(?:|\W)')
        FINDTITLE = re.compile('(?:|)TITLE(?:|\W)')

        '''
        itterate through the ADDUSERS array,
        using the previously compiled regexes to sub out the placeholder variables in the template css blocks
        with each editor's indivisual settings 
        '''

        if self.TIMECHECKON ==True:
            for i in self.ADDUSERS:
                if self.TOGGLECHECK.isChecked():
                    i.USERBLOCK = re.sub(FINDUSERNAME, i.NAME, tempCSS.TOGGLEDTIMESEARCHBLOCK)
                else:
                    i.USERBLOCK = re.sub(FINDUSERNAME, i.NAME, tempCSS.TIMESEARCHBLOCK)
                i.USERBLOCK= re.sub(FINDUSERID, i.UID, i.USERBLOCK)
                i.USERBLOCK= re.sub(FINDUSERNAME, i.NAME, i.USERBLOCK)
                i.USERBLOCK = re.sub(FINDUSERNODESIZE, i.ICONSIZE, i.USERBLOCK)
                i.USERBLOCK= re.sub(FINDUSERNODECOLOR, i.NODECOLORTEXT, i.USERBLOCK)
                i.USERBLOCK = re.sub(FINDUSERNODESHAPE, i.ICONSHAPE, i.USERBLOCK)
                i.USERBLOCK= re.sub(FINDUSERNAME, i.NAME, i.USERBLOCK)
                i.USERBLOCK = re.sub(FINDUSERWAYWIDTH, i.LINEWIDTH, i.USERBLOCK )
                i.USERBLOCK  = re.sub(FINDUSERWAYCOLOR, i.LINECOLORTEXT, i.USERBLOCK )
                i.USERBLOCK  = re.sub(FINDTIMESEARCH, self.SEARCHDATES, i.USERBLOCK )
                self.FINSHEDUSERBLOCK  += str(i.USERBLOCK)

#####FIX TEMPUSEERS INPUT TO EXPORT BY REPLACING WITH ADDUSERS AND ADDING FUNCTION TO UPDATE ADDUSERS AFTER EVERY CHANGE IN DATA
        else:
            for i in self.ADDUSERS:
                if self.TOGGLECHECK.isChecked():
                    i.USERBLOCK = re.sub(FINDUSERNAME, i.NAME, tempCSS.TOGGLEDUSERBLOCK)
                else:
                    i.USERBLOCK = re.sub(FINDUSERNAME, i.NAME, tempCSS.USERBLOCK)
                i.USERBLOCK= re.sub(FINDUSERID, i.UID, i.USERBLOCK)
                i.USERBLOCK= re.sub(FINDUSERNAME, i.NAME, i.USERBLOCK)
                i.USERBLOCK = re.sub(FINDUSERNODESIZE, i.ICONSIZE, i.USERBLOCK)
                i.USERBLOCK= re.sub(FINDUSERNODECOLOR, i.NODECOLORTEXT, i.USERBLOCK)
                i.USERBLOCK = re.sub(FINDUSERNODESHAPE, i.ICONSHAPE, i.USERBLOCK)
                i.USERBLOCK= re.sub(FINDUSERNAME, i.NAME, i.USERBLOCK)
                i.USERBLOCK = re.sub(FINDUSERWAYWIDTH, i.LINEWIDTH, i.USERBLOCK )
                i.USERBLOCK  = re.sub(FINDUSERWAYCOLOR, i.LINECOLORTEXT, i.USERBLOCK )

                ' Add the newest fisihed user block to the finished userblock'
            
                self.FINSHEDUSERBLOCK  += str(i.USERBLOCK)
                
        'Do the same for the static CSS blocks only once to enter all Team (unuploaded) Highlight settings'
        
        STATICBLOCK = re.sub(FINDNOTUPNODESIZE, self.ICONSIZE, tempCSS.STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPNODECOLOR,self.TEAMNODECOLORTEXT, STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPNODESHAPE, self.TEAMICONSHAPE, STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPWAYCOLOR, self.TEAMLINECOLORTEXT, STATICBLOCK)
        STATICBLOCK = re.sub(FINDNOTUPWAYWIDTH, self.LINEWIDTH, STATICBLOCK)
        STATICBLOCK = re.sub(FINDTITLE, self.TITLE, STATICBLOCK)
        
        'glue the fisihed userblock to the static block on the end'
        
        self.BLOCK = self.FINSHEDUSERBLOCK + STATICBLOCK
        
        'define the export file location & name'
        
        file = self.output_file_dir+("/")+(self.FILENAME)
        
        'write out the finished MapCSS file to the chosen directory'
        
        with open(file, 'w')as CSS:
            CSS.writelines (self.BLOCK)
        self.BLOCK = ""
        STATICBLOCK=""
        self.FINSHEDUSERBLOCK =""
        for i in self.ADDUSERS:
            i.USERBLOCK = ""

    ##############################################################################

    def CLEAR_clicked(self):
        '''Clear resets all of the values in the editor info fields,
           i.e. if the user wants to clear the text fields and reset their current color and shape
           selections to default, or if the user selected an editor to modify,
           but then decided not to make any changes'''
        try:
            self.NRSELECT = ""
            self.EDITORNAME.setText("")
            self.EDITORID.setText("")
            self.EDITORID.repaint()
            self.EDITORNAME.repaint()
            '''Repaint the ADD button with the appropriate text,
            since there is now no info in the editor info field,
            we can treat it as if adding a new editor'''
            self.ADD.setText("ADD")
            self.ADD.repaint()
            self.SELTEXT = ""
            self.pix.fill(QColor(self.WHITE))
            self.EDITORNODECOLORICON.setPixmap(self.pix)
            self.EDITORLINECOLORICON.setPixmap(self.pix)
            self.EDITORNODECOLORICON.repaint()
            self.EDITORLINECOLORICON.repaint()
            self.TEMPEDITORICONSHAPE = ""
            shape = QtGui.QIcon("")
            self.EDITORNODESHAPEICON.setIcon(shape)
            self.EDITORNODESHAPEICON.repaint()
        except Exception as e:
            logger.exception(e)

    def REMOVE_clicked(self):
        '''
        Remove_clicked opens a QDialog box asking the user if they are sure
        that they wish to remove the currently selected editor from the Table
        '''
        self.dialog = QMessageBox.question(
            self,
            "PyQt5 message",
            "Are you sure you want to remove this editor?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if self.dialog == QMessageBox.Yes:
            one.REMOVE_GO()

    def REMOVEALL_clicked(self):
        '''
        Remove_clicked opens a QDialog box asking the user if they are sure
        that they wish to remove all editors from the Table
        '''       
        self.GOREMOVEALL = True
        self.dialog = QMessageBox.question(
            self,
            "PyQt5 message",
            "Are you sure you want to remove all editors?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if self.dialog == QMessageBox.Yes:
            one.REMOVEALL_GO()

    def REMOVEALL_GO(self):
        '''
        REMOVEALL_GO clears all editors from the table as well as
        the ADDUSERS and TEMPUSERS array 
        ''' 
        try:
            self.usercount = 0
            self.ADDUSERS = []
            self.TEMPUSERS = {}
            self.pix.fill(QColor(self.WHITE))
            self.TEAMNODECOLORICON.setPixmap(self.pix)
            self.TEAMLINECOLORICON.setPixmap(self.pix)
            self.TEAMLINEWIDTHSPIN.setValue(0)
            self.TEAMICONSIZESPIN.setValue(0)
            self.TEAMNAME.setText("")
            self.TEAMNAME.repaint()
            self.TEAMNODECOLORICON.repaint()
            self.TEAMLINECOLORICON.repaint()
            for i in range(0, 50):
                self.GEMarray[i][0] = str("")
                self.GEMarray[i][1] = str("")
                self.GEMarray[i][2] = QtGui.QColor(clear)
                self.GEMarray[i][3] = QtGui.QColor(clear)
            self.GOREMOVEALL = False
        except Exception as e:
            logger.exception(e)

    def REMOVE_GO(self):
        '''
        REMOVEALL_GO clears the currently selected editor from the table as well as
        the ADDUSERS and TEMPUSERS array 
        ''' 
        for ix in self.TABLE.selectedIndexes():
            dat = ix.data()
            row = ix.row()
            if dat is not None:
                self.NRSELECT = row
            else:
                self.NRSELECT = ""
            try:
                self.ADDUSERS[int(self.NRSELECT)] = ""

            except Exception as e:
                logger.exception(e)
            try:
                self.TEMPUSERS[str(self.NRSELECT)] = 0
            except Exception as e:
                logger.exception(e)
            self.GEMarray[self.NRSELECT][0] = str("")
            self.GEMarray[self.NRSELECT][1] = str("")
            self.GEMarray[self.NRSELECT][2] = QtGui.QColor(clear)
            self.GEMarray[self.NRSELECT][3] = QtGui.QColor(clear)
            self.NRSELECT = ""
            self.usercount -= 1

    def SETNR(self):
        '''
        SETNR collects the row index for the currently selected editor in the table
        and assigns it to the NRSELECT variable
        '''
        for ix in self.TABLE.selectedIndexes():
            dat = ix.data()
            row = ix.row()
            if dat != "":
                self.NRSELECT = row
            else:
                self.NRSELECT = ""

    def EDIT_clicked(self):
        '''
        EDIT_clicked grabs all of the info from the class instance of the selected editor in the table and populates the
        Editor Settings fields in the GUI with that information. It also changes the text of the "ADD" button to "UPDATE" while the
        changes are being made
        '''
        for ix in self.TABLE.selectedIndexes():
            dat = ix.data()
            row = ix.row()
            if dat != "":
                self.NRSELECT = row

                self.ADD.setText("UPDATE")
                self.ADD.repaint()
            else:
                self.NRSELECT = ""
        if self.NRSELECT != "":
            if type(self.TEMPUSERS[str(self.NRSELECT)]) != str:
                self.GOEDIT = True
                self.EDITORNAME.setText(self.TEMPUSERS[str(self.NRSELECT)].NAME)
                self.EDITORID.setText(self.TEMPUSERS[str(self.NRSELECT)].UID)
                self.EDITORNAME.repaint()
                self.EDITORID.repaint()
                self.pix.fill(QColor(self.TEMPUSERS[str(self.NRSELECT)].NODECOLORUI))
                self.EDITORNODECOLORICON.setPixmap(self.pix)

                self.EDITORNODECOLORICON.repaint()
                self.pix.fill(QColor(self.TEMPUSERS[str(self.NRSELECT)].LINECOLORUI))
                self.EDITORLINECOLORICON.setPixmap(self.pix)
                self.EDITORLINECOLORICON.repaint()
                
#
                shape = QtGui.QIcon(self.TEMPUSERS[str(self.NRSELECT)].icon)
                self.EDITORNODESHAPEICON.setIcon(shape)
                self.EDITORNODESHAPEICON.repaint()
                
                self.EDITORLINEWIDTHSPIN.setValue(
                    int(self.TEMPUSERS[str(self.NRSELECT)].LINEWIDTH)

                )
                self.EDITORNODESIZESPIN.setValue(
                    int(self.TEMPUSERS[str(self.NRSELECT)].ICONSIZE)
                )
                self.EDITORLINEWIDTHSPIN.repaint()
                self.EDITORNODESIZESPIN.repaint()
                self.EDITORSELECT = self.NRSELECT

    @staticmethod
    def get_index_parsed_users(parsed_users: dict, user_key: str) -> str:
        """
        Parse a user dict to find the index key. It assumes that the user_key
        is unique in the dict. The primary purpose is if someone used different
        methods for determining the `set .class` in the mapcss file.
        """
        
        if user_key in parsed_users:
            return user_key
        for user in parsed_users:
            for key in parsed_users[user]:
                if parsed_users[user][key] == user_key:
                    return user
        return None

    @staticmethod
    def parse_team_from_mapcss(mapcss_text: str) -> str:
        title = re.findall(r"title: \"(.*?)\"", mapcss_text)

        title = (str(title).split(" "))
        
        title = title[3] if isinstance(title, list) else title
        teamname = title.split(".")
        teamname = (str(teamname[0]) )if title else None
        #teamname = re.findall(r".*For\s?(.*?)\s?Team.*?", title) 
        #teamname = teamname[0] if isinstance(teamname, list) else teamname
        return teamname
        

        
    @staticmethod
    def parse_users_from_mapcss(mapcss_text: str, parsed_users: dict = {}) -> dict:

        if OLDSTYLE != True:
            for i in re.finditer(
                r"\*\s*(\[\s*osm_user_name\s*\(\s*\)|\[\s*setting\(\s*\"user_.*?\"\s*\)).*?}",  # noqa: E501
                mapcss_text,
                ):
                temp = i.group()
                j = str(temp).split("}") 
                j = str(j).split("]")
                j= str(j).split("= ")
                j= str(j[1]).split('",')
                username = j[0]
                  
                personname = re.findall(r"setting\(\s*\"user_(.*?)\"", temp)
                parsed_users[username] = {"name": personname[0]}
            return parsed_users
        else:
            for i in re.finditer(
                r"\*\s*(\[\s*osm_user_name\s*\(\s*\)|\[\s*setting\(\s*\"user_.*?\"\s*\)).*?}",  # noqa: E501
                mapcss_text,
                ):
                temp = i.group()
                username = re.findall(r"osm_user_name\(\)\s*==\s*\\?\"?(.*?)\\?\"?\"", temp)
                if len(username) != 1:
                    username = re.findall(r"user:\\?\"?(.*?)\\?\"?\"", temp)
                personname = re.findall(r"setting\(\s*\"user_(.*?)\"", temp)
                if len(username) == 1 and len(personname) == 1:
                    parsed_users[username[0]] = {"name": personname[0]}
            return parsed_users
    
    @staticmethod
    def parse_line_colors_from_mapcss(mapcss_text: str, parsed_users: dict) -> dict:
        """
        This method parses way information from a mapcss file.
        >>> mapcss = "way.Dain { z-index: -10; casing-color: #B108D6; casing-width: 7; casing-opacity: 0.6; }"
        >>> MAINWindow.parse_line_colors_from_mapcss(mapcss, {})
        Traceback (most recent call last):
            ...
        MapCSSParseException: Unknown user: Dain
        >>> users = {"Dain": {}}
        >>> MAINWindow.parse_line_colors_from_mapcss(mapcss, users)
        {'Dain': {'casing-color': '#B108D6', 'casing_width': '7'}}
        """
        WAYSETTINGSBLOCK = re.findall(r"way\..*?}", mapcss_text)
        for i in WAYSETTINGSBLOCK:
            color = re.findall(r"casing-color:\s*([#A-Za-z0-9]+)\s*;", i)[0]
            width = re.findall(r"casing-width:\s*([0-9px]+)\s*;", i)[0]
            width = width.strip("px")

            for user in re.findall(r"way\.(.*?)\s*[,{]", i):
                # MAINWindow since this is the current class...
                key = MAINWindow.get_index_parsed_users(parsed_users, user)
                if key in parsed_users:
                    parsed_users[key]["casing-color"] = color
                    parsed_users[key]["casing_width"] = width
                else:
                    logger.debug(WAYSETTINGSBLOCK)
                    logger.debug(parsed_users)
                    raise MapCSSParseException(
                        "Unknown user: " + user,
                        exception_type=MapCSSParseExceptionType.UNKNOWN_USER,
                    )
        return parsed_users

    @staticmethod
    def parse_node_colors_from_mapcss(mapcss_text: str, parsed_users: dict) -> dict:
        """
        This method parses node information from a mapcss file.
        >>> mapcss = "node.Aaron { symbol-size: 15; symbol-shape: triangle; symbol-stroke-color: blue; symbol-stroke-width: 3px; symbol-fill-opacity: 0.5; z-index: -5; }"
        >>> MAINWindow.parse_node_colors_from_mapcss(mapcss, {})
        Traceback (most recent call last):
            ...
        MapCSSParseException: Unknown user: Aaron
        >>> users = {"Aaron": {}}
        >>> MAINWindow.parse_node_colors_from_mapcss(mapcss, users)
        {'Aaron': {'symbol-size': '15', 'symbol-shape': 'triangle', 'symbol-stroke-color': 'blue', 'symbol-stroke-width': '3px'}}
        """
        NODESETTINGSBLOCK = re.findall(r"node\..*?}", mapcss_text)
        for i in NODESETTINGSBLOCK:
            size = re.findall(r"symbol-size:\s*([0-9px]+)\s*;", i)[0]
            shape = re.findall(r"symbol-shape:\s*([#A-Za-z0-9]+)\s*;", i)[0]
            color = re.findall(r"symbol-stroke-color:\s*([#A-Za-z0-9]+)\s*;", i)[0]
            width = re.findall(r"symbol-stroke-width:\s*([0-9px]+)\s*;", i)[0]
            width = width.strip("px")

            for user in re.findall(r"node\.(.*?)\s*[,{]", i):
                # MAINWindow since this is the current class...
                key = MAINWindow.get_index_parsed_users(parsed_users, user)
                if key in parsed_users:
                    parsed_users[key]["symbol-size"] = size
                    parsed_users[key]["symbol-shape"] = shape
                    parsed_users[key]["symbol-stroke-color"] = color
                    parsed_users[key]["symbol-stroke-width"] = width
                else:
                    logger.debug(NODESETTINGSBLOCK)
                    logger.debug(parsed_users)
                    raise MapCSSParseException(
                        "Unknown user: " + user,
                        exception_type=MapCSSParseExceptionType.UNKNOWN_USER,
                    )
        return parsed_users

    def parse_mapcss_text(self, INFILETEXT: str) -> dict:
        # parsed_users = {user_class: {name: user_name, ...}}
        parsed_users = {}
        original_text = str(INFILETEXT)
        # Remove all comments from the original text (this just makes some
        # regexes easier). While the replaces/substitutions could be squashed
        # together, this is more readable in my opinion
        text_no_newline = original_text.replace("\n", " ")
        text_no_newline = re.sub(
            r"//.*?\n",
            "",
            re.sub(r"//.*?\\n", " ", re.sub(r"/\*.*?\*/", " ", text_no_newline)),
        )

        self.TEAMNAME.setText(self.parse_team_from_mapcss(text_no_newline))

        parsed_users = self.parse_users_from_mapcss(
            text_no_newline, parsed_users=parsed_users
        )

        self.TEAMLINECOLORTEXT = re.findall(
            r"way:modified.*?casing-color:\s?([#0-9A-Za-z]*)", text_no_newline
        )
        self.TEAMLINECOLORTEXT = (
            self.TEAMLINECOLORTEXT[0]
            if isinstance(self.TEAMLINECOLORTEXT, list)
            else self.TEAMLINECOLORTEXT
        )
        self.TEAMNODECOLORTEXT = re.findall(
            r"node:modified.*?symbol-stroke-color:\s?([#0-9A-Za-z]*)", text_no_newline,
        )
        self.TEAMNODECOLORTEXT = (
            self.TEAMNODECOLORTEXT[0]
            if isinstance(self.TEAMNODECOLORTEXT, list)
            else self.TEAMNODECOLORTEXT
        )
        self.TEAMLINECOLORUI = QtGui.QColor(self.TEAMLINECOLORTEXT)
        self.TEAMNODECOLORUI = QtGui.QColor(self.TEAMNODECOLORTEXT)
        self.LINEWIDTH = re.findall(
            r"way:modified.*?casing-width\s?:\s?([0-9]+)", text_no_newline
        )
        self.LINEWIDTH = (
            self.LINEWIDTH[0] if isinstance(self.LINEWIDTH, list) else self.LINEWIDTH
        )
        self.ICONSIZE = re.findall(
            r"node:modified.*?symbol-size:\s?([0-9]+)", text_no_newline
        )
        self.ICONSIZE = (
            self.ICONSIZE[0] if isinstance(self.ICONSIZE, list) else self.ICONSIZE
        )
        self.TEAMICONSHAPE = re.findall(
            r"node:modified.*?symbol-shape:\s?([a-zA-Z]+)", text_no_newline
        )
        self.TEAMICONSHAPE = (
            self.TEAMICONSHAPE[0]
            if isinstance(self.TEAMICONSHAPE, list)
            else self.TEAMICONSHAPE
        )

        parsed_users = self.parse_line_colors_from_mapcss(text_no_newline, parsed_users)
        parsed_users = self.parse_node_colors_from_mapcss(text_no_newline, parsed_users)
        return parsed_users

    def construct_table(self, parsed_users: dict):
        for user in parsed_users:
            CONSTRUCTOR = str(self.usercount)
            CONSTRUCTOR = EDITORINFO()
            NAME = parsed_users[user]["name"]
            CONSTRUCTOR.NAME = NAME
            CONSTRUCTOR.UID = user
            CONSTRUCTOR.LINECOLORUI = QtGui.QColor(parsed_users[user]["casing-color"])
            CONSTRUCTOR.NODECOLORUI = QtGui.QColor(
                parsed_users[user]["symbol-stroke-color"]
            )
            CONSTRUCTOR.LINECOLORTEXT = parsed_users[user]["casing-color"]
            CONSTRUCTOR.NODECOLORTEXT = parsed_users[user]["symbol-stroke-color"]
            CONSTRUCTOR.ICONSIZE = parsed_users[user]["symbol-size"]
            CONSTRUCTOR.LINEWIDTH = parsed_users[user]["symbol-stroke-width"]
            CONSTRUCTOR.ICONSHAPE = parsed_users[user]["symbol-shape"]
            CONSTRUCTOR.ICONSHAPE = CONSTRUCTOR.ICONSHAPE.lower()
            self.TEMPUSERS[str(self.usercount)] = CONSTRUCTOR


            ##
            self.ADDUSERS.append(CONSTRUCTOR)
            ##
            self.GEMarray[self.usercount][0] = str(CONSTRUCTOR.NAME)
            self.GEMarray[self.usercount][1] = str(CONSTRUCTOR.UID)
            self.GEMarray[self.usercount][2] = QtGui.QColor(CONSTRUCTOR.LINECOLORUI)
            ##self.GEMarray[self.usercount][3] = QtGui.QColor(CONSTRUCTOR.ICONSHAPE)
            self.EDITORNODECOLORDISPLAY(self.usercount)
            self.pix.fill(QColor(self.TEAMNODECOLORUI))
            self.TEAMNODECOLORICON.setPixmap(self.pix)
            self.TEAMNODECOLORICON.repaint()
            self.TEAMLINEWIDTHSPIN.setValue(int(self.LINEWIDTH))
            self.TEAMICONSIZESPIN.setValue(int(self.ICONSIZE))
            self.pix.fill(QColor(self.TEAMLINECOLORUI))
            self.TEAMLINECOLORICON.setPixmap(self.pix)
            self.TEAMLINECOLORICON.repaint()
            self.usercount += 1
            self.TABLE.resizeColumnsToContents()
            self.TABLE.resizeRowsToContents()
            



    def IMPORTGO(self):
        """
        IMPORTGO opens a QfileDialog to allow the user to select a local mapcss file to import.
        The function also parses the fisrst block of the incoming mapcss file to determine if the Meta block
        is at the top of the file, which distinguishes it from the new-style mapcss files we have built
        specifically for GEM. These two types of files need to be parsed differently, so the OLDSTYLE bool is
        accordingly which will allow the parse_users function to choose use the correct method of parsing the file.
        IMPORTGO then calls IMPORT_clicked once a file is chosen.
        """        
        try:
            infile = QtWidgets.QFileDialog.getOpenFileName(
                self, self.filters, self.output_file_dir, self.select_filters
            )
            infile = str(infile[0])
            with open(infile, "r+") as reader:
                infile_text = reader.read()
                TYPETEST = infile_text.split("{")
                if TYPETEST[0] == ("meta "):
                    OLDSTYLE = True
                else:
                    OLDSTYLE = False
                TYPETEST = ""
        except Exception as e:
            pass
            #logger.exception(e)
        try:
            self.IMPORT_clicked(infile_text)
        except Exception as e:
            #logger.exception(e)
            pass
    def IMPORT_clicked(self, PULL):
        '''
        IMPORT_clicked calls the parsed_users function which rips the editor data from the selected Mapcss file
        (Using the OLD or NEW style according to the bool we set in IMPORTGO) and then calls
        construct_table to populate the table with the parsed editor information
        '''   
        parsed_users = self.parse_mapcss_text(str(PULL))
        self.construct_table(parsed_users)

    def EDITORNODECOLORDISPLAY(self, count):
        '''
        EDITORNODECOLORDISPLAY applies a selected node color highlight to the selected editor's node highlight shape
        and reflects that change in the editor table
        '''

        if self.TEMPUSERS[str(count)].ICONSHAPE == "circle":

            pixmap = QtGui.QPixmap(self.CIRCLE)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "square":
            pixmap = QtGui.QPixmap(self.SQUARE)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "triangle":
            pixmap = QtGui.QPixmap(self.TRIANGLE)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "pentagon":
            pixmap = QtGui.QPixmap(self.PENTAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "hexagon":
            pixmap = QtGui.QPixmap(self.HEXAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "heptagon":
            pixmap = QtGui.QPixmap(self.HEPTAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "octagon":
            pixmap = QtGui.QPixmap(self.OCTAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "nonagon":
            pixmap = QtGui.QPixmap(self.NONAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)

            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon

        if self.TEMPUSERS[str(count)].ICONSHAPE == "decagon":
            pixmap = QtGui.QPixmap(self.DECAGON)
            pixmap = pixmap.scaled(30, 30)
            mask = pixmap.createMaskFromColor(QColor("black"), Qt.MaskOutColor)
            pixmap.fill((QColor(self.TEMPUSERS[str(count)].NODECOLORUI)))
            pixmap.setMask(mask)
            self.TEMPUSERS[str(count)].icon = QtGui.QIcon(pixmap)
            self.GEMarray[count][3] = self.TEMPUSERS[str(count)].icon
##################################
class EDITORiconWindow(QMainWindow):
    def __init__(self,SELECT):
        QMainWindow.__init__(self)
        self.setGeometry(650,300,225,250)
        self.setWindowTitle("Select Node Highlight")
        self.EDITNODEHIGHLIGHTHOME(SELECT)
        
    def EDITNODEHIGHLIGHTHOME(self,SELECT):
#COL 1

        circB = QPushButton(self)
        circ = QtGui.QIcon(one.CIRCLE)
        circB.setIcon(circ)
        circB.resize(75,75)
        circB.move(10,20)

        circLABEL = QLabel(self)
        circLABEL.setText("Circle")
        circLABEL.resize(60,20)
        circLABEL.move(30, 70)
        circB.clicked.connect(lambda: self.CIRCLE_clicked(SELECT))

        
        triB = QPushButton(self)
        tri  = QtGui.QIcon(one.TRIANGLE)
        triB.setIcon(tri)
        triB.resize(75,75)
        triB.move(70,20)
        triB.clicked.connect(lambda: self.TRIANGLE_clicked(SELECT))
        triLABEL = QLabel(self)
        triLABEL.setText("Triangle")
        triLABEL.resize(60,20)
        triLABEL.move(82, 70)


        squareB = QPushButton(self)
        square = QtGui.QIcon(one.SQUARE)
        squareB.setIcon(square)
        squareB.resize(75,75)
        squareB.move(130,20)
        squareB.clicked.connect(lambda: self.SQUARE_clicked(SELECT))
        squareLABEL = QLabel(self)
        squareLABEL.setText("Square")
        squareLABEL.resize(60,20)
        squareLABEL.move(145, 70)
##COL 2

        pentB = QPushButton(self)
        pent  = QtGui.QIcon(one.PENTAGON)
        pentB.setIcon(pent)
        pentB.resize(75,75)
        pentB.move(10,85)
        pentB.clicked.connect(lambda: self.PENTA_clicked(SELECT))
        pentLABEL = QLabel(self)
        pentLABEL.setText("Pentagon")
        pentLABEL.resize(60,20)
        pentLABEL.move(18, 135)

        
        hexB = QPushButton(self)
        hexagon  = QtGui.QIcon(one.HEXAGON)
        hexB.setIcon(hexagon)
        hexB.resize(75,75)
        hexB.move(70,85)
        hexB.clicked.connect(lambda: self.HEX_clicked(SELECT))
        hexLABEL = QLabel(self)
        hexLABEL.setText("Hexagon")
        hexLABEL.resize(60,20)
        hexLABEL.move(80, 135)


        heptB = QPushButton(self)
        heptagon = QtGui.QIcon(one.HEPTAGON)
        heptB.setIcon(heptagon)
        heptB.resize(75,75)
        heptB.move(130,85)
        heptB.clicked.connect(lambda: self.HEPTA_clicked(SELECT))
        hepLABEL = QLabel(self)
        hepLABEL.setText("Heptagon")
        hepLABEL.resize(60,20)
        hepLABEL.move(138, 135)
##COL 3

        octoB = QPushButton(self)
        octo  = QtGui.QIcon(one.OCTAGON)
        octoB.setIcon(octo)
        octoB.resize(75,75)
        octoB.move(10,150)
        octoB.clicked.connect(lambda: self.OCTA_clicked(SELECT))
        octoLABEL = QLabel(self)
        octoLABEL.setText("Octagon")
        octoLABEL.resize(60,20)
        octoLABEL.move(22, 200)
        
        nonB = QPushButton(self)
        non  = QtGui.QIcon(one.NONAGON)
        nonB.setIcon(non)
        nonB.resize(75,75)
        nonB.move(70,150)
        nonB.clicked.connect(lambda: self.NONA_clicked(SELECT))
        nonLABEL = QLabel(self)
        nonLABEL.setText("Nonagon")
        nonLABEL.resize(60,20)
        nonLABEL.move(80, 200)
        
        decaB = QPushButton(self)
        deca = QtGui.QIcon(one.DECAGON)
        decaB.setIcon(deca)
        decaB.resize(75,75)
        decaB.move(130,150)
        decaB.clicked.connect(lambda: self.DECA_clicked(SELECT))
        decaLABEL = QLabel(self)
        decaLABEL.setText("Decagon")
        decaLABEL.resize(60,20)
        decaLABEL.move(140, 200)
        
        self.show()
        
   

    def CIRCLE_clicked(self,SELECT):
        if SELECT == "TEAM":
            one.TEAMICONSHAPE = "circle"
            shape = QtGui.QIcon(one.CIRCLE)
            one.TEAMNODESHAPEICON.setIcon(shape)
            one.TEAMNODESHAPEICON.repaint()            
        else:
            if (str(one.NRSELECT)) != '':
                
                one.TEMPUSERS[(str(one.NRSELECT))].ICONSHAPE = "circle"
            else:
                one.TEMPEDITORICONSHAPE = "circle"
            shape = QtGui.QIcon(one.CIRCLE)
            one.EDITORNODESHAPEICON.setIcon(shape)
            one.EDITORNODESHAPEICON.repaint()        
        self.close()


        
        
    def TRIANGLE_clicked(self,SELECT):
        if SELECT == "TEAM":
            one.TEAMICONSHAPE = "triangle"
            shape = QtGui.QIcon(one.TRIANGLE)
            one.TEAMNODESHAPEICON.setIcon(shape)
            one.TEAMNODESHAPEICON.repaint()            
        else:
            if (str(one.NRSELECT)) != '':
                
                one.TEMPUSERS[(str(one.NRSELECT))].ICONSHAPE = "triangle"
            else:
                one.TEMPEDITORICONSHAPE = "triangle"
            shape = QtGui.QIcon(one.TRIANGLE)
            one.EDITORNODESHAPEICON.setIcon(shape)
            one.EDITORNODESHAPEICON.repaint()        
        self.close()


        
    def SQUARE_clicked(self,SELECT):
        if SELECT == "TEAM":
            one.TEAMICONSHAPE = "square"
            shape = QtGui.QIcon(one.SQUARE)
            one.TEAMNODESHAPEICON.setIcon(shape)
            one.TEAMNODESHAPEICON.repaint()            
        else:
            if (str(one.NRSELECT)) != '':
                
                one.TEMPUSERS[(str(one.NRSELECT))].ICONSHAPE = "square"
            else:
                one.TEMPEDITORICONSHAPE = "square"
            shape = QtGui.QIcon(one.SQUARE)
            one.EDITORNODESHAPEICON.setIcon(shape)
            one.EDITORNODESHAPEICON.repaint()        
        self.close()



        
###
    def PENTA_clicked(self,SELECT):
        if SELECT == "TEAM":
            one.TEAMICONSHAPE = "pentagon"
            shape = QtGui.QIcon(one.PENTAGON)
            one.TEAMNODESHAPEICON.setIcon(shape)
            one.TEAMNODESHAPEICON.repaint()            
        else:
            if (str(one.NRSELECT)) != '':
                
                one.TEMPUSERS[(str(one.NRSELECT))].ICONSHAPE = "pentagon"
            else:
                one.TEMPEDITORICONSHAPE = "pentagon"
            shape = QtGui.QIcon(one.PENTAGON)
            one.EDITORNODESHAPEICON.setIcon(shape)
            one.EDITORNODESHAPEICON.repaint()        
        self.close()



        
    def HEX_clicked(self,SELECT):
        if SELECT == "TEAM":
            one.TEAMICONSHAPE = "hexagon"
            shape = QtGui.QIcon(one.HEXAGON)
            one.TEAMNODESHAPEICON.setIcon(shape)
            one.TEAMNODESHAPEICON.repaint()            
        else:
            if (str(one.NRSELECT)) != '':
                
                one.TEMPUSERS[(str(one.NRSELECT))].ICONSHAPE = "hexagon"
            else:
                one.TEMPEDITORICONSHAPE = "hexagon"
            shape = QtGui.QIcon(one.HEXAGON)
            one.EDITORNODESHAPEICON.setIcon(shape)
            one.EDITORNODESHAPEICON.repaint()        
        self.close()
        
        
    def HEPTA_clicked(self,SELECT):
        if SELECT == "TEAM":
            one.TEAMICONSHAPE = "heptagon"
            shape = QtGui.QIcon(one.HEPTAGON)
            one.TEAMNODESHAPEICON.setIcon(shape)
            one.TEAMNODESHAPEICON.repaint()            
        else:
            if (str(one.NRSELECT)) != '':
                
                one.TEMPUSERS[(str(one.NRSELECT))].ICONSHAPE = "heptagon"
            else:
                one.TEMPEDITORICONSHAPE = "heptagon"
            shape = QtGui.QIcon(one.HEPTAGON)
            one.EDITORNODESHAPEICON.setIcon(shape)
            one.EDITORNODESHAPEICON.repaint()        
        self.close()

        
 ##
    def OCTA_clicked(self,SELECT):
        if SELECT == "TEAM":
            one.TEAMICONSHAPE = "octagon"
            shape = QtGui.QIcon(one.OCTAGON)
            one.TEAMNODESHAPEICON.setIcon(shape)
            one.TEAMNODESHAPEICON.repaint()            
        else:
            if (str(one.NRSELECT)) != '':
                
                one.TEMPUSERS[(str(one.NRSELECT))].ICONSHAPE = "octagon"
            else:
                one.TEMPEDITORICONSHAPE = "octagon"
            shape = QtGui.QIcon(one.OCTAGON)
            one.EDITORNODESHAPEICON.setIcon(shape)
            one.EDITORNODESHAPEICON.repaint()        
        self.close()

        
        
    def NONA_clicked(self,SELECT):
        if SELECT == "TEAM":
            one.TEAMICONSHAPE = "nonagon"
            shape = QtGui.QIcon(one.NONAGON)
            one.TEAMNODESHAPEICON.setIcon(shape)
            one.TEAMNODESHAPEICON.repaint()            
        else:
            if (str(one.NRSELECT)) != '':
                
                one.TEMPUSERS[(str(one.NRSELECT))].ICONSHAPE = "nonagon"
            else:
                one.TEMPEDITORICONSHAPE = "nonagon"
            shape = QtGui.QIcon(one.NONAGON)
            one.EDITORNODESHAPEICON.setIcon(shape)
            one.EDITORNODESHAPEICON.repaint()        
        self.close()
        
    def DECA_clicked(self,SELECT):
        if SELECT == "TEAM":
            one.TEAMICONSHAPE = "decagon"
            shape = QtGui.QIcon(one.DECAGON)
            one.TEAMNODESHAPEICON.setIcon(shape)
            one.TEAMNODESHAPEICON.repaint()            
        else:
            if (str(one.NRSELECT)) != '':
                
                one.TEMPUSERS[(str(one.NRSELECT))].ICONSHAPE = "decagon"
            else:
                one.TEMPEDITORICONSHAPE = "decagon"
            shape = QtGui.QIcon(one.DECAGON)
            one.EDITORNODESHAPEICON.setIcon(shape)
            one.EDITORNODESHAPEICON.repaint()        
        self.close()
            
###################################
def main(args):
        app = QtWidgets.QApplication(args)
        global one
        one =MAINWindow ()
        one.show()
        sys.exit(app.exec_())
        if self.EXIT == 1:
            sys.exit(0)
        sys._excepthook = sys.excepthook
        
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback) 
    sys.exit(1) 
sys.excepthook = exception_hook

while  True:
    main(sys.argv) 

            

# ################################   MAIN LOOP   ########################### #
##def main(args):
##    parser = argparse.ArgumentParser(description="Modify MapCSS files for QC purposes")
##    parser.add_argument(
##        "--test", action="store_true", required=False, help="Run doctests"
##    )
##    parser.add_argument(
##        "-f", "--file", required=False, help="A file to open the program with"
##    )
##    parsed_args = parser.parse_args()
##    if parsed_args.test:
##        import doctest
##
##        doctest.testmod()
##    else:
##        app = QtWidgets.QApplication(args)
##        global one
##        one = MAINWindow()
##        one.show()
##        if parsed_args.file is not None:
##            mapcss_file = parsed_args.file
##            if isinstance(mapcss_file, str):
##                mapcss_file = [mapcss_file]
##            for mfile in mapcss_file:
##                with open(mfile, "r") as f:
##                    one.IMPORT_clicked(f.read())
##        sys.exit(app.exec_())
##        sys._excepthook = sys.excepthook
##        sys.excepthook = exception_hook
##
##
##def exception_hook(exctype, value, traceback):
##    print(exctype, value, traceback)
##    try:
##        sys._excepthook(exctype, value, traceback)
##    except Exception as error:
##        logger.exception(error)
##    sys.exit(1)
##
##
##if __name__ == "__main__":
##    main(sys.argv)
