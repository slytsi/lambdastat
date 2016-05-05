import os
import glob
import time
import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
#probe path to temperature reading
device_file = '/sys/bus/w1/devices/28-000006c61575/w1_slave'

def read_temp_raw():
	f = open(device_file,'r')
	lines = f.readlines()
	f.close()
	return lines
#this converts from c to f and divides the value by 1000
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

#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

awshost = "youriotendpoint.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "your iot thing name"
thingName = "your iot thing name"
caPath = "path to /VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem"
certPath = "path to your certificate.pem.crt"
keyPath = "path to your private.pem.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

while 1==1:
    sleep(60)
    if connflag == True:
        realtemp01 = (read_temp())
        mqttc.publish("Outside Temperature", realtemp01, qos=1)
        print("Outside Temperature " + "%.2f" % realtemp01 )
    else:
        print("waiting for connection...")
