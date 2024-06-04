class ChatController:
    import socket
    import pydirectinput
    import time
    import os.path
    import threading
    import keyboard
    from keyCommand import KeyCommand
    import csv

    def __init__(self, mainWindow):
        self.server = "irc.chat.twitch.tv"
        self.port = 6667
        self.botName = "chatPlays"
        self.auth = ""
        self.channel = ""
        self.sock = self.socket.socket()
        self.keyFound = False
        self.active = False
        self.doConnect = False
        self.commands = []
        self.mainWindow = mainWindow
        self.endKey = 'ctrl+shift+x'
        self.keyboard.add_hotkey(self.endKey, lambda: self.toggleControl())
        here = self.os.path.dirname(self.os.path.abspath(__file__))
        path = self.os.path.join(here, 'streamKey.txt')
        keySaved = self.os.path.exists(path)
        if keySaved:
            self.mainWindow.showError("Saved stream key found \n Twitch Details Loaded")
            keyFile = open(path, "r")
            keyRaw = keyFile.readlines()
            keyFile.close()
            self.channel = keyRaw[0].strip()
            self.auth = keyRaw[1].strip()
            self.keyFound = True
       

    # def printDetails(self):
    #     print(self.server)
    #     print(self.port)
    #     print(self.getBotName())
    #     print(self.getAuth())
    #     print(self.getChannel())

    # def getBotName(self):
    #     return self.botName
    
    # def getAuth(self):
    #     return self.auth
    
    # def getChannel(self):
    #     return self.channel


    def apiConnect(self):
        self.sock = self.socket.socket()
        self.sock.connect((self.server, self.port))
        self.sock.send(f"PASS {self.auth}\n".encode('utf-8'))
        self.sock.send(f"NICK {self.botName}\n".encode('utf-8'))
        self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))
        self.joinChat()

    def joinChat(self):
        self.mainWindow.runLabel.setText("Status: Connecting...")
        self.doConnect = False
        loading = True
        self.sock.settimeout(3)
        while loading:
            try:
                joinMsg = self.sock.recv(1024)
                joinMsg = joinMsg.decode()
            except self.socket.timeout:
                loading = False
            for line in joinMsg.split("\n")[0:-1]:
                print(line)
                if loading:
                    loading = self.loadingComplete(line)
        if self.doConnect:
            print("Running Controller")
            self.runController()
        else:
            print("Connection Failed")
            self.mainWindow.runLabel.setText("Status: Invalid Twitch Details")
            self.endConnection()

    def loadingComplete(self, line):
        if "End of /NAMES list" in line:
            self.sendMessage("CHAT PLAYS IS NOW ACTIVE!")
            self.doConnect = True
            return False
        elif "Improperly formatted auth" in line:
            return False
        elif not line:
            return False
        else:
            return True
    

    def sendMessage(self, message):
        messageTemp = "PRIVMSG " + self.channel + " :" + message
        self.sock.send((messageTemp + "\n").encode())


    def getUser(self, line):
        try:
            lines = line.split(":")
            namesplit = lines[1].split("!")
            return namesplit[0]
        except:
            return ""

    def getMsg(self, line):
        lines = line.split(":")
        return lines[-1]
    
    
    def runController(self):
        self.mainWindow.runLabel.setText("Status: Connected")
        while self.active:
            try:
                readChat = self.sock.recv(1024).decode('utf-8')
            except:
                readChat = ""
            for line in readChat.split("\r\n"):
                currentCommand = []
                username = self.getUser(line)
                msg = self.getMsg(line)
                for command in self.commands:
                    if command.enabled:
                        if msg.lower() == command.message.lower():
                            currentCommand.append(command)
                if not len(currentCommand) == 0:
                    self.gameControl(currentCommand)
                if msg != "":
                    print(username + ": " + msg)


    def gameControl(self, currentCommand):
        print("Command triggered: " + currentCommand[0].message)
        for command in currentCommand:
            self.pydirectinput.keyDown(command.control)

        self.time.sleep(currentCommand[0].duration*0.033)

        for command in currentCommand:
            self.pydirectinput.keyUp(command.control)

    def saveFile(self, filePath):
        if filePath != '':
            fileName = filePath.split('/')[-1]
            if fileName != '':
                if filePath.split('.')[-1] != "csv":
                    filePath = filePath + ".csv"
            with open(filePath, 'w', newline='') as file:
                writer = self.csv.writer(file)
                fields = ["message", "control", "duration"]
                writer.writerow(fields)

                for i in self.commands:
                    writer.writerow([i.message , i.control , i.duration])

                
    def loadFile(self, filePath):
        csvCheck = filePath.split('.')[-1]
        try:
            if csvCheck == 'csv':
                with open(filePath) as file:
                    reader = self.csv.reader(file, delimiter=',')
                    title_line = True
                    self.commands = []
                    for line in reader:
                        if title_line:
                            if not (line[0] == "message" and line[1] == "control" and line[2] == "duration"):
                                raise Exception("Invalid CSV file")
                            title_line = False
                        else:
                            self.addCommand(line[0], line[1], line[2])

                    self.mainWindow.loaded = True
            else:
                raise Exception("Non-CSV file selected")
        except:
            if filePath != "":
                self.mainWindow.showError("Invalid preset file")


    def addCommand(self, message, control, duration):
        self.commands.append(self.KeyCommand(message,control,duration))

    def endConnection(self):
        try:
            self.sendMessage("CHAT PLAYS IS OVER!")
            self.active = False
            self.sock.shutdown(self.socket.SHUT_RDWR)
            self.sock.close()
            self.mainWindow.t1 = self.threading.Thread(target=self.mainWindow.startControl)
        except:
            self.mainWindow.showError("Code isn't running")

    def toggleControl(self):
        if self.active:
            self.mainWindow.endClicked()