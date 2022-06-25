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
while number<10:
    number +=1
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    
    if (number==7):
        socket.send(b"Scannig Complete")
    elif (number==8):
        #if camera is ok
        #socket.send(b"Camera:1")
        #if camera is false
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