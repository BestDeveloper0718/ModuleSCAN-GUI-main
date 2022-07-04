# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 20:37:38 2022

@author: VM
"""

from argparse import ArgumentDefaultsHelpFormatter
import sys, time
from threading import Thread
from PyQt5 import QtWidgets, QtSql, QtGui, uic
from PyQt5.QtCore import QThread, Qt, QPoint, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox,QInputDialog;
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import zmq, json, sqlite3, hashlib,threading, schedule,requests


# QT-Widgets
qtcreator_file  = "ModuleSCAN.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)



class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('ModuleSCAN.ui',self)
        self.show()
        self.login_flag=False
        self.setting_flag = False
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('mydb.db')
        self.btn_update_settings.clicked.connect(self.update_setting)
        self.automatically_update()
        self.schedule_id=0
        pixmap = QPixmap('Module.png')
        self.pushButton_START.setEnabled(True)
        self.Camera_1.setScaledContents(True)
        self.Camera_1.setPixmap(pixmap)
        self.Camera_1.setStyleSheet("QLabel { border: 5px solid grey ;  border-radius: 5px;}")
        self.Camera_2.setScaledContents(True)
        self.Camera_2.setPixmap(pixmap)
        self.Camera_2.setStyleSheet("QLabel { border: 5px solid grey ;  border-radius: 5px;}")
        self.Camera_3.setStyleSheet("QLabel { border: 5px solid grey ;  border-radius: 5px;}")
        self.Camera_3.setScaledContents(True)
        self.Camera_3.setPixmap(pixmap)
        self.lineEdit_operator.setFocus(True)
        self.pushButton_START.clicked.connect(self.start_button_clicked)
        self.pushButton_LOGIN_LOGOUT.clicked.connect(self.login)
        self.tabWidget.currentChanged.connect(self.password)
        self.pushButton_START.setEnabled(False)

        self.status=""
        self.label_list = []
        self.scan_module1=True
        self.scan_module2=True
        self.scan_module3=True
        self.automatically_update()
        self.receive_status = Thread(target=self.receive_status)
        self.receive_status.start()
        self.timer = QTimer()
        self.timer.timeout.connect(self.set_state)
        self.timer.start(1000)

        
    

    def set_state(self):
        msg = self.status
        if(msg["CAMERA1"]=="1"):
            self.label_text_Cam1_OK.setText("<p style='color:green;'>OK<p>")
            pixmap = QPixmap('Module.png')
            self.Camera_1.setScaledContents(True)
            self.Camera_1.setPixmap(pixmap)
        else:
            self.Camera_1.setText("<p style='color:red;'>ERROR<p>")
            self.label_text_Cam1_OK.setText("<p style='color:red;'>ERROR<p>")

        if(msg["CAMERA2"]=="1"):
            self.label_text_Cam2_OK.setText("<p style='color:green;'>OK<p>")
            pixmap = QPixmap('Module.png')
            self.Camera_2.setScaledContents(True)
            self.Camera_2.setPixmap(pixmap)
        else:
            self.Camera_2.setText("<p style='color:red;'>ERROR<p>")
            self.label_text_Cam2_OK.setText("<p style='color:red;'>ERROR<p>")
            

        if(msg["CAMERA3"]=="1"):
            self.label_text_Cam3_OK.setText("<p style='color:green;'>OK<p>")
            pixmap = QPixmap('Module.png')
            self.Camera_3.setScaledContents(True)
            self.Camera_3.setPixmap(pixmap)
        else:
            self.Camera_3.setText("<p style='color:red;'>ERROR<p>")
            self.label_text_Cam3_OK.setText("<p style='color:red;'>ERROR<p>")

        if(msg["LASER_SCANNER"]=="1"):
            self.label_text_laserscanner_OK.setText("<p style='color:green;'>OK<p>")
        else:
            self.label_text_laserscanner_OK.setText("<p style='color:red;'>ERROR<p>")

        if(msg["CONTROL_UNIT"]=="1"):
            self.label_text_ControlUnit_OK.setText("<p style='color:green;'>OK<p>")
        else:
            self.label_text_ControlUnit_OK.setText("<p style='color:red;'>ERROR<p>")

        if(msg["LIGHT_CURTAIN"]=="1"):
            self.label_text_LightCurtain_OK.setText(" <p style='color:green;'>OK<p>")
        else:
            self.label_text_LightCurtain_OK.setText("<p style='color:red;'>ERROR<p>")

        if(msg["LINER_RAXIS"]=="1"):
            self.label_text_LinearAxis_OK_2.setText("<p style='color:green;'>OK<p>")
        else:
            self.label_text_LinearAxis_OK_2.setText("<p style='color:red;'>ERROR<p>")

    def receive_status(self):
        while True:
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind("tcp://*:5555")
            status = socket.recv_json()
            self.status = json.loads(status)
            print(status)

    result=""

                
    def login(self):
        if(self.pushButton_LOGIN_LOGOUT.text()=="LOG OUT"):
            self.pushButton_START.setEnabled(False)
            self.lineEdit_operator.setEnabled(True)
            self.lineEdit_operator.clear()
            self.pushButton_LOGIN_LOGOUT.setText("LOGIN")
        elif(self.lineEdit_operator.text()=="C600001A8B6F9301"):
            self.pushButton_START.setEnabled(True)
            QMessageBox.information(self, 'Inform', "Login success. Congratulation!", QMessageBox.Ok)
            self.lineEdit_operator.setEnabled(False)
            self.pushButton_LOGIN_LOGOUT.setText("LOG OUT")
            self.login_flag=True
        else:
            QMessageBox.information(self, 'Warning', "Tag Id is InCorrect!", QMessageBox.Ok)

    def password (self, event):
        if(event==0):
            self.setting_flag=False
        if(self.setting_flag):
            self.tabWidget.setCurrentIndex(event)
        else:
            self.tabWidget.setCurrentIndex(0)
        print(event )
        for label in self.label_list:
            label.show()
        if (event == 1 and not self.setting_flag):            
            text, ok = QInputDialog.getText(self, 'Password', 'Input Password')
            if (ok and hashlib.md5(text.encode()).hexdigest()=="e5d875fa758ae48c78040c151039af66"):
                self.setting_flag = True
                self.tabWidget.setCurrentIndex(1)
                for label in self.label_list:
                    label.hide()

                
            else:
                QMessageBox.information(self, 'Warning', "Password is InCorrect!", QMessageBox.Ok)
      

    def scan(self):
        context = zmq.Context()
        #  Socket to talk to server
        print("Connecting to server…")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5554")
        message=""
        for request in range(8):
            print("Sending request %s …" % request)
            if(request<7):
                socket.send(b"Start Command")
                message = socket.recv()
                print("Received reply %s [ %s ]" % (request, message))
            
            #  Get the reply.            
            elif(message.strip()==b'Scanning completed'):#//-------------------------------receive result json file form backend
                socket.send(b"send result")
                global result
                result = json.loads(socket.recv_json())
                print(result)
        return result                


    def start_button_clicked(self):
        self.start_scan = Thread(target=self.scan)
        global result
        result = self.start_scan.start()
        self.start_scan.join()
        print(result)
        self.label_list.clear()
        if(result["Overallresult"]=="1"):
            self.overallresult.setText("<p style='color:green;'>PASSED<p>")
        else:
            self.overallresult.setText("<p style='color:red;'>FAILDED<p>")
        if(result["Module1"]["RESULT"]=="1" and self.scan_module1):
            self.Camera_1.setStyleSheet("QLabel { border: 5px solid green ;  border-radius: 5px;}")
        elif(self.scan_module1):
            self.Camera_1.setStyleSheet("QLabel { border: 5px solid red ;  border-radius: 5px;}")
            if(result["Module1"]["PIN9"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(202,205)
                self.label_list.append(label)
            if(result["Module1"]["PIN10"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(213,205)
                self.label_list.append(label)
            if(result["Module1"]["PIN11"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(262,205)
                self.label_list.append(label)
            if(result["Module1"]["PIN12"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(274,205)
                self.label_list.append(label)
            if(result["Module1"]["PIN13"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(309,205)
                self.label_list.append(label)
            if(result["Module1"]["PIN14"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(360,205)
                self.label_list.append(label)
            if(result["Module1"]["PIN15"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(371,205)
                self.label_list.append(label)
            if(result["Module1"]["PIN8"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(213,285)
                self.label_list.append(label)
            if(result["Module1"]["PIN7"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(236,285)
                self.label_list.append(label)
            if(result["Module1"]["PIN6"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(275,285)
                self.label_list.append(label)
            if(result["Module1"]["PIN5"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(300,285)
                self.label_list.append(label)
            if(result["Module1"]["PIN14"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(322,285)
                self.label_list.append(label)
            if(result["Module1"]["PIN3"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(334,285)
                self.label_list.append(label)
            if(result["Module1"]["PIN2"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(356,285)
                self.label_list.append(label)
            if(result["Module1"]["PIN1"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(367,285)
                self.label_list.append(label)
            if(result["Module1"]["SCREW3"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(186,221)
                self.label_list.append(label)
            if(result["Module1"]["SCREW4"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(385,221)
                self.label_list.append(label)
            if(result["Module1"]["SCREW2"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(186,266)
                self.label_list.append(label)
            if(result["Module1"]["SCREW1"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(387,266)
                self.label_list.append(label)
            if(result["Module1"]["P1"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(25,65)
                label.show()
                label.setStyleSheet("QLabel { border: 5px solid red ;  border-radius: 5px;}")
                label.move(404,268)
                self.label_list.append(label)


        if(result["Module2"]["RESULT"]=="1" and self.scan_module2):
            self.Camera_2.setStyleSheet("QLabel { border: 5px solid green ;  border-radius: 5px;}")
        elif(self.scan_module2):
            self.Camera_2.setStyleSheet("QLabel { border: 5px solid red ;  border-radius: 5px;}")
            if(result["Module2"]["PIN9"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(202,375)
                self.label_list.append(label)
                
            if(result["Module2"]["PIN10"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(213,375)
                self.label_list.append(label)
            if(result["Module2"]["PIN11"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(262,375)
                self.label_list.append(label)
            if(result["Module2"]["PIN12"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(274,375)
                self.label_list.append(label)
            if(result["Module2"]["PIN13"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(309,375)
                self.label_list.append(label)
            if(result["Module2"]["PIN14"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(360,375)
                self.label_list.append(label)
            if(result["Module2"]["PIN15"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(371,375)
                self.label_list.append(label)
            if(result["Module2"]["PIN8"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(213,455)
                self.label_list.append(label)
            if(result["Module2"]["PIN7"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(236,455)
                self.label_list.append(label)
            if(result["Module2"]["PIN6"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(275,455)
                self.label_list.append(label)
            if(result["Module2"]["PIN5"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(300,455)
                self.label_list.append(label)
            if(result["Module2"]["PIN4"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(322,455)
                self.label_list.append(label)
            if(result["Module2"]["PIN3"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(334,455)
                self.label_list.append(label)
            if(result["Module2"]["PIN2"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(356,455)
                self.label_list.append(label)
            if(result["Module2"]["PIN1"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(367,455)
                self.label_list.append(label)
            if(result["Module2"]["SCREW3"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(186,221+170)
                self.label_list.append(label)
            if(result["Module2"]["SCREW4"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(385,221+170)
                self.label_list.append(label)
            if(result["Module2"]["SCREW2"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(186,266+170)
                self.label_list.append(label)
            if(result["Module2"]["SCREW1"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(387,266+170)
                self.label_list.append(label)
            if(result["Module2"]["P1"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(25,65)
                label.show()
                label.setStyleSheet("QLabel { border: 5px solid red ;  border-radius: 5px;}")
                label.move(404,438)
                self.label_list.append(label)

        if(result["Module3"]["RESULT"]=="1" and self.scan_module3):
            self.Camera_3.setStyleSheet("QLabel { border: 5px solid green ;  border-radius: 5px;}")
        elif(self.scan_module3):
            self.Camera_3.setStyleSheet("QLabel { border: 5px solid red ;  border-radius: 5px;}")
            if(result["Module3"]["PIN9"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(202,545)
                self.label_list.append(label)                        
            if(result["Module3"]["PIN10"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(213,545)
                self.label_list.append(label)
            if(result["Module3"]["PIN11"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(262,545)
                self.label_list.append(label)
            if(result["Module3"]["PIN12"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(274,545)
                self.label_list.append(label)
            if(result["Module3"]["PIN13"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(309,545)
                self.label_list.append(label)
            if(result["Module3"]["PIN14"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(360,545)
                self.label_list.append(label)
            if(result["Module3"]["PIN15"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(371,545)
                self.label_list.append(label)
            if(result["Module3"]["PIN8"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(213,625)
                self.label_list.append(label)
            if(result["Module3"]["PIN7"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(236,625)
                self.label_list.append(label)
            if(result["Module3"]["PIN6"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(275,625)
                self.label_list.append(label)
            if(result["Module3"]["PIN5"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(300,625)
                self.label_list.append(label)
            if(result["Module3"]["PIN4"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(322,625)
                self.label_list.append(label)
            if(result["Module3"]["PIN3"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(334,625)
                self.label_list.append(label)
            if(result["Module3"]["PIN2"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(356,625)
                self.label_list.append(label)
            if(result["Module3"]["PIN1"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(367,625)
                self.label_list.append(label)
            if(result["Module3"]["SCREW3"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(186,221+340)
                self.label_list.append(label)
            if(result["Module3"]["SCREW4"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(385,221+340)
                self.label_list.append(label)
            if(result["Module3"]["SCREW2"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(186,266+340)
                self.label_list.append(label)
            if(result["Module3"]["SCREW1"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(10,10)
                label.show()
                label.setPixmap(QPixmap("red_circle.png"))
                label.move(387,266+340)
                self.label_list.append(label)
            if(result["Module3"]["P1"]=="0"):
                label = QLabel(self)
                label.setScaledContents(True)
                label.resize(25,65)
                label.show()
                label.setStyleSheet("QLabel { border: 5px solid red ;  border-radius: 5px;}")
                label.move(404,608)
                self.label_list.append(label)

        if(result["Module1"]["P1"]=="1"):
            self.module1_P1_connector.setText("<p style='color:green;'>OK<p>")
        else:
            self.module1_P1_connector.setText("<p style='color:red;'>ERROR<p>")
        if(result["Module1"]["AOI"]=="1"):
            self.module1_AOI.setText("<p style='color:green;'>OK<p>")
        else:
            self.module1_AIO.setText("<p style='color:red;'>ERROR<p>")
        if(result["Module2"]["P1"]=="1"):
            self.module2_P1_connector.setText("<p style='color:green;'>OK<p>")
        else:
            self.module2_P1_connector.setText("<p style='color:red;'>ERROR<p>")
        if(result["Module2"]["AOI"]=="1"):
            self.module2_AOI.setText("<p style='color:green;'>OK<p>")
        else:
            self.module2_AIO.setText("<p style='color:red;'>ERROR<p>")
        if(result["Module3"]["P1"]=="1"):
            self.module3_P1_connector.setText("<p style='color:green;'>OK<p>")
        else:
            self.module3_P1_connector.setText("<p style='color:red;'>ERROR<p>")
        if(result["Module3"]["AOI"]=="1"):
            self.module3_AOI.setText("<p style='color:green;'>OK<p>")
        else:
            self.module3_AIO.setText("<p style='color:red;'>ERROR<p>")
        if(result["Module1"]["SCREW1"]=="1" and result["Module1"]["SCREW2"]=="1" and result["Module1"]["SCREW3"]=="1" and result["Module1"]["SCREW4"]=="1"):
            self.module1_screws.setText("<p style='color:green;'>OK<p>")
        else:
            self.module1_screws.setText("<p style='color:red;'>ERROR<p>")
        if(result["Module2"]["SCREW1"]=="1" and result["Module2"]["SCREW2"]=="1" and result["Module2"]["SCREW3"]=="1" and result["Module2"]["SCREW4"]=="1"):
            self.module2_screws.setText("<p style='color:green;'>OK<p>")
        else:
            self.module2_screws.setText("<p style='color:red;'>ERROR<p>")
        if(result["Module3"]["SCREW1"]=="1" and result["Module3"]["SCREW2"]=="1" and result["Module3"]["SCREW3"]=="1" and result["Module3"]["SCREW4"]=="1"):
            self.module3_screws.setText("<p style='color:green;'>OK<p>")
        else:
            self.module3_screws.setText("<p style='color:red;'>ERROR<p>") 
        if(result["Module1"]["PIN1"]=="1" and result["Module1"]["PIN2"]=="1" and result["Module1"]["PIN3"]=="1" and result["Module1"]["PIN4"]=="1" and result["Module1"]["PIN5"]=="1" and result["Module1"]["PIN6"]=="1" and result["Module1"]["PIN7"]=="1" and result["Module1"]["PIN8"]=="1" and result["Module1"]["PIN9"]=="1" and result["Module1"]["PIN10"]=="1" and result["Module1"]["PIN11"]=="1" and result["Module1"]["PIN12"]=="1" and result["Module1"]["PIN13"]=="1" and result["Module1"]["PIN14"]=="1" and result["Module1"]["PIN15"]=="1"):
            self.module1_pressfit_pins.setText("<p style='color:green;'>OK<p>")
        else:
            self.module1_pressfit_pins.setText("<p style='color:red;'>ERROR<p>")
        if(result["Module2"]["PIN1"]=="1" and result["Module2"]["PIN2"]=="1" and result["Module2"]["PIN3"]=="1" and result["Module2"]["PIN4"]=="1" and result["Module2"]["PIN5"]=="1" and result["Module2"]["PIN6"]=="1" and result["Module2"]["PIN7"]=="1" and result["Module2"]["PIN8"]=="1" and result["Module2"]["PIN9"]=="1" and result["Module2"]["PIN10"]=="1" and result["Module2"]["PIN11"]=="1" and result["Module2"]["PIN12"]=="1" and result["Module2"]["PIN13"]=="1" and result["Module2"]["PIN14"]=="1" and result["Module2"]["PIN15"]=="1"):
            self.module2_pressfit_pin.setText("<p style='color:green;'>OK<p>")
        else:
            self.module2_pressfit_pin.setText("<p style='color:red;'>ERROR<p>")
        if(result["Module3"]["PIN1"]=="1" and result["Module3"]["PIN2"]=="1" and result["Module3"]["PIN3"]=="1" and result["Module3"]["PIN4"]=="1" and result["Module3"]["PIN5"]=="1" and result["Module3"]["PIN6"]=="1" and result["Module3"]["PIN7"]=="1" and result["Module3"]["PIN8"]=="1" and result["Module3"]["PIN9"]=="1" and result["Module3"]["PIN10"]=="1" and result["Module3"]["PIN11"]=="1" and result["Module3"]["PIN12"]=="1" and result["Module3"]["PIN13"]=="1" and result["Module3"]["PIN14"]=="1" and result["Module3"]["PIN15"]=="1"):
            self.module3_pressfit_pins.setText("<p style='color:green;'>OK<p>")
        else:
            self.module3_pressfit_pins.setText("<p style='color:red;'>ERROR<p>")

        self.module1_QR1.setText(result["Module1"]["QRCODE1"])
        self.module1_QR2.setText(result["Module1"]["QRCODE2"])
        self.module1_QR3.setText(result["Module1"]["QRCODE3"])
        self.module2_QR1.setText(result["Module2"]["QRCODE1"])
        self.module2_QR2.setText(result["Module2"]["QRCODE2"])
        self.module2_QR3.setText(result["Module2"]["QRCODE3"])
        self.module3_QR1.setText(result["Module3"]["QRCODE1"])
        self.module3_QR2.setText(result["Module3"]["QRCODE2"])
        self.module3_QR3.setText(result["Module3"]["QRCODE3"])


    def automatically_update(self):        
        with sqlite3.connect('mydb.db') as db:
            cursor=db.cursor()
            cursor.execute("select* from setting where key='modul_1'")
            product=cursor.fetchall()
            product=product[0]
            if(str(product[2])== "1"):
                self.checkBox.setCheckState(2)
                self.scan_module1=True
            else :
                self.checkBox.setCheckState(0)
                self.scan_module1=False
            
            cursor.execute("select* from setting where key='modul_2'")
            product=cursor.fetchall()
            product=product[0]
            if(str(product[2])== "1"):
                self.checkBox_2.setCheckState(2)
                self.scan_module2=True
            else :
                self.checkBox_2.setCheckState(0)
                self.scan_module2=False

            cursor.execute("select* from setting where key='modul_3'")
            product=cursor.fetchall()
            product=product[0]
            if(str(product[2])== "1"):
                self.checkBox_3.setCheckState(2)
                self.scan_module3=True
            else :
                self.checkBox_3.setCheckState(0)
                self.scan_module3=False
            
            cursor.execute("select* from setting where key='check_screw'")
            product=cursor.fetchall()
            product=product[0]
            if(str(product[2])== "1"):
                self.checkBox_check_screw.setCheckState(2)
            else :
                self.checkBox_check_screw.setCheckState(0)

            cursor.execute("select* from setting where key='update_database'")
            product=cursor.fetchall()
            product=product[0]
            if(str(product[2])== "1"):
                self.checkBox_update_DB.setCheckState(2)
            else :
                self.checkBox_update_DB.setCheckState(0)

            cursor.execute("select* from setting where key='HTTP_POST'")
            product=cursor.fetchall()
            product=product[0]
            if(str(product[2])== "1"):
                self.checkBox_http_post.setCheckState(2)
            else :
                self.checkBox_http_post.setCheckState(0)

            cursor.execute("select* from setting where key='save_json'")
            product=cursor.fetchall()
            product=product[0]
            if(str(product[2])== "1"):
                self.save_json.setCheckState(2)
            else :
                self.save_json.setCheckState(0)
            cursor.execute("select* from setting where key='module_press'")
            product=cursor.fetchall()
            product=product[0]
            self.module_press.setText(str(product[2]))

            cursor.execute("select* from setting where key='test_location'")
            product=cursor.fetchall()
            product=product[0]
            self.test_location.setText(str(product[2]))
        # self.send_updated_setting()
           
    def update_setting(self):

        query = QtSql.QSqlQuery()	
        self.db.open()

        if(self.checkBox.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'modul_1'""")
            self.scan_module1=True
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'modul_1'""")
            self.scan_module1=False

        if(self.checkBox_2.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'modul_2'""")
            self.scan_module2=True
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'modul_2'""")
            self.scan_module2=False

        if(self.checkBox_3.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'modul_3'""")
            self.scan_module3=True
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'modul_3'""")
            self.scan_module3=False

        if(self.checkBox_check_screw.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'check_screw'""")
            screw = 1
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'check_screw'""")
            screw = 0

        if(self.checkBox_update_DB.isChecked()):
            update_db = 1
            query.exec_(f"""update setting set value = {'true'} where key = 'update_database'""")
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'update_database'""")
            update_db = 0

        if(self.checkBox_http_post.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'HTTP_POST'""")
            http_post = 1
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'HTTP_POST'""")
            http_post = 0

        if(self.save_json.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'save_json'""")
            save_json = 1
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'save_json'""")
            save_json = 0

        module_press = self.module_press.text()
        test_location = self.test_location.text()
        query.exec_(f"""update setting set value = '{module_press}' where key = 'module_press'""")
        query.exec_(f"""update setting set value = '{test_location}' where key = 'test_location'""")
                
        self.db.close()
        self.send_updated_setting()

    def send_updated_setting(self):
        context = zmq.Context()
        #  Socket to talk to server
        print("Connecting to server…")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5553")
        socket.send(b"Request updating settings")
        module_1 = self.checkBox.isChecked()
        module_2 = self.checkBox_2.isChecked()
        module_3 = self.checkBox_3.isChecked()
        screw = self.checkBox_check_screw.isChecked()
        update_db = self.checkBox_update_DB.isChecked()
        http_post = self.checkBox_http_post.isChecked()
        save_json = self.save_json.isChecked()
        module_press = self.module_press.text()
        test_location = self.test_location.text()
        sending_data = {
            "module_1" : module_1,
            "module_2" : module_2,
            "module_3" : module_3,
            "screws" : screw,
            "update_db" : update_db,
            "http_post" : http_post,
            "save_json" : save_json,
            "module_press" : module_press,
            "test_location" : test_location
        }
        message = socket.recv()
        print(message)
        if(message.strip()==b'Ready to update settings'):
            message_json=json.dumps(sending_data)
            socket.send_json(message_json)
            msg = socket.recv()
            print(msg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())