from pubnub import Pubnub
import RPi.GPIO as GPIO
import time

pubnub = Pubnub(publish_key="pub-c-0bed295e-a3e2-451a-882c-76cda83f73c9", subscribe_key="sub-c-3477209c-225a-11e7-894d-0619f8945a4f", ssl_on=False)
channel = "Smart Lamp"

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.output(27, 1)
GPIO.output(17, 1)

button_blink = True

def turnOnLights():
    GPIO.output(27, 0)
    GPIO.output(17, 0)

def turnOffLights():
    GPIO.output(27, 1)
    GPIO.output(17, 1)

def turnOnYellowLights():
    GPIO.output(27, 1)
    GPIO.output(17, 0)

def turnOnWhiteLights():
    GPIO.output(27, 0)
    GPIO.output(17, 1)

def blinkLights():
    GPIO.output(27, 0)
    GPIO.output(17, 0)
    time.sleep(0.5)
    GPIO.output(27, 0)
    GPIO.output(17, 1)
    time.sleep(0.5)
    GPIO.output(27, 1)
    GPIO.output(17, 0)
    time.sleep(0.5)
    GPIO.output(27, 1)
    GPIO.output(17, 1)
    time.sleep(0.5)

def callback(message, channel):
    command = message['command']

    print(command)

    if command == "On":
        turnOnLights()
    elif command == "Off":
        turnOffLights()
    elif command == "Yellow":
        turnOnYellowLights()
    elif command == "White":
        turnOnWhiteLights()
    elif command == "Blink":
        blinkLights()
            
def error(message):
    print("ERROR : " + str(message))

def connect(message):
    print("CONNECTED")

def reconnect(message):
    print("RECONNECTED")

def disconnect(message):
    print("DISCONNECTED")

pubnub.subscribe(channels=channel, callback=callback, error=error,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)

while True:
    button_on = GPIO.input(14)
    button_yellow = GPIO.input(15)
    button_white = GPIO.input(18)
    button_off = GPIO.input(24)

    if button_blink == True:
        button_blink = GPIO.input(23)

    if button_on == False:
        turnOnLights()
        button_blink = True
    
    if button_off == False:
        turnOffLights()
        button_blink = True

    if button_yellow == False:
        turnOnYellowLights()
        button_blink = True

    if button_white == False:
        turnOnWhiteLights()
        button_blink = True

    if button_blink == False:
        blinkLights()