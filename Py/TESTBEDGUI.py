#!/usr/bin/env python
import argparse
import json
import requests
import urllib
import httpbin
import github
import tempCSS
from datetime import datetime
from github import Github
import os
import sys
import logging
import re
from enum import Enum, auto
import PyQt5
from PyQt5.QtCore import QDate
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt
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
class MAINWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(720, 300, 700, 620)
        self.setWindowTitle("GEM - GUI Editor for Mapcss")
        self.MWHOME(self)
        self.output_file_dir = os.path.expanduser("~/Documents")

    def MWHOME(self, MAINWindow):
        self.TITLE = ""
        self.ADMINPASS = "**********"
        self.repoGO = False
        self.GOREMOVEALL = False
        self.CALENDAROPEN = False
        self.SEARCHDATES = ""
        
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

        self.GUMTEMPUSERS = {}
        for j in range(100):
            self.GUMTEMPUSERS[str(j)] = 0
        self.ADDUSERS = []
        self.GUMADDUSERS = []
        self.filters = ""
        self.select_filters = "MAPCSS (*.mapcss)"
        self.directory = os.getcwd()
        self.SELTEXT = ""
        self.TEMPEDITORICONSHAPE = ""
        self.TEMPLINECOLORTEXT = ""
        self.TEMPNODECOLORTEXT = ""
        self.GOEDIT = False
        self.TABS = QTabWidget(self)
        self.TABS.resize(690, 580)
        self.TABS.move(5, 25)
        self.TAB1 = QWidget()
        self.TABS.addTab(self.TAB1, "GEM")
        self.PULLUSER = ""
        # ###############################TABLE BUTTONS############################## #

        self.TABLE = QtWidgets.QTableView(self.TAB1)
        self.TABLE.resize(400, 330)
        self.TABLE.move(255, 30)


        self.REMOVE = QtWidgets.QPushButton(self.TAB1)
        self.REMOVE.setText("REMOVE")
        self.REMOVE.resize(110, 25)
        self.REMOVE.move(250, 367)


        self.REMOVEALL = QPushButton(self.TAB1)
        self.REMOVEALL.setText("REMOVE ALL")
        self.REMOVEALL.resize(110, 25)
        self.REMOVEALL.move(250, 392)


        self.EXPORT = QPushButton(self.TAB1)
        self.EXPORT.setText("EXPORT")
        self.EXPORT.resize(110, 25)
        self.EXPORT.move(350, 392)


        self.IMPORT = QPushButton(self.TAB1)
        self.IMPORT.setText("IMPORT")
        self.IMPORT.resize(110, 25)
        self.IMPORT.move(350, 367)


        self.RESTACK = QPushButton(self.TAB1)
        self.RESTACK.setText("RESTACK")
        self.RESTACK.resize(110, 25)
        self.RESTACK.move(550, 367)


        self.MOVEUP = QPushButton(self.TAB1)
        self.MOVEUP.setText("MOVE UP")
        self.MOVEUP.resize(110, 25)
        self.MOVEUP.move(450, 367)


        self.MOVEDOWN = QPushButton(self.TAB1)
        self.MOVEDOWN.setText("MOVE DOWN")
        self.MOVEDOWN.resize(110, 25)
        self.MOVEDOWN.move(450, 392)

        # ##############################TEAM SETTINGS######################## #
        self.groupBox = QtWidgets.QGroupBox(self.TAB1)

        self.groupBox.setGeometry(QtCore.QRect(5, 30, 245, 40))

        self.TEAMNAMELABEL = QtWidgets.QLabel(self.groupBox)
        self.TEAMNAMELABEL.setText("Team Name")
        self.TEAMNAMELABEL.resize(250, 20)
        self.TEAMNAMELABEL.move(10, 5)

        self.TEAMNAME = QtWidgets.QLineEdit(self.groupBox)
        self.TEAMNAME.resize(130, 20)
        self.TEAMNAME.move(105, 8)
        # ##############################HIGHLIGHT SETTINGS################### #
        self.groupBox3 = QtWidgets.QGroupBox(self.TAB1)
        self.groupBox3.setGeometry(QtCore.QRect(5, 75, 245, 120))

        self.NOTUPLOADEDLABEL = QtWidgets.QLabel(self.groupBox3)
        self.NOTUPLOADEDLABEL.setText("Highlight non-uploaded additions")
        self.NOTUPLOADEDLABEL.resize(250, 20)
        self.NOTUPLOADEDLABEL.move(10, 5)

        self.TEAMLINECOLOR = QPushButton(self.groupBox3)
        self.TEAMLINECOLOR.setText("LINE COLOR")
        self.TEAMLINECOLOR.resize(110, 25)
        self.TEAMLINECOLOR.move(3, 30)


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
        self.ICONSHAPELABEL.setText("Node Shape  -")
        self.ICONSHAPELABEL.resize(250, 20)
        self.ICONSHAPELABEL.move(10, 84)

        self.TEAMICONSHAPEBOX = QtWidgets.QComboBox(self.groupBox3)
        self.TEAMICONSHAPEBOX.setEnabled(True)

        self.TEAMICONSHAPEBOX.blockSignals(True)
        self.TEAMICONSHAPEBOX.resize(138, 20)
        self.TEAMICONSHAPEBOX.addItem("Circle")
        self.TEAMICONSHAPEBOX.addItem("Triangle")
        self.TEAMICONSHAPEBOX.addItem("Square")
        self.TEAMICONSHAPEBOX.addItem("Pentagon")
        self.TEAMICONSHAPEBOX.addItem("Hexagon")
        self.TEAMICONSHAPEBOX.addItem("Heptagon")
        self.TEAMICONSHAPEBOX.addItem("Octagon")
        self.TEAMICONSHAPEBOX.addItem("Nonagon")
        self.TEAMICONSHAPEBOX.addItem("Decagon")
        self.TEAMICONSHAPEBOX.setCurrentIndex(-1)
        self.TEAMICONSHAPEBOX.blockSignals(False)

        self.TEAMICONSHAPEBOX.move(105, 85)

        # ##############################EDITOR SETTINGS###################### #

        self.groupBox2 = QtWidgets.QGroupBox(self.TAB1)
        self.groupBox2.setGeometry(QtCore.QRect(5, 200, 245, 220))

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


        self.CLEAR = QPushButton(self.groupBox2)
        self.CLEAR.setText("CLEAR")
        self.CLEAR.resize(80, 25)
        self.CLEAR.move(83, 75)


        self.EDIT = QPushButton(self.groupBox2)
        self.EDIT.setText("EDIT")
        self.EDIT.resize(80, 25)
        self.EDIT.move(160, 75)
        self.EDITORLINECOLOR = QPushButton(self.groupBox2)
        self.EDITORLINECOLOR.setText("LINE COLOR")
        self.EDITORLINECOLOR.resize(110, 25)
        self.EDITORLINECOLOR.move(5, 105)
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
        self.EDITORICONSHAPELABEL.setText("Node Shape  -")
        self.EDITORICONSHAPELABEL.resize(250, 20)
        self.EDITORICONSHAPELABEL.move(12, 190)

        self.EDITORICONSHAPEBOX = QtWidgets.QComboBox(self.groupBox2)
        self.EDITORICONSHAPEBOX.setEnabled(True)

        self.EDITORICONSHAPEBOX.blockSignals(True)
        
        self.EDITORICONSHAPEBOX.resize(135, 20)
        self.EDITORICONSHAPEBOX.clear()
        self.EDITORICONSHAPEBOX.move(100, 190)

        self.TIMEBox = QtWidgets.QGroupBox(self.TAB1)
        self.TIMEBox.setGeometry(QtCore.QRect(5, 425, 245, 125))
  
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
        self.CAL.setText("OPEN CALANDER")
        self.CAL.resize(155, 25)
        self.CAL.move(90, 1)
        self.CAL.clicked.connect(self.CHOOSEDATE)


        self.TIMETOGGLELABEL = QtWidgets.QLabel(self.TIMEBox)
        self.TIMETOGGLELABEL.setText("Toggle Timestamp Search on/off:")
        self.TIMETOGGLELABEL.resize(250, 20)
        self.TIMETOGGLELABEL.move(12, 100)

        self.TIMETOGGLECHECK = QtWidgets.QCheckBox(self.TIMEBox)
        self.TIMETOGGLECHECK.move(222, 102)
       #self.TIMETOGGLECHECK.toggled.connnect(self.TOGGLETIMESEARCH)
        self.retranslateUi(MAINWindow)

        # ####################### RETRANSLATE UI ########################## #

    def retranslateUi(self, MAINWindow):

        self.GEMheaders = [
            "NAME",
            "USER ID",
            "LINE HIGHLIGHT",
            "NODE HIGHLIGHT",
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
        self.setParent(None)
        self.deleteLater()

        self.close()

    def CHOOSEDATE(self):
        if self.CALENDAROPEN == False:
            self.calendar = QCalendarWidget(self)
            self.calendar.move(260, 380)
            self.calendar.resize(300, 200)
            self.calendar.setGridVisible(True)
            self.calendar.show()
            self.calendar.clicked.connect(self.SETSTARTDATE)
            self.CALENDAROPEN = True
            self.CAL.setText("CLOSE CALANDER")
        else:
            self.calendar.close()
            self.TAB1.repaint()
            self.CALENDAROPEN = False
            self.CAL.setText("OPEN CALANDER")


        
    def SETSTARTDATE(self,qDate):
        if self.STARTDATESELECT.isChecked():
              self.STARTDATE.setText('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))
              self.STARTDATE.repaint()
        elif self.ENDDATESELECT.isChecked():
              self.ENDDATE.setText('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))
              self.ENDDATE.repaint()
              
    def SETSEARCHDATES(self):
        if self.STARTDATE.currentText()!= "":
            if self.ENDDATE.currentText()!= "":
                self.SEARCHDATES  = ("timestamp:%s/%s"%(self.STARTDATE.text(),self.ENDDATE.text()))
            else:
                self.SEARCHDATES = "timestamp:%s/"%(self.STARTDATE.text())
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

    def TOGGLETIMESEARCH(self):

        pass
        
#



# ################################   MAIN LOOP   ########################### #
def main(args):
    parser = argparse.ArgumentParser(description="Modify MapCSS files for QC purposes")
    parser.add_argument(
        "--test", action="store_true", required=False, help="Run doctests"
    )
    parser.add_argument(
        "-f", "--file", required=False, help="A file to open the program with"
    )
    parsed_args = parser.parse_args()
    if parsed_args.test:
        import doctest

        doctest.testmod()
    else:
        app = QtWidgets.QApplication(args)
        global one
        one = MAINWindow()
        one.show()
        if parsed_args.file is not None:
            mapcss_file = parsed_args.file
            if isinstance(mapcss_file, str):
                mapcss_file = [mapcss_file]
            for mfile in mapcss_file:
                with open(mfile, "r") as f:
                    one.IMPORT_clicked(f.read())
        sys.exit(app.exec_())
        #sys._excepthook = sys.excepthook
        #sys.excepthook = exception_hook


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    try:
        sys._excepthook(exctype, value, traceback)
    except Exception as error:
        logger.exception(error)
    sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
