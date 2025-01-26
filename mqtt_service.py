import time
import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

class MQTTClient:
    def __init__(self, mqtt_token, subscribe_topic):
        self.client = mqtt.Client()
        self.subscribers = []
        self.broker_address = "mqtt.beebotte.com"
        self.port = 1883


        # Set the username to 'token:CHANNEL_TOKEN' before calling connect
        # load_dotenv()
        # channel_token = os.getenv("MQTT_TOKEN")
        self.client.username_pw_set(mqtt_token)

        self.subscribe_topic = subscribe_topic

        # Set callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, data, flags, rc):
        """Called upon reception of CONNACK response from the server."""
        print("Connected with result code " + str(rc))
        client.subscribe(self.subscribe_topic, 1)

    def on_message(self, client, data, msg):
        """Called when a message is received from the broker."""
        print(f"Received message: {msg.payload}")
        try:
            command = json.loads(msg.payload)
            # print(f"Received command: {command}")

            # Notify all registered subscribers
            for notify_callback in self.subscribers:
                notify_callback(command)
            
        except json.JSONDecodeError:
            print("Invalid JSON received")

        except Exception as e:
            print(f"Error processing message: {e}")

    def start(self):
        """Connect to the MQTT broker and start the loop."""
        self.client.connect(self.broker_address, self.port, 60)
        self.client.loop_start()

    def subscribe(self, notify_callback):
        """Register a callback to be notified when a message is received."""
        self.subscribers.append(notify_callback)

    def publish(self, topic, data):
        # self.client.publish("mychannel/myresource", "Hello World", 1)
        self.client.publish(topic, data, 1)

if __name__ == "__main__":
    # Initialize the MQTT client with broker address, port, and username token
    mqtt_client = MQTTClient(broker_address="mqtt_broker_address", port=1883, username_token="token:token_xxx")

    # Example of subscribing to commands
    def handle_command(command):
        print(f"Handling command: {command}")

    mqtt_client.subscribe(handle_command)

    # Start the MQTT client
    mqtt_client.start()

    # Keep the script running
    while True:
        time.sleep(1)
