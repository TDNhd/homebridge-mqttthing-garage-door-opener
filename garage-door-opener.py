import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

relay = 17          #Optionally set this to desired pin
reedOpen = 5        #Optionally set this to desired pin
reedClosed = 12     #Optionally set this to desired pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(reedOpen, GPIO.IN)
GPIO.setup(reedClosed, GPIO.IN)
GPIO.setup(relay, GPIO.OUT)

broker = "<your Broker address>"
tls_port = 8883     #Port "8883" needed when running SSL/TLS encrypted connection (default TCP/IP port is 1883)
client = mqtt.Client(client_id="garage", clean_session=False)

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
client.on_message=on_message
client.tls_set(ca_certs="<CA certificate location path>", certfile="<Client certificate location path>", keyfile="<Client key location path>")     #Only needed when running SSL/TLS encrypted connection
client.tls_insecure_set(True)       #Needed when certificate is self-signed
client.connect(host=broker, port=tls_port)
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