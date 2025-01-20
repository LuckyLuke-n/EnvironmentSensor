package communication

import (
	"errors"
	"fmt"
	"os"
	"strconv"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"github.com/google/uuid"
)

var messagePubHandler mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
	fmt.Printf("Received message: %s from topic: %s\n", msg.Payload(), msg.Topic())
}

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
	fmt.Println("Connected")
}

var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
	fmt.Printf("Connect lost: %v", err)
}

var machineName string = ""

type MqttConfig struct {
	Host     string
	Port     int
	Username string
	Password string
	UseTls   bool
}

func LoadConfigFromEnv() MqttConfig {
	var host = os.Getenv("ENVSENSOR_MQTT_HOST")
	var username = os.Getenv("ENVSENSOR_MQTT_USERNAME")
	var password = os.Getenv("ENVSENSOR_MQTT_PASSWORD")

	port, err := strconv.Atoi(os.Getenv("ENVSENSOR_MQTT_PORT"))
	if err != nil {
		fmt.Println("Error parsing string to int:", err)
	}

	useTls, err := strconv.ParseBool(os.Getenv("ENVSENSOR_MQTT_USETLS"))
	if err != nil {
		fmt.Println("Error parsing string to bool:", err)
	}

	return MqttConfig{host, port, username, password, useTls}
}

type MqttHandler struct {
	Host     string
	Port     int
	Username string
	Password string
	Topic    string
	UseTls   bool
	Client   mqtt.Client
}

func NewClient(host string, port int, username string, password string, useTls bool) (*MqttHandler, error) {
	if host == "" || username == "" || password == "" {
		return nil, errors.New("host, username and password cannot be empty")
	}

	machineName, err := os.Hostname()

	if err != nil {
		fmt.Println("Error:", err)
	}

	return &MqttHandler{Host: host, Port: port, Username: username, Password: password, Topic: machineName + "/temperaturesensor", UseTls: useTls}, nil
}

func (c *MqttHandler) connect() {
	opts := mqtt.NewClientOptions()
	opts.AddBroker("tcp://" + c.Host + ":" + strconv.Itoa(c.Port))
	opts.SetClientID(machineName + uuid.New().String())
	opts.SetUsername(c.Username)
	opts.SetPassword(c.Password)
	// opts.SetDefaultPublishHandler(messagePubHandler)
	opts.OnConnect = connectHandler
	opts.OnConnectionLost = connectLostHandler
	c.Client = mqtt.NewClient(opts)
	if token := c.Client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
}

func (c *MqttHandler) Publish(payload string) {
	c.Client.Publish(c.Topic, 0, false, payload)
}
