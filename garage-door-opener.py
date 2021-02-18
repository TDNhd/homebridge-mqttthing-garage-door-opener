from configparser import ConfigParser
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

#Reads config.ini file
config_location = 'home/pi/garage/config.ini'
config = ConfigParser()
config.read(config_location)

broker = str(config['mqtt']['brokerAddress'])
port = (config['mqtt']['port'])     #Port "8883" needed when running SSL/TLS encrypted connection (default TCP/IP port is 1883)
clientID = (config['mqtt']['client_id'])
tls_set = (config['tls']['tls_set'])
if tls_set:
    CA_crt = str(config['tls']['CA_crt'])
    Client_crt = str(config['tls']['Client_crt'])
    Client_key = str(config['tls']['Client_key'])
    tls_insecure_set = (config['tls']['tls_insecure_set'])
else:
    CA_crt = Client_crt = Client_key = tls_insecure_set = None
relay = (config['GPIO']['relay'])
reedOpen = (config['GPIO']['reedOpen'])
reedClosed = (config['GPIO']['reedClosed'])

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(reedOpen, GPIO.IN)
GPIO.setup(reedClosed, GPIO.IN)
GPIO.setup(relay, GPIO.OUT)

status = ""
last = ""
stopped = False

def relay_on_off():
    GPIO.output(relay, True)
    time.sleep(0.5)
    GPIO.output(relay, False)
    
#Takes input, controlls door and Sends door status when it's assumed
def on_message(client, userdata, message):
    global stopped
    setTargetDoorState = str(message.payload.decode("utf-8"))
    if GPIO.input(reedOpen) == 0 and GPIO.input(reedClosed) == 0 and stopped == False:
        client.publish(topic="garage/getCurrentDoorState", payload="Stopped", qos=1, retain=True)
        relay_on_off()
        stopped = True
    
    elif GPIO.input(reedOpen) == 0 and GPIO.input(reedClosed) == 0 and stopped == True:
        if last == "Opening":
            publish = "Closing"
            target = "close"
        else :
            publish = "Opening"
            target = "open"
        client.publish(topic="garage/getCurrentDoorState", payload=publish, qos=1, retain=True)
        client.publish(topic="garage/getTargetDoorState", payload=target, qos=1, retain=True)
        relay_on_off()
        stopped = False

    elif setTargetDoorState == "open" and GPIO.input(reedOpen) == 0:
        client.publish(topic="garage/getTargetDoorState", payload="open", qos=1, retain=True)
        relay_on_off()

    elif setTargetDoorState == "close" and GPIO.input(reedClosed) == 0:
        client.publish(topic="garage/getTargetDoorState", payload="close", qos=1, retain=True)
        relay_on_off()

#Connects to mqtt Broker    
client = mqtt.Client(client_id=clientID, clean_session=False)
client.on_message=on_message
if tls_set:
    client.tls_set(ca_certs=CA_crt, certfile=Client_crt, keyfile=Client_key)     #Only needed when running SSL/TLS encrypted connection
    client.tls_insecure_set(tls_insecure_set)       #Needed when certificate is self-signed
client.connect(host=broker, port=port)
client.subscribe(topic="garage/setTargetDoorState", qos=1)
client.loop_start()

#Sends real door status when it's known
while True:
    if GPIO.input(reedOpen) == 1 and status != "Closing":
        client.publish(topic="garage/getTargetDoorState", payload="open", qos=1, retain=True)
        client.publish(topic="garage/getCurrentDoorState", payload="Open" ,qos=1, retain=True)
        status = last = "Closing"
    
    elif GPIO.input(reedClosed) == 1 and status != "Opening":
        client.publish(topic="garage/getTargetDoorState", payload="close", qos=1, retain=True)
        client.publish(topic="garage/getCurrentDoorState", payload="Closed", qos=1, retain=True)
        status = last = "Opening"
        
    elif GPIO.input(reedOpen) == 0 and GPIO.input(reedClosed) == 0 and status != "unknown":
        client.publish(topic="garage/getCurrentDoorState", payload=last, qos=1, retain=True)
        if last == "Closing":
            client.publish(topic="garage/getTargetDoorState", payload="close", qos=1, retain=True)
        elif last == "Opening":
            client.publish(topic="garage/getTargetDoorState", payload="open", qos=1, retain=True)
        status = "unknown"
    time.sleep(0.1)

#GG von Tobias und Teymen