import os
import glob
import time
import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
import json

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
device_file = '/sys/bus/w1/devices/28-000006c61575/w1_slave'

awshost = "host.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "shadow"
thingName = "Pi"
iot_topic = "$aws/things/Pi/shadow/update"
caPath = "yourcertpath/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem"
certPath = "yourcertpath/certificate.pem.crt"
keyPath = "yourcertpaths/private.pem.key"

def getTime():
        currenttime=time.localtime()
        return (time.strftime("%Y%m %H%M%S", currenttime))
def read_temp_raw():
	f = open(device_file,'r')
	lines = f.readlines()
	f.close()
	return lines
def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string)  / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return  temp_f

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    print(iot_topic +str(msg.payload))
#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

while 1==1:
    #sleep(5)
    if connflag == True:
        now = getTime()
        realtemp01 = (read_temp())
        #realtemp01 = int(realtemp01)
        payload = json.dumps({
        "state": {
              "reported": {
                      "Temperature": realtemp01
        }
    }
})
        mqttc.publish(iot_topic , payload, qos=1)
        print("Current Temperature ", realtemp01)
        sleep(60)
    else:
        print("waiting for connection...")
        sleep(1)
