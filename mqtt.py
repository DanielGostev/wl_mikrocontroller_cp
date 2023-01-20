import paho.mqtt.client as paho
import sensor_data
import time


class MqttControl:
    def __init__(self, address, port, sensor_logger):
        self.address = address  # "192.168.178.35"  # Broker address
        self.port = port  # 1883  # Broker port
        self.paho_client = paho.Client("Python")  # create new instance
        self._sensor_logger = sensor_logger

    def connect_broker(self):
        self.paho_client.on_connect = self.on_connect  # attach function to callback
        self.paho_client.on_message = self.on_message  # attach function to callback
        self.paho_client.connect(self.address, port=self.port)  # connect to broker
        self.paho_client.loop_start()  # start the loop

    def subscribe(self, topic):
        self.paho_client.subscribe(topic)
        print("Subscribed")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print("Connection failed")

    def on_message(self, client, userdata, message):
        print("Message received: " + message.payload.decode("utf-8"))
        self._sensor_logger.log_data(sensor_data.SensorData("pico_fb", message.payload.decode("utf-8"), time.time()))

