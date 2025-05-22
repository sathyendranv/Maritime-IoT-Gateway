import json
import time

import paho.mqtt.client as mqtt
import sys
import os
import queue

# Add the top-level directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class MqttPublisher:
    def __init__(self, logger, broker, port=1883, username=None, password=None, client_id="mqtt_client", keepalive=60, enable_lwt=False):
        self.logger = logger
        self.BROKER = broker
        self.PORT = port
        self.CLIENT_ID = client_id
        self.enable_lwt = enable_lwt
        self.client = mqtt.Client(client_id=self.CLIENT_ID)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.topics = []
        if username != "" and password != "":
            self.client.username_pw_set(username, password)
        self.client.connect(broker, port, keepalive)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info("Connected to MQTT Broker!")
        else:
            self.logger.error(f"Failed to connect, return code {rc}")
    def on_disconnect(self,client, userdata, rc):
        self.logger.error("Disconnected with result code " + str(rc))

    def publish(self, msg, topic):
        self.logger.info(f"Publishing message to topic {topic}: {msg}")
        if topic not in self.topics:
            self.topics.append(topic)
            self.client.will_set(topic, payload="connection lost", qos=1, retain=True)
        self.client.publish(topic, msg)

def start_mqtt_client(config, logger, write_q):
    mqtt_client = MqttPublisher(logger, config['host'], config['port'],config['username'] ,config['password'] ,config['client_id'], config['keepalive'])
    mqtt_client.client.loop_start()
    while True:
        try:
            # Get an item from the queue
            item = write_q.get(timeout=3)  # Wait for 3 seconds for an item
            logger.debug(f"Received item: {item.__dict__}")
            # if item.protocol == "mqtt":
            mqtt_client.publish(item.msg, item.topic)
            # logger.debug(f"Published data: {mqtt_client.item.msg}")
            write_q.task_done()
        except queue.Empty:
            print("No more items to process, worker is exiting.")
            time.sleep(1)
            continue