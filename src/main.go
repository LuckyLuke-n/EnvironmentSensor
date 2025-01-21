package main

import (
	"EnvironmentSensor/communication"
	"EnvironmentSensor/sensor"
	"fmt"
	"strings"
)

var appName string = "Environment Sensor"
var appVersion string = "1.0.0"

var mqttHandler communication.MqttHandler

func main() {

	var builder strings.Builder
	builder.WriteString("Welcome to ")
	builder.WriteString(appName)
	builder.WriteString(" ")
	builder.WriteString(appVersion)
	builder.WriteString("\n")

	fmt.Println(builder.String())
	fmt.Println("Loading settings...")
	var mqttConfig = communication.LoadConfigFromEnv()

	fmt.Println("Connect to message bus...")
	var mqttClient, err = communication.NewClient(mqttConfig.Host, mqttConfig.Port, mqttConfig.Username, mqttConfig.Password, mqttConfig.UseTls)

	if err != nil {
		fmt.Println("cannot connect to message bus", err)
	}
	mqttHandler = *mqttClient
	mqttHandler.Connect(mqttConfig.UseTls)

	// start sensor
	fmt.Println("Starting the sensor...")
	bme := sensor.SensorMock{}
	bme.Subscribe(Callback)

	bme.Start()
}

func Callback(data sensor.SensorData) {
	mqttHandler.Publish(data.JsonString())
}
