from paho.mqtt import client as mqtt_client
import SensorData
import time
from SensorData import SensorData

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

class MqttPublisher:

    def __init__(self, host: str, port: int, topic: str ):
        self.broker = host
        self.port = port
        self.topic = topic
        self._graceful_disconnect = False
    
    def connect(self, client_id: str, username: str, password: str):
        self.client_id = client_id

        # For paho-mqtt 2.0.0, you need to add the properties parameter.
        def on_connect(client, userdata, flags, rc, properties):
            if rc == 0:
                print("Connected to MQTT Broker!")
                self.is_connected = True
            else:
                print("Failed to connect, return code %d\n", rc)
                self.is_connected = False

        def on_disconnect(client, userdata, rc):

            if self._graceful_disconnect:
                return

            print("Disconnected with result code: %s", rc)
            reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
            while reconnect_count < MAX_RECONNECT_COUNT:
                print("Reconnecting in %d seconds...", reconnect_delay)
                time.sleep(reconnect_delay)

                try:
                    client.reconnect()
                    print("Reconnected successfully!")
                    return
                except Exception as err:
                    print("%s. Reconnect failed. Retrying...", err)

                reconnect_delay *= RECONNECT_RATE
                reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
                reconnect_count += 1
            print("Reconnect failed after %s attempts. Exiting...", reconnect_count)

        # Set Connecting Client ID
        self.client = mqtt_client.Client(client_id)
        # For paho-mqtt 2.0.0, you need to set callback_api_version.
        self.client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.connect(self.broker, self.port)
    
    def publish(self, payload: SensorData):
        result = self.client.publish(self.topic, payload)
        status = result[0] # result: [0, 1]
        if status == 1:
            print(f"Failed to send message to topic {self.topic}")

    def disconnect(self):
        self._graceful_disconnect = True
        self.client.disconnect()