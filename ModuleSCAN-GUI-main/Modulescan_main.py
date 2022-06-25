# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 20:37:38 2022

@author: VM
"""

from argparse import ArgumentDefaultsHelpFormatter
import sys
from PyQt5 import QtWidgets, uic, QtSql, QtGui
import sqlite3
import zmq


# QT-Widgets
qtcreator_file  = "ModuleSCAN.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)




class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btn_update_settings.clicked.connect(self.update_setting)
        self.automatically_update()
        self.pushButton_START.clicked.connect(self.send_socket)
        # self.calc_tax_button.clicked.connect(self.CalculateTax)

    # def CalculateTax(self):
    #         price = int(self.price_box.toPlainText())
    #         tax = (self.tax_rate.value())
    #         total_price = price  + ((tax / 100) * price)
    #         total_price_string = "The total price with tax is: " + str(total_price)
    #         self.results_window.setText(total_price_string)

    def send_socket(self):
       #
        #   Hello World client in Python
        #   Connects REQ socket to tcp://localhost:5555
        #   Sends "Hello" to server, expects "World" back
        #

        context = zmq.Context()

        #  Socket to talk to server
        print("Connecting to server…")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        #  Do 10 requests, waiting each time for a response
        for request in range(10):
            print("Sending request %s …" % request)
            socket.send(b"Start Command")

            #  Get the reply.
            message = socket.recv()
            if(message[len(message)-1]==49 and request==7):#Camera1:1
                print("Camera1 is ok")
                self.Camera_1.setText("Camera1 is OK.")
            elif(message[len(message)-1]==48 and request==7): #Camera1:0
                print("Camera1 is false")
                self.Camera_1.setText("<p style='color:red;'>ERROR<p>")

            elif(message[len(message)-1]==49 and request==8):#Camera2:1
                print("Camera2 is ok")
                self.Camera_2.setText("Camera1 is OK.")
            elif(message[len(message)-1]==48 and request==8): #Camera2:0
                print("Camera2 is false")
                self.Camera_2.setText("<p style='color:red;'>ERROR<p>")

            elif(message[len(message)-1]==49 and request==9):#Camera3:1
                print("Camera3 is ok")
                self.Camera_3.setText("Camera1 is OK.")
            elif(message[len(message)-1]==48 and request==9): #Camera3:0
                print("Camera3 is false")
                self.Camera_3.setText("<p style='color:red;'>ERROR<p>")

            else :
                print("Received reply %s [ %s ]" % (request, message))



    def automatically_update(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydb.db')
        with sqlite3.connect('mydb.db') as db:
            cursor=db.cursor()

            cursor.execute("select* from setting where key='modul_1'")
            product=cursor.fetchall()
            product=product[0]
            if(str(product[2])== "1"):
                self.checkBox.setCheckState(2)
            else :
                self.checkBox.setCheckState(0)
            
            cursor.execute("select* from setting where key='modul_2'")
            product=cursor.fetchall()
            product=product[0]
            if(str(product[2])== "1"):
                self.checkBox_2.setCheckState(2)
            else :
                self.checkBox_2.setCheckState(0)

            cursor.execute("select* from setting where key='modul_3'")
            product=cursor.fetchall()
            product=product[0]
            if(str(product[2])== "1"):
                self.checkBox_3.setCheckState(2)
            else :
                self.checkBox_3.setCheckState(0)
            
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

            cursor.execute("select* from setting where key='module_press'")
            product=cursor.fetchall()
            product=product[0]
            self.module_press.setText(str(product[2]))

            cursor.execute("select* from setting where key='test_location'")
            product=cursor.fetchall()
            product=product[0]
            self.test_location.setText(str(product[2]))
        


    def update_setting(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydb.db')
        query = QtSql.QSqlQuery()	
        db.open()
        query.exec_("create table setting(id int primary key, "
        "key varchar(20), value varchar(20))")

        if(self.checkBox.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'modul_1'""")
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'modul_1'""")

        if(self.checkBox_2.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'modul_2'""")
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'modul_2'""")

        if(self.checkBox_3.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'modul_3'""")
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'modul_3'""")

        if(self.checkBox_check_screw.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'check_screw'""")
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'check_screw'""")

        if(self.checkBox_update_DB.isChecked()):
            query.exec_(f"""update setting set value = {'true'} where key = 'update_database'""")
        else:
            query.exec_(f"""update setting set value = {'false'} where key = 'update_database'""")

        module_press = self.module_press.text()
        test_location = self.test_location.text()
        print(module_press)
        query.exec_(f"""update setting set value = '{module_press}' where key = 'module_press'""")
        query.exec_(f"""update setting set value = '{test_location}' where key = 'test_location'""")


        # print("update")
        # query.exec_("insert into setting (key, value ) values('modul_1', '0')")
        # query.exec_("insert into setting (key, value ) values('modul_2', '0')")
        # query.exec_("insert into setting (key, value ) values('modul_3', '0')")
        # query.exec_("insert into setting (key, value ) values('check_screw', '0')")
        # query.exec_("insert into setting (key, value ) values('update_database', '0')")
        # query.exec_("insert into setting (key, value ) values('module_press', '')")
        # query.exec_("insert into setting (key, value ) values('test_location', '')")
        return False
		
	
        
        
    
        return True

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())