import json
import time

import paho.mqtt.client as mqtt
import sys
import os

# Add the top-level directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class MqttPublisher:
    def __init__(self, broker='localhost', port=1883, topic='maritime/iot/data', client_id='maritime-iot-gateway-001'):
        self.BROKER = broker
        self.PORT = port
        self.TOPIC = topic
        self.CLIENT_ID = client_id
        self.payload = {
            "temperature": 22.5,
            "humidity": 60
        }
        self.client = mqtt.Client(client_id=self.CLIENT_ID)
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.publish(self.TOPIC, json.dumps(self.payload))
            print(f"Published data to topic {self.TOPIC}")
        else:
            print(f"Failed to connect, return code {rc}")

    def publish(self):
        self.client.connect(self.BROKER, self.PORT, 5)
        self.client.loop_start()
        time.sleep(2)
        self.client.loop_stop()
        self.client.disconnect()

def main():
    publisher = MqttPublisher()
    publisher.publish()

if __name__ == "__main__":
    main()