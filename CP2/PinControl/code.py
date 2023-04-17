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
# Use this topic if you'd like to connect to a standard MQTT broker
mqtt_topic = "control/pico"
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led1 = digitalio.DigitalInOut(board.GP16)
led1.direction = digitalio.Direction.OUTPUT
led2 = digitalio.DigitalInOut(board.GP14)
led2.direction = digitalio.Direction.OUTPUT
led3 = digitalio.DigitalInOut(board.GP15)
led3.direction = digitalio.Direction.OUTPUT


### Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connect(mqtt_client, userdata, flags, rc):
    # This function will be called when the mqtt_client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))


def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def publish(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client publishes data to a feed.
    print("Published to {0} with PID {1}".format(topic, pid))


def message(client, topic, message):
    # Method called when a client's subscribed feed has a new value.
    print("New message on topic {0}: {1}".format(topic, message))

def sub_cb(client, topic, message):
    payload = json.loads(message)
    print("Message received: " + payload["Heater"] + payload["Fan"]) 
    if payload["Heater"] == "on":
        led1.value = True
        led3.value = True
    elif payload["Heater"] == "off":
        led1.value = False
        led3.value = False
    if payload["Fan"] == "on":
        led2.value = True
    elif payload["Fan"] == "off":
        led2.value = False


# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=secrets["broker"],
    port=secrets["port"],   
    #username=secrets["aio_username"],
    #password=secrets["aio_key"],
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

#print("Publishing to %s" % mqtt_topic)
#mqtt_client.publish(mqtt_topic, "Hello Broker!")

#print("Unsubscribing from %s" % mqtt_topic)
#mqtt_client.unsubscribe(mqtt_topic)

#print("Disconnecting from %s" % mqtt_client.broker)
#mqtt_client.disconnect()

#    print("Subscribing to %s" % mqtt_topic)
mqtt_client.subscribe(mqtt_topic,1)
led.value = True
while True:
    mqtt_client.loop()
    time.sleep(2)
