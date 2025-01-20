package main

import (
	"EnvironmentSensor/communication"
	"EnvironmentSensor/sensor"
	"fmt"
	"strings"
)

var mqttHandler communication.MqttHandler

func main() {

	var builder strings.Builder
	builder.WriteString("Welcome to ")
	builder.WriteString(AppName)
	builder.WriteString(" ")
	builder.WriteString(AppVersion)
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

	// start sensor
	fmt.Println("Starting the sensor...")
	bme := sensor.SensorMock{}
	bme.Subscribe(Callback)

	bme.Start()
}

func Callback(data sensor.SensorData) {
	mqttHandler.Publish(data.JsonString())
}
