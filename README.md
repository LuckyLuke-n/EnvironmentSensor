# Environment Sensor: BME280 Sensor Data Reader
This Python script reads temperature and humidity data from a BME280 sensor. The BME280 is a versatile sensor that can measure temperature, humidity, and pressure, making it ideal for various environmental monitoring applications.

## Features
- Reads temperature and humidity data from the BME280 sensor.
- Pushes the data to a message bus.

## Requirements
- Python 3.x
- smbus2 library for I2C communication
- RPi.bme280 library for interfacing with the BME280 sensor

## License
This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for details.

## Installation
#### Connect the sensor
The pin layout is described [here](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/2).
Images are at the bottom of the readme.

#### Install raspi-config and i2detect
```
sudo apt update
sudo apt install raspi-config
sudo apt install i2c-tools
```

Run raspi-config and configure the i2c according to [that tutorial](https://randomnerdtutorials.com/raspberry-pi-bme280-data-logger/)
```
sudo raspi-config
```
- The following menu will open. Select Interface Options.
- Then, select the I2C option.
- Finally, enable I2C by selecting Yes.
- Reboot

Check the sensor
```
sudo i2cdetect -y 1
```
and see something like that
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- 77
```

#### Set environment for script
That is the number you will put in the launch_settings/env.json for sensor address. In that case it is 0x77.
```
{
    "is_mocked": "False",
    "mqtt_host": "host",
    "mqtt_port": "1883",
    "mqtt_user": "user",
    "mqtt_password": "secret",
    "sensor_address": "0x77"
}
```

#### Startup
Create file /etc/systemd/system/tempsensor.service
```
[Unit]
Description=Temperature Sensor Service
After=network.target

[Service]
Type=simple
User=usr
WorkingDirectory=/home/usr/Sources/Tempsensor
ExecStart=/bin/bash -c 'source tempsensorenv/bin/activate && python3 src/envsensor.py'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
Then run
```
sudo systemctl daemon-reload
sudo systemctl enable tempsensor.service
sudo systemctl start tempsensor.service
```

## Acknowledgments
Thanks to the developers of the BME280 sensor for providing accurate environmental data.
Special thanks to the open-source community for their contributions and support.
