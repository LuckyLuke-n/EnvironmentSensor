from Bme280Wrapper import Bme280Wrapper
import os
from SensorData import SensorData
from MqttPublisher import MqttPublisher
import socket

MQTT_HOST = os.environ["ES_MQTT_HOST"]
MQTT_PORT = 8883
MQTT_USER = os.environ["ES_MQTT_USER"]
MQTT_PASSWORD = os.environ["ES_MQTT_PASSWORD"]
MQTT_TOPIC = "environmentsensor/" + socket.gethostname()
SENSOR_ADDRESS = 0x77

def main():

    observer = Observer()
    try:
        sensor = Bme280Wrapper(SENSOR_ADDRESS)
        sensor.start_driver()
        sensor.attach(observer)
    except KeyboardInterrupt:
        print('Program stopped')
        sensor.detach(observer)
        sensor.stop_driver()
        observer.dispose()

class Observer:

    def __init__(self):
        self._publisher = MqttPublisher(MQTT_HOST, MQTT_PORT, MQTT_TOPIC )
        self._publisher.connect(MQTT_USER, MQTT_PASSWORD)

    def update(self, data: SensorData):
        self._publisher.publish( data )
        print(f"Observer received: {data.temperature}")      

    def dispose(self):
        self._publisher.disconnect()       

if __name__ == "__main__":
    main()