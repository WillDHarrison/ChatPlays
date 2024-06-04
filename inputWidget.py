from PyQt5 import QtCore, QtGui, QtWidgets
import os

class InputWidget(QtWidgets.QWidget):
    def __init__(self, message, control, duration, index, mainWindow):
        super(InputWidget, self).__init__()
        self.message = message
        self.control = control
        self.duration = duration
        self.index = index
        self.mainWindow = mainWindow
        self.keys = []
        
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, 'possibleKeyBinds.txt')
        keysFile = open(path, "r")
        keysRaw = keysFile.readlines()
        for i in keysRaw:
            keyRaw = i.strip()
            key = (keyRaw.split("'"))[1]
            self.keys.append(key)

        self.setupUi()


    def setupUi(self):
        self.setObjectName("Form")
        self.resize(906, 68)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.textChanged.connect(self.update)
        
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(210, 10, 131, 41))
        self.comboBox.setObjectName("comboBox")
        for key in self.keys:
            self.comboBox.addItem(key, key)
        self.comboBox.setCurrentIndex(self.keys.index(self.control))
        self.comboBox.currentIndexChanged.connect(self.update)

        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setGeometry(QtCore.QRect(360, 10, 71, 41))
        self.spinBox.setValue(int(self.duration))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.spinBox.setFont(font)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.valueChanged.connect(self.update)

        self.checkBox = QtWidgets.QCheckBox(self)
        self.checkBox.setGeometry(QtCore.QRect(540, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        if self.mainWindow.chat.commands[self.index].enabled:
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setChecked(False)
        self.checkBox.stateChanged.connect(self.enableToggle)

        self.deleteButton = QtWidgets.QPushButton(self)
        self.deleteButton.setGeometry(QtCore.QRect(790, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.deleteButton.setFont(font)
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.deleteClicked)

        self.plainTextEdit.setPlainText(self.message)
        self.checkBox.setText("Enabled")
        self.deleteButton.setText("Delete")

    def update(self):
        self.changeMessage(self.plainTextEdit.toPlainText())
        self.changeControl(self.comboBox.currentData())
        self.changeDuration(self.spinBox.value())
        
    def deleteClicked(self):
        self.mainWindow.deleteSinglePreset(self.index)
        
    def changeMessage(self, newMessage):
        self.mainWindow.chat.commands[self.index].message = newMessage

    def changeControl(self, newControl):
        self.mainWindow.chat.commands[self.index].control = newControl

    def changeDuration(self, newDuration):
        self.mainWindow.chat.commands[self.index].duration = newDuration

    def changeIndex(self, newIndex):
        self.index = newIndex

    def enableToggle(self):
        if self.mainWindow.chat.commands[self.index].enabled:
            self.mainWindow.chat.commands[self.index].enabled = False
        else:
            self.mainWindow.chat.commands[self.index].enabled = True
