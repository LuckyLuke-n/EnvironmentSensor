import time
import socket
# import fcntl
import smbus2
import bme280
from datetime import datetime

class Bme280Wrapper:

    def __init__(self, sensor_address: int, location_tag: str):
        self.sensor_address = sensor_address
        self._stopping_token_thrown = False
        self._observers = []
        self.location_tag = location_tag
    
    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def start_driver(self):
        """
        Calibrates sensor and starts reading until exception occurs or keyboard interrupt happens
        """
        bus = smbus2.SMBus(1)
        # Load calibration parameters
        calibration_params = bme280.load_calibration_params(bus, self.sensor_address)

        while not self._stopping_token_thrown:
            try:
                # Read sensor data
                data = bme280.sample(bus, self.sensor_address, calibration_params)

                # Extract temperature, pressure, and humidity
                temperature_celsius = data.temperature
                pressure = data.pressure
                humidity = data.humidity

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
                        "hostname": socket.gethostname().lower(),
                        "location": self.location_tag,
                        "sensor": "bme280"
                    }
                    observer.update(data)

                # Wait for a few seconds before the next reading
                time.sleep(30)

            except Exception as e:
                print('An unexpected error occurred:', str(e))
                break

    def stop_driver(self):
        """
        Stops the driver. Data from the sensor is no longer processed.
        """
        self._stopping_token_thrown = True