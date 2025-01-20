package mqttHandler

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"

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

type MqttHandler struct {
	Host     string
	Port     int
	Username string
	Password string
	Topic    string
	UseTls   bool
	Client   mqtt.Client
}

type SensorData struct {
	Temperature     float32
	Humidity        float32
	AmbientPressure float32
}

func NewClient(host string, port int, username string, password string, useTls bool) (*MqttHandler, error) {
	if host == "" || username == "" || password == "" {
		return nil, errors.New("Host, username and password cannot be empty")
	}

	machineName, err := os.Hostname()

	if err != nil {
		fmt.Println("Error:", err)
	}

	return &MqttHandler{Host: host, Port: port, Username: username, Password: password, Topic: machineName + "/temperaturesensor", UseTls: useTls}, nil
}

func (c *MqttHandler) connect() {
	opts := mqtt.NewClientOptions()
	opts.AddBroker("tcp://" + c.Host + ":" + string(c.Port))
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

func (c *MqttHandler) publish(data SensorData) {
	payload, err := json.Marshal(data)

	if err != nil {
		fmt.Println("Error:", err)
	}

	c.Client.Publish(c.Topic, 0, false, payload)
}
