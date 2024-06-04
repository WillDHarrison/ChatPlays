from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from chatController import ChatController
from inputWidget import InputWidget
from twitchInputUI import TwitchInput
import sys
import os
import threading

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.extW = None
        self.setupUi()
        self.show()
        self.chat = ChatController(self)
        self.t1 = threading.Thread(target=self.startControl)
        self.loaded = False
        self.commandWidgets = []
        self.currFunc = ""

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(969, 695)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)


        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")


        self.KeyList = QtWidgets.QScrollArea(self.centralwidget)
        self.KeyList.setGeometry(QtCore.QRect(10, 70, 951, 461))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.KeyList.sizePolicy().hasHeightForWidth())

        self.KeyList.setSizePolicy(sizePolicy)
        self.KeyList.setMinimumSize(QtCore.QSize(0, 300))
        self.KeyList.setWidgetResizable(True)
        self.KeyList.setObjectName("KeyList")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 949, 459))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        self.KeyList.setWidget(self.scrollAreaWidgetContents)


        self.LabelFrame = QtWidgets.QFrame(self.centralwidget)
        self.LabelFrame.setGeometry(QtCore.QRect(9, 10, 951, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LabelFrame.setFont(font)
        self.LabelFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LabelFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LabelFrame.setObjectName("LabelFrame")
        self.ChatInpLabel = QtWidgets.QLabel(self.LabelFrame)
        self.ChatInpLabel.setGeometry(QtCore.QRect(30, 10, 131, 31))
        self.ChatInpLabel.setObjectName("ChatInpLabel")
        self.KeyPressLabel = QtWidgets.QLabel(self.LabelFrame)
        self.KeyPressLabel.setGeometry(QtCore.QRect(220, 10, 131, 31))
        self.KeyPressLabel.setObjectName("KeyPressLabel")
        self.DurLabel = QtWidgets.QLabel(self.LabelFrame)
        self.DurLabel.setGeometry(QtCore.QRect(370, 10, 131, 31))
        self.DurLabel.setObjectName("DurLabel")

        self.ButtonFrame = QtWidgets.QFrame(self.centralwidget)
        self.ButtonFrame.setGeometry(QtCore.QRect(10, 550, 951, 101))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ButtonFrame.setFont(font)
        self.ButtonFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ButtonFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ButtonFrame.setObjectName("ButtonFrame")

        self.AddButton = QtWidgets.QPushButton(self.ButtonFrame)
        self.AddButton.setGeometry(QtCore.QRect(10, 10, 171, 81))
        self.AddButton.setObjectName("AddButton")
        self.AddButton.clicked.connect(self.addClicked)

        self.RunButton = QtWidgets.QPushButton(self.ButtonFrame)
        self.RunButton.setGeometry(QtCore.QRect(580, 10, 171, 81))
        self.RunButton.setObjectName("RunButton")
        self.RunButton.clicked.connect(self.runClicked)

        self.EndButton = QtWidgets.QPushButton(self.ButtonFrame)
        self.EndButton.setGeometry(QtCore.QRect(770, 10, 171, 81))
        self.EndButton.setObjectName("EndButton")
        self.EndButton.clicked.connect(self.endClicked)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 969, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTwitch = QtWidgets.QMenu(self.menubar)
        self.menuTwitch.setObjectName("menuTwitch")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.actionLoad = QtWidgets.QAction(self)
        self.actionLoad.setObjectName("actionLoad")
        self.actionLoad.triggered.connect(self.loadClicked)

        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(self.savePreset)

        self.actionKey = QtWidgets.QAction(self)
        self.actionKey.setObjectName("actionKey")
        self.actionKey.triggered.connect(self.inputTwitchDetails)

        self.actionNew = QtWidgets.QAction(self)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.triggered.connect(self.newClicked)

        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuTwitch.addAction(self.actionKey)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTwitch.menuAction())

        self.runLabel = QtWidgets.QLabel(self.ButtonFrame)
        self.runLabel.setGeometry(QtCore.QRect(190, 20, 361, 61))
        self.runLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.runLabel.setObjectName("runLabel")
        

        self.setWindowTitle("Twitch Chat Plays Customiser")
        self.ChatInpLabel.setText("Chat Input")
        self.KeyPressLabel.setText("Key Press")
        self.DurLabel.setText("Duration")
        self.AddButton.setText("Add Control")
        self.RunButton.setText("Run Controller")
        self.EndButton.setText("End Controller")
        self.menuFile.setTitle("File")
        self.menuTwitch.setTitle("Twitch")

        self.actionLoad.setText("Load Preset")
        self.actionLoad.setStatusTip("Load a previously created preset")
        self.actionLoad.setShortcut("Ctrl+O")

        self.actionSave.setText("Save Preset")
        self.actionSave.setStatusTip("Save the current preset")
        self.actionSave.setShortcut("Ctrl+S")

        self.actionKey.setText("Input Stream Details")
        
        self.actionNew.setText("New Preset")
        self.actionNew.setShortcut("Ctrl+N")

        self.runLabel.setText("Status: Not Connected")

    def addClicked(self):
        self.loaded = True
        self.chat.addCommand("command", "a", 0)
        self.addSinglePresetToList("command", "a", 0, len(self.commandWidgets))

    def runClicked(self):
        if (self.chat.keyFound):
            if (len(self.chat.commands) > 0):
                if not self.t1.is_alive():
                    self.showError("Controller is now running")
                    self.t1.start()
                else:
                    self.showError("Code already running")
            else:
                self.showError("There are no commands to run")
        else:
            self.showError("Stream Key Not Found")
    
    def startControl(self):
        self.chat.active = True
        self.chat.apiConnect()

    def endClicked(self):
        self.chat.endConnection()
        self.runLabel.setText("Status: Not Connected")

    def newClicked(self):
        self.currFunc = "new"
        if self.loaded:
            self.checkSave()
        else:
            self.newPreset()

    def loadClicked(self):
        self.currFunc = "load"
        if self.loaded:
            self.checkSave()
        else:
            self.loadPreset()

    def newPreset(self):
        self.loaded = False
        self.chat.commands = []
        self.resetPresetsList()

    def savePreset(self):
        here = os.path.dirname(os.path.abspath(__file__))
        path = here + "/presets"
        fileName = QFileDialog.getSaveFileName(self, 'Save Preset', path)
        self.chat.saveFile(fileName[0])

    def loadPreset(self):
        here = os.path.dirname(os.path.abspath(__file__))
        path = here + "/presets"
        fileName = QFileDialog.getOpenFileName(self, 'Load Preset', path)
        self.chat.loadFile(fileName[0])
        self.resetPresetsList()
        self.addFullPresetToList()

    def inputTwitchDetails(self):
        self.extW = TwitchInput(self)
        self.extW.show()

    def addFullPresetToList(self):
        i = 0
        for command in self.chat.commands:
            self.addSinglePresetToList(command.message, command.control, command.duration, i)
            i += 1
            
    def addSinglePresetToList(self, message, control, duration, index):
        commWidget = InputWidget(message, control, duration, index, self)
        self.commandWidgets.append(commWidget)
        commNum = len(self.commandWidgets) - 1
        self.commandWidgets[commNum].setMinimumSize(QtCore.QSize(0, 100))
        self.commandWidgets[commNum].setObjectName("command" + str(commNum))
        self.verticalLayout.addWidget(self.commandWidgets[commNum])

    def resetPresetsList(self):
        for commW in self.commandWidgets:
            self.verticalLayout.removeWidget(commW)
            commW.deleteLater()
            commW = None

        self.commandWidgets = []
    
    def deleteSinglePreset(self, index):
        commW = self.commandWidgets[index]

        self.verticalLayout.removeWidget(commW)
        commW.deleteLater()
        commW = None

        self.commandWidgets.pop(index)
        self.chat.commands.pop(index)

        self.resetIndexes()

    def resetIndexes(self):
        for i in range (0, len(self.commandWidgets)):
            self.commandWidgets[i].changeIndex(i)

    def addCommand(self, message, control, duration):
        self.chat.addCommand(message, control, duration)
        self.addSinglePresetToList(self, message, control, duration, len(self.commandWidgets))

    def showError(self, errMessage):
        err = QMessageBox()
        err.setWindowTitle("Notice")
        err.setText(errMessage)

        err.exec_()

    def checkSave(self):
        sav = QMessageBox()
        sav.setWindowTitle("Save")
        sav.setText("Save the current preset first?")
        sav.setStandardButtons(QMessageBox.Save|QMessageBox.No|QMessageBox.Cancel)
        sav.buttonClicked.connect(self.saveButtClicked)

        sav.exec_()
    
    def saveButtClicked(self, button):
        if button.text() == "Save":
            self.savePreset()
            if self.currFunc == "load":
                self.loadPreset()
            elif self.currFunc == "new":
                self.newPreset()
        elif button.text() == "&No":
            if self.currFunc == "load":
                self.loadPreset()
            elif self.currFunc == "new":
                self.newPreset()
        elif button.text() == "Cancel":
            pass

    def closeEvent(self, event):
        if self.chat.active:
            self.endClicked()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())


##  pyuic5 -x [uifile.ui] -o [pythonfile.py]
