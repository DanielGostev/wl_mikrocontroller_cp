import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import time
import board
import busio
import digitalio
import adafruit_max31865
import json

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to %s" % secrets["ssid"])

wifi.radio.connect(secrets["ssid"], secrets["password"])

print("Connected to %s!" % secrets["ssid"])

### Topic Setup ###

# MQTT Topic
mqtt_topic = "control/pico"
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
GPIO16 = digitalio.DigitalInOut(board.GP16)
GPIO16.direction = digitalio.Direction.OUTPUT
GPIO14 = digitalio.DigitalInOut(board.GP14)
GPIO14.direction = digitalio.Direction.OUTPUT
GPIO15 = digitalio.DigitalInOut(board.GP15)
GPIO15.direction = digitalio.Direction.OUTPUT


### Code ###

def connect(mqtt_client, userdata, flags, rc):
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))


def disconnect(mqtt_client, userdata, rc):
    print("Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(mqtt_client, userdata, topic, pid):
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def publish(mqtt_client, userdata, topic, pid):
    print("Published to {0} with PID {1}".format(topic, pid))


def message(client, topic, message):
    print("New message on topic {0}: {1}".format(topic, message))

def sub_cb(client, topic, message):
    payload = json.loads(message)
    print("Message received: " + payload["Heater"] + payload["Fan"]) 
    if payload["Heater"] == "on":
        GPIO16.value = True
        GPIO15.value = True
    elif payload["Heater"] == "off":
        GPIO16.value = False
        GPIO15.value = False
    if payload["Fan"] == "on":
        GPIO14.value = True
    elif payload["Fan"] == "off":
        GPIO14.value = False


# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=secrets["broker"],
    port=secrets["port"],   
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

# Connect callback handlers to mqtt_client
mqtt_client.on_connect = connect
mqtt_client.on_disconnect = disconnect
mqtt_client.on_subscribe = subscribe
mqtt_client.on_unsubscribe = unsubscribe
mqtt_client.on_publish = publish
#mqtt_client.on_message = message
mqtt_client.on_message = sub_cb

# Connect the client to the MQTT broker.
print("Attempting to connect to %s" % mqtt_client.broker)
mqtt_client.connect()

mqtt_client.subscribe(mqtt_topic,1)
led.value = True
while True:
    mqtt_client.loop()
    time.sleep(2)
