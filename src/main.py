import Bme280Wrapper as bme280_wrapper;

def main():
    sensor = bme280_wrapper.Bme280Wrapper(0x77)
    sensor.start_driver()

if __name__ == "__main__":
    main()