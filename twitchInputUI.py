from PyQt5 import QtCore, QtGui, QtWidgets
import os

class TwitchInput(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(TwitchInput, self).__init__()
        self.mainWindow = mainWindow
        self.toSave = False
        self.setupUi()
    
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(449, 200)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.setFont(font)
        self.checkBox = QtWidgets.QCheckBox(self)
        self.checkBox.setGeometry(QtCore.QRect(30, 130, 151, 41))
        self.checkBox.stateChanged.connect(self.saveTrigger)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")

        self.channelNameInput = QtWidgets.QLineEdit(self)
        self.channelNameInput.setGeometry(QtCore.QRect(150, 20, 251, 31))
        self.channelNameInput.setObjectName("channelNameInput")
        self.channelNameInput.setText(self.mainWindow.chat.channel)

        self.streamKeyInput = QtWidgets.QLineEdit(self)
        self.streamKeyInput.setGeometry(QtCore.QRect(150, 70, 251, 31))
        self.streamKeyInput.setObjectName("streamKeyInput")
        self.streamKeyInput.setText(self.mainWindow.chat.auth)
        self.streamKeyInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.streamKeyInput.setStyleSheet('lineedit-password-character: 9679')

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(260, 130, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.confirmClicked)

        self.channelLabel = QtWidgets.QLabel(self)
        self.channelLabel.setGeometry(QtCore.QRect(25, 20, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.channelLabel.setFont(font)
        self.channelLabel.setObjectName("channelLabel")

        self.keyLabel = QtWidgets.QLabel(self)
        self.keyLabel.setGeometry(QtCore.QRect(25, 70, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.keyLabel.setFont(font)
        self.keyLabel.setObjectName("keyLabel")

        self.setWindowTitle("Input Twitch Details")
        self.checkBox.setText("Save Details")
        self.pushButton.setText("Confirm")
        self.channelLabel.setText("Channel Name")
        self.keyLabel.setText("Stream Key")
        
        

    def saveTrigger(self, checked):
        if checked:
            self.toSave = True
        else:
            self.toSave = False

    def confirmClicked(self):
        twitchDetails = [self.getChannelName() + '\n', self.getStreamKey() + '\n']
        self.mainWindow.chat.channel = twitchDetails[0].strip()
        self.mainWindow.chat.auth = twitchDetails[1].strip()
        if twitchDetails[1].strip() != "":
            self.mainWindow.chat.keyFound = True
        else:
            self.mainWindow.chat.keyFound = False
        if self.toSave:
            here = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(here, 'streamKey.txt')
            preset_file = open(path, "w")
            preset_file.writelines(twitchDetails)
            preset_file.close()
        self.close()

    def getChannelName(self):
        a = self.channelNameInput.text()
        if a != "":
            if a[0] != "#":
                a = "#" + a
        return a

    def getStreamKey(self):
        return self.streamKeyInput.text()
