import time
from datetime import datetime
from SensorData import SensorData

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
                temperature_celsius = 22.5
                pressure = 1000
                humidity = 44.14

                # Print the readings
                print("Temperature: {:.2f} °C".format(temperature_celsius))
                print("Pressure: {:.2f} hPa".format(pressure))
                print("Humidity: {:.2f} %".format(humidity))

                for observer in self._observers:
                    observer.update(SensorData( datetime.now(), temperature_celsius, pressure, humidity ))

                # Wait for a few seconds before the next reading
                time.sleep(2)

            except Exception as e:
                print('An unexpected error occurred:', str(e))
                break

    def stop_driver(self):
        """
        Stops the driver. Data from the sensor is no longer processed.
        """
        self._stopping_token_thrown = True