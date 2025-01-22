package sensor

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"

	"github.com/d2r2/bme280"
	"github.com/d2r2/go-i2c"
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

type Bme280Sensor struct {
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

func (p *Bme280Sensor) Subscribe(s Subscriber) {
	p.subscribers = append(p.subscribers, s)
}

func (p *Bme280Sensor) Notify(sensorData SensorData) {
	for _, subscriber := range p.subscribers {
		subscriber(sensorData)
	}
}

func (m *Bme280Sensor) Start() {

	sensorAddress, err := strconv.ParseInt(os.Getenv("ENVSENSOR_BME280_ADDRESS"), 0, 16)
	if err != nil {
		fmt.Println("Error parsing string to bool:", err)
	}

	// Create a new I2C connection
	i2c, err := i2c.NewI2C(bme280.Address, 1) // 1 is the I2C bus number
	if err != nil {
		log.Fatalf("Failed to create I2C connection: %v", err)
	}
	defer i2c.Close()

	// Create a new BME280 instance
	bme, err := bme280.New(i2c)
	if err != nil {
		log.Fatalf("Failed to create BME280 instance: %v", err)
	}

	// Read data from the sensor
	for {
		// Read temperature, pressure, and humidity
		temperature, pressure, humidity, err := bme.ReadAll()
		if err != nil {
			log.Printf("Failed to read from BME280: %v", err)
			time.Sleep(2 * time.Second)
			continue
		}

		// Print the results
		fmt.Printf("Temperature: %.2f °C\n", temperature)
		fmt.Printf("Pressure: %.2f hPa\n", pressure/100) // Convert Pa to hPa
		fmt.Printf("Humidity: %.2f %%\n", humidity)
		fmt.Println()

		// Wait for a while before the next reading
		time.Sleep(2 * time.Second)
	}

}
