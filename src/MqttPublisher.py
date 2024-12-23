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

        self.unacked_publish = set()

        # For paho-mqtt 2.0.0, you need to add the properties parameter.
        def on_connect(client, userdata, flags, reason_code, properties):
            print("Connected")
            if reason_code.is_failure:
                print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
            else:
                # we should always subscribe from on_connect callback to be sure
                # our subscribed is persisted across reconnections.
                client.subscribe("$SYS/#")


        # Set Connecting Client ID
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
        # For paho-mqtt 2.0.0, you need to set callback_api_version.
        self.client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
        self.client.user_data_set(self.unacked_publish)
        self.client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)

        if self.client.is_connected():
            print("Conn")
        else:
            print("Fail")

        self.client.loop_start()
    
    def publish(self, payload: SensorData):
        result = self.client.publish(self.topic, payload)
        self.unacked_publish.add(result.mid)
        status = result[0] # result: [0, 1]
        if status == 1:
            print(f"Failed to send message to topic {self.topic}")
        elif status == 4:
            print(f"No connection to broker to publish to topic {self.topic}")

    def disconnect(self):
        self._graceful_disconnect = True
        self.client.disconnect()
        self.client.loop_stop()