import smbus2
import bme280
import sys
import time
import requests
import datetime
from picamera import PiCamera
from time import sleep

camera = PiCamera()

url = "https://meteo-station.herokuapp.com/data"
interval = 120 #120 seconds (2 mins)
if len(sys.argv) > 1:
    interval = sys.argv[1]

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object


# the compensated_reading class has the following attributes
while True:
    try:
        data = bme280.sample(bus, address, calibration_params)
        # there is a handy string representation too
        print("Receiving data from bme280...")
        print(data)
        data_id = data.id
        ts = datetime.now()
        temp = round(data.temperature, 1)
        press = round(data.pressure, 4)
        hum = round(data.humidity, 2)
        data = { 
            "temp": temp,
            "press": press,
            "hum": hum,
            "timestamp": ts.strftime("%m-%d-%Y, %H:%M:%S")
        }
        response = requests.post(url, json = data)
        if response.status_code is 200:
            print("Data sent correctly")
        else:
            print("Server errror")
    except:
        print("error while retriving data from bme280")

    try:
        camera.start_preview()
        for i in range(5):
            sleep(5)
            camera.capture('/home/pi/Desktop/image%s.jpg' % i)
        camera.stop_preview()
    except:    
        print("error while sending the photo update")

    time.sleep(interval)
