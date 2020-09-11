import argparse
import json
import requests
import urllib
import httpbin
import github
from github import Github
import os
import sys
import logging
import re
from enum import Enum, auto
import PyQt5
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
)
from PyQt5.QtWidgets import QPushButton, QMessageBox, QTabWidget


git = Github('f689ec8e76db5bf9282b9cbe662d7a9003f82d41')

        menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        exitAct = QAction(QIcon("exit.png"), " &Quit", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setStatusTip("Exit GEM")
        exitAct.triggered.connect(self.closeEvent)
        FILE = self.menubar.addMenu("&File")
        self.GITPULL = FILE.addMenu("Git Pull")
        GITPUSH = QAction(" &Git Push", self)
        GITPUSH.setStatusTip("Export .Mapcss to Github")
        #GITPUSH.triggered.connect(GITSTUFF.CONFIRMPUSH)
        GITPUSH = FILE.addAction(GITPUSH)
        FILE.addAction(exitAct)

def GITMENUINFO(APP):

        try:
            org = git.get_user('CEFgoose')
            repo = org.get_repo('TEST')
            contents = repo.get_contents("")
            print(contents)
            pulllist = {}
            pullcount = 0
            pullcountlist = []
            for i in contents:
                i = str(i)
                i = i.split('"')
                i = i[1]

                if "mapcss" in i:
                    i = i.split(".")
                    i = i[0]
                    pullcount += 1
                    pullcountlist.append(pullcount)
                    pulllist[pullcount] = i
            PULLS = []
            for j in range(pullcount):
                TEXT = pulllist[j + 1]
                ACT = str("ACT%s" % (j))
                ACT = QAction("&Pull %s Paintstyle from Github" % (TEXT))
                ACT.setStatusTip("Import .Mapcss from Github")
                APP.GITPULL.addAction(ACT)
                PULLS.append(ACT)

            for j in  PULLS:
                j.triggered.connect(GITPULL_clicked)

        except github.BadCredentialsException as error:
            pass


def CONFIRMPUSH(APP):
    passdialog = APP.CONFIRMPOPUP()
    passdialog.show()

def GITPULL_clicked(APP):
    SENDER = APP.sender()
    TEXT = SENDER.text()
    TEXT = TEXT.replace(" &Pull ", "")
    TEXT = TEXT.replace(" Paintstyle from Github", "")
    org = ACCESSTOKEN.get_user("Kaart-labs")
    repo = org.get_repo("GEM")
    contents = repo.get_contents("%s.mapcss" % (TEXT))
    c = contents.decoded_content
    APP.IMPULLGO(c)

def GITPUSH_GO(APP):
    APP.USERENTRYBLOCK = ""
    APP.MASTERENTERYTEXT = ""
    APP.OUTUSERS = 0
    APP.EXPORT_clicked(True)
    NAME = "Kaart_QC_%s.mapcss" % (APP.TEAMNAME.text())
    try:
        contents = repo.get_contents(NAME)
        c = contents.decoded_content
        repo.update_file(
            contents.path, "GEM", APP.OUTPUSHTEXT, contents.sha
        )
    except Exception as error:

        repo.create_file(NAME, "GEM", APP.OUTPUSHTEXT)


# ###### PASSWORD POPUP WINDOW ###### #


class CONFIRMPOPUP(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(900, 100, 300, 80)
        self.setWindowTitle("CONFIRMATION")
        self.POPHOME()

    def POPHOME(self):
        self.LABEL = QtWidgets.QLabel(self)
        self.LABEL.setText("Enter administrator password:")
        self.LABEL.resize(300, 20)
        self.LABEL.move(13, 5)

        self.PASSFIELD = QtWidgets.QLineEdit(self)
        self.PASSFIELD.setEchoMode(self.PASSFIELD.Password)
        self.PASSFIELD.resize(275, 20)
        self.PASSFIELD.move(12, 30)

        self.CONFIRM = QPushButton(self)
        self.CONFIRM.setText("CONFIRM")
        self.CONFIRM.resize(150, 25)
        self.CONFIRM.move(5, 50)
        self.CONFIRM.clicked.connect(self.CONFIRMED_clicked)

        self.CANCEL = QPushButton(self)
        self.CANCEL.setText("CANCEL")
        self.CANCEL.resize(150, 25)
        self.CANCEL.move(145, 50)
        self.CANCEL.clicked.connect(self.CANCEL_clicked)
        self.show()

    def CONFIRMED_clicked(self):
        TESTPASS = self.PASSFIELD.text()

        if TESTPASS == one.ADMINPASS:
            one.GITPUSH_GO()
        self.close()

    def CANCEL_clicked(self):
        self.close()



    def IMPULLGO(self, PULL):
        '''
        IMPULL_GO  is a function intended for the github functionalitycalls the parse_mapcss function to rip editor data from an imported mapcss file, then calls
        the construct table function to pupulate the table with the imported information.
        '''
        parsed_users = self.parse_mapcss_text(str(PULL))
        self.construct_table(parsed_users)
