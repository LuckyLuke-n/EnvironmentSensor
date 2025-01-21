package sensor

import (
	"encoding/json"
	"fmt"
	"math"
	"os"
	"os/signal"
	"syscall"
	"time"
)

type SensorData struct {
	Temperature     float32 `json:"temperature"`
	Humidity        float32 `json:"humidity"`
	AmbientPressure float32 `json:"pressure"`
}

func NewSensorData(temperature float32, humidity float32, ambientPressure float32) *SensorData {
	return &SensorData{temperature, humidity, ambientPressure}
}

func (s *SensorData) JsonString() string {

	jsonString, err := json.Marshal(s)

	if err != nil {
		fmt.Println("Error:", err)
	}

	return string(jsonString)
}

type Subscriber func(SensorData)

func roundToTwoDecimalPlaces(value float32) float32 {
	return float32(math.Round(float64(value*100)) / 100)
}

type Sensor interface {
	Start()
}

type SensorMock struct {
	subscribers []Subscriber
}

func (p *SensorMock) Subscribe(s Subscriber) {
	p.subscribers = append(p.subscribers, s)
}

func (p *SensorMock) Notify(sensorData SensorData) {
	for _, subscriber := range p.subscribers {
		subscriber(sensorData)
	}
}

func (m *SensorMock) Start() {
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	// Create a channel to indicate when to stop the loop
	done := make(chan bool, 1)

	// Start a goroutine to handle the signal
	go func() {
		<-sigs // Wait for a signal
		fmt.Println("\nReceived interrupt signal, stopping...")
		done <- true // Send a signal to stop the loop
	}()

	// Infinite loop
	for {
		select {
		case <-done:
			fmt.Println("Sensor Mock stopped.")
			return
		default:
			data := SensorData{}
			data.Temperature = roundToTwoDecimalPlaces(21.4661)
			data.Humidity = roundToTwoDecimalPlaces(44)
			data.AmbientPressure = roundToTwoDecimalPlaces(980.411)

			m.Notify(data)

			time.Sleep(5 * time.Second)
		}
	}
}
