import time
import sys
import os

if sys.platform.startswith('linux') or sys.platform == 'darwin':
    import fcntl
else:
    print("fcntl is not available on this platform.")
    print("application will shut down.")
    os._exit(0)

import smbus2
import bme280

class Bme280Wrapper:

    def __init__(self, sensor_address: int):
        self.sensor_address = sensor_address
        return

    def start_driver(self ):
        """
        Calibrates sensor and starts reading until exception occurs or keyboard interrupt happens
        """
        bus = smbus2.SMBus(1)

        # Load calibration parameters
        calibration_params = bme280.load_calibration_params(bus, self.sensor_address)

        while True:
            try:
                # Read sensor data
                data = bme280.sample(bus, self.sensor_address, calibration_params)

                # Extract temperature, pressure, and humidity
                temperature_celsius = data.temperature
                pressure = data.pressure
                humidity = data.humidity

                # Print the readings
                print("Temperature: {:.2f} °C".format(temperature_celsius))
                print("Pressure: {:.2f} hPa".format(pressure))
                print("Humidity: {:.2f} %".format(humidity))

                # Wait for a few seconds before the next reading
                time.sleep(2)

            except KeyboardInterrupt:
                print('Program stopped')
                break
            except Exception as e:
                print('An unexpected error occurred:', str(e))
                break