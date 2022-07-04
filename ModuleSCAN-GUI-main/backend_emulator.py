#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import datetime
from tracemalloc import start
from unicodedata import numeric
import zmq, json, time, schedule
from threading import Thread

startedAt=""
finishedAt = ""

#receive result into json file from device
result = {
  "Overallresult": "1",
  "SCAN-ID": "6453272",
  "MODULES": "1 1 1",
  "SCREWS": "1",
  "Module1": {
    "RESULT": "0",
    "PIN1": "0",
    "PIN2": "0",
    "PIN3": "0",
    "PIN4": "0",
    "PIN5": "0",
    "PIN6": "0",
    "PIN7": "0",
    "PIN8": "0",
    "PIN9": "0",
    "PIN10": "0",
    "PIN11": "0",
    "PIN12": "0",
    "PIN13": "0",
    "PIN14": "0",
    "PIN15": "0",
    "SCREW1": "0",
    "SCREW2": "0",
    "SCREW3": "0",
    "SCREW4": "0",
    "P1": "0",
    "AOI": "1",
    "QRCODE1":"1432142323",
    "QRCODE2" : "1343421",
    "QRCODE3" : "14343454 - A 07 - 02 637289362"
  },
  "Module2": {
    "RESULT": "0",
    "PIN1": "0",
    "PIN2": "0",
    "PIN3": "0",
    "PIN4": "0",
    "PIN5": "0",
    "PIN6": "0",
    "PIN7": "0",
    "PIN8": "0",
    "PIN9": "0",
    "PIN10": "0",
    "PIN11": "0",
    "PIN12": "0",
    "PIN13": "0",
    "PIN14": "0",
    "PIN15": "0",
    "SCREW1": "0",
    "SCREW2": "0",
    "SCREW3": "0",
    "SCREW4": "0",
    "P1": "0",
    "AOI": "1",
    "QRCODE1":"1432142323",
    "QRCODE2" : "1343421",
    "QRCODE3" : "14343454 - A 07 - 02 637289362"

  },
  "Module3":{
    "RESULT": "0",
    "PIN1": "0",
    "PIN2": "0",
    "PIN3": "0",
    "PIN4": "0",
    "PIN5": "0",
    "PIN6": "0",
    "PIN7": "0",
    "PIN8": "0",
    "PIN9": "0",
    "PIN10": "0",
    "PIN11": "0",
    "PIN12": "0",
    "PIN13": "0",
    "PIN14": "0",
    "PIN15": "0",
    "SCREW1": "0",
    "SCREW2": "0",
    "SCREW3": "0",
    "SCREW4": "0",
    "P1": "0",
    "AOI": "1",
    "QRCODE1":"1432142323",
    "QRCODE2" : "1343421",
    "QRCODE3" : "14343454 - A 07 - 02 637289362"

  }
}

json_string = json.dumps(result)
Result_json = json.loads(json_string)
#save json file per each module
module1 = {
  "user_id" : "C600001A8B6F9301",
  "test_system_identification" : "test_system_igbt_module",
  "igbt_module_serial_number": "QRCODE1",
  "pass": result["Module1"]["RESULT"],
  "results" : result,
  "step" : 1,
  "error_message": 0,
  "comment": 0,
  "test_system" : "2022VMM001",
  "test_position" : 1,
  "startedAt" : startedAt,
  "finishedAt": finishedAt
}

module2 = {
  "user_id" : "C600001A8B6F9301",
  "test_system_identification" : "test_system_igbt_module",
  "igbt_module_serial_number": "QRCODE1",
  "pass": result["Module2"]["RESULT"],
  "results" : result,
  "step" : 1,
  "error_message": 0,
  "comment": 0,
  "test_system" : "2022VMM001",
  "test_position" : 2,
  "startedAt" : startedAt,
  "finishedAt": finishedAt
}

module3 = {
  "user_id" : "C600001A8B6F9301",
  "test_system_identification" : "test_system_igbt_module",
  "igbt_module_serial_number": "QRCODE1",
  "pass": result["Module3"]["RESULT"],
  "results" : result,
  "step" : 1,
  "error_message": 0,
  "comment": 0,
  "test_system" : "2022VMM001",
  "test_position" : 3,
  "startedAt" : startedAt,
  "finishedAt": finishedAt
}
main_flag=False
schedule_id=0

def main_schedule():
  while True:
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5554")
    for number in range(8):
      if(number<6):
        message = socket.recv() 
        print("Received request %s: %s" %(number, message))
        socket.send(b"Scanning")
        #//-----------------------------------------when the scanning is completed-------------------
      elif(number==6):
        message = socket.recv() 
        print("Received request %s: %s" %(number, message))

        socket.send(b"Scanning completed")
        now = datetime.datetime.now()
        # current_time = now.strftime("")
        path = "_{}_{}_{}_{}_{}_{}.json".format(now.year,now.month, now.day, now.hour, now.minute, now.second)

        
        with open("Module1_"+path, 'w') as outfile:
            json.dump(module1,outfile)
        with open("Module2_"+path, 'w') as outfile:
            json.dump(module2,outfile)
        with open("Module3_"+path, 'w') as outfile:
            json.dump(module3,outfile)
      else:
        msg=socket.recv()
        message_json=json.dumps(result)
        socket.send_json(message_json)
    time.sleep(1)

def receive_updated_setting():
  while True:
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5553")
    message = socket.recv() 
    print("received settings")
    if(message.strip()==b'Request updating settings'):      
        socket.send(b"Ready to update settings")
        msg = json.loads(socket.recv_json())
        socket.send(b"update success")
        print(msg)
        if(msg["module_1"]):#//----------------------------received status json 
          if(msg["module_1"]==1):
            pass
          else:
            pass
          if(msg["module_2"]==1):
            pass
          else:
            pass
          if(msg["module_3"]==1):
            pass
          else:
            pass
          if(msg["screws"]==1):
            pass
          else:
            pass
          if(msg["update_db"]==1):
            pass
          else:
            pass
          if(msg["http_post"]==1):
            pass
          else:
            pass
          if(msg["save_json"]==1):
            now = datetime.datetime.now()
            # current_time = now.strftime("")
            global startedAt, finishedAt
            filepath = "Result_{}_{}_{}_{}_{}_{}.json".format(now.year,now.month, now.day, now.hour, now.minute, now.second)
            startedAt = "Result_{}_{}_{}_{}_{}_{}.json".format(now.year,now.month, now.day, now.hour, now.minute, now.second-7)
            finishedAt = filepath
            with open(filepath, 'w') as outfile:
                json.dump(json_string,outfile)
    time.sleep(1)


def send_status():
  while True:
    print("ok")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    message_Dict={
            "CAMERA1":"0",
            "CAMERA2":"0",
            "CAMERA3":"1",
            "LASER_SCANNER":"0",
            "CONTROL_UNIT":"0",
            "LIGHT_CURTAIN":"0",
            "LINER_RAXIS":"1"
        }
    message_json=json.dumps(message_Dict)
    socket.send_json(message_json)
    time.sleep(1)
  

send_state = Thread(target=send_status)
send_scannig = Thread(target=main_schedule)
receive_setting = Thread(target=receive_updated_setting)
send_scannig.start()
send_state.start()
receive_setting.start()
# schedule.every(1).second.do(receive_updated_setting)
# schedule.every(1).second.do(send_status)
# schedule_id = schedule.every(1).second.do(main_schedule)


# while True:
#     schedule.run_pending()
#     time.sleep(1)
#         #  Wait for next request from client  
   
    

  
