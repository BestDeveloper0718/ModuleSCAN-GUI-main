#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq


context = zmq.Context()

socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
number=0

operator_name_list = ['John','Alex','Temo']

print('Started')
while number<10:

    #  Wait for next request from client
    print('wait')
    message = socket.recv()

    print("Received request: %s" % message)
    str_message = message.decode('ascii')

    if 'Login action' in  str_message:
        print("login action")
        user_name = str_message.split(':',1)[1]
        if user_name in operator_name_list:
            socket.send(b"Login:1")
        else:
            socket.send(b"Login:0")

    if message == b"Start Command":
        number +=1
    #  Do some 'work'
        time.sleep(1)
        #  Send reply back to client
        
        if (number==7):
            socket.send(b"Scanning Complete")
        elif (number==8):
            #if camera is ok
            #socket.send(b"Camera:1")
            #if camera is false
            print('camera1')
            socket.send(b"Camera1:0")
        elif (number==9):
            #if camera is ok
            #socket.send(b"Camera:1")
            #if camera is false
            socket.send(b"Camera2:1")
        elif (number==10):
            #if camera is ok
            #socket.send(b"Camera:1")
            #if camera is false
            socket.send(b"Camera3:0")
        else:
            socket.send(b"success")