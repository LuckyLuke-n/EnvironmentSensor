import time
import socket
import random
from datetime import datetime

class Bme280Mock:

    def __init__(self, sensor_address: int):
        self.sensor_address = sensor_address
        self._stopping_token_thrown = False
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def start_driver(self):
        """
        Calibrates sensor and starts reading until exception occurs or keyboard interrupt happens
        """

        while not self._stopping_token_thrown:
            try:
                # Extract temperature, pressure, and humidity
                temperature_celsius = random.uniform(15, 25)
                pressure = random.uniform(990, 1000)
                humidity = random.uniform(40, 60)

                # Print the readings
                # print("Temperature: {:.2f} °C".format(temperature_celsius))
                # print("Pressure: {:.2f} hPa".format(pressure))
                # print("Humidity: {:.2f} %".format(humidity))

                for observer in self._observers:
                    data = {
                        "timestamp": str(datetime.utcnow()),
                        "temperature": round(temperature_celsius, 2),
                        "pressure": round(pressure, 2),
                        "humidity": round(humidity, 2),
                        "hostname": socket.gethostname().lower()
                    }
                    observer.update(data)

                # Wait for a few seconds before the next reading
                time.sleep(5)

            except Exception as e:
                print('An unexpected error occurred:', str(e))
                break

    def stop_driver(self):
        """
        Stops the driver. Data from the sensor is no longer processed.
        """
        self._stopping_token_thrown = True