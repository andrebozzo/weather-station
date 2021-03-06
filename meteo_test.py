import smbus2
import bme280
from ds18b20_therm import DS18B20
port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

# the compensated_reading class has the following attributes
'''print(data.id)
print(data.timestamp)
print(data.temperature)
print(data.pressure)
print(data.humidity)
'''
print("BME280 (temp, hum, press) -> ")
# there is a handy string representation too
print(data)

sonda_temp = DS18B20()
print("DS18B20 (sonda temp) ->")
print(sonda_temp.read_temp())