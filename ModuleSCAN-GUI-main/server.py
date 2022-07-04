#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import datetime
from tracemalloc import start
from unicodedata import numeric
import zmq, json, time, schedule


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
