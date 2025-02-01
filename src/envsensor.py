#!/usr/bin/env python3

import os
import socket
import json
import uuid
from MqttPublisher import MqttPublisher
from pathlib import Path

with open( os.path.join(Path(__file__).resolve().parent, "launch_settings", "env.json"), 'r') as file:
    environment = json.load(file)

IS_MOCKED = environment["is_mocked"]
MQTT_HOST = environment["mqtt_host"]
MQTT_PORT = int(environment["mqtt_port"])
MQTT_USER = environment["mqtt_user"]
MQTT_PASSWORD = environment["mqtt_password"]
MQTT_TOPIC = socket.gethostname().lower() + "/environmentsensor"
MQTT_TLS = environment["mqtt_tls"]
SENSOR_ADDRESS = int(environment["sensor_address"], 16)

if IS_MOCKED == "True":
    print("Starting mock")
    from Bme280Mock import Bme280Mock
else:
    print("Starting real sensor")
    from Bme280Wrapper import Bme280Wrapper

def main():

    observer = Observer()
    try:
        if IS_MOCKED == "True":
            sensor = Bme280Mock(SENSOR_ADDRESS)
        else:
            sensor = Bme280Wrapper(SENSOR_ADDRESS)

        sensor.attach(observer)
        sensor.start_driver()
    except KeyboardInterrupt:
        print('Program stopped')
        sensor.detach(observer)
        sensor.stop_driver()
        observer.dispose()

class Observer:

    def __init__(self):
        client_id = socket.gethostname() + "-"  + str(uuid.uuid4())
        self._publisher = MqttPublisher(MQTT_HOST, MQTT_PORT, MQTT_TOPIC, MQTT_TLS )
        self._publisher.connect(client_id, MQTT_USER, MQTT_PASSWORD)

    def update(self, data: dict):
        json_string = json.dumps(data, indent=4)
        self._publisher.publish( json_string ) 

    def dispose(self):
        self._publisher.disconnect()       

if __name__ == "__main__":
    main()