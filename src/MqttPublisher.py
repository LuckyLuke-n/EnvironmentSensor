from paho.mqtt import client as mqtt_client

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

class MqttPublisher:

    def __init__(self, host: str, port: int, topic: str, use_tls: bool ):
        self.broker = host
        self.port = port
        self.topic = topic
        self.use_tls = use_tls
        self._graceful_disconnect = False
    
    def connect(self, client_id: str, username: str, password: str):
        self.client_id = client_id

        self.unacked_publish = set()

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc) + "\n" )

        # Set Connecting Client ID
        # For paho-mqtt 2.0.0, you need to set callback_api_version.
        self.client = mqtt_client.Client()
        self.client.user_data_set(self.unacked_publish)
        self.client.username_pw_set(username, password)

        if self.use_tls:
            self.client.tls_set()
            
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)

        self.client.loop_start()
    
    def publish(self, payload: str):
        result = self.client.publish(self.topic, payload)
        self.unacked_publish.add(result.mid)
        status = result[0] # result: [0, 1]
        if status == 1:
            print(f"Failed to send message to topic {self.topic}")
        elif status == 4:
            print(f"No connection to broker to publish to topic {self.topic}. Check credentials.")

    def disconnect(self):
        self._graceful_disconnect = True
        self.client.loop_stop()
        self.client.disconnect()