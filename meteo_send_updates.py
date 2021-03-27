import smbus2
import bme280
import sys
import time
import requests
from ds18b20_therm import DS18B20
from datetime import datetime
from picamera import PiCamera
from time import sleep
from forecaster import ZambrettiForecaster
from forecaster import Rilevazione

url_data = "https://meteo-station.herokuapp.com/data"
url_photo = "https://meteo-station.herokuapp.com/photo"

#url_data = "http://192.168.1.80:8080/data"
#url_photo = "http://192.168.1.80:8080/photo"

interval = 1800 #1800 seconds (30 mins)
if len(sys.argv) > 1:
    interval =int(sys.argv[1])
print("Updates will be sent every %d seconds, every %.2f minutes" % (interval, interval/60))
port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
temp_sonda = DS18B20()
camera = PiCamera(resolution=(1080, 920))
forecasterZ = ZambrettiForecaster(interval=interval)
# the compensated_reading class has the following attributes
while True:

    print("Receiving data from bme280...")
    data = bme280.sample(bus, address, calibration_params)
    # there is a handy string representation too
    data_id = data.id
    ts = datetime.now()
    temp = round(data.temperature, 1)
    press = round(data.pressure, 4)
    hum = round(data.humidity, 2)
    print("Receiving data from ds18b20...")
    temp_s = temp_sonda.read_temp()
    
    r = Rilevazione(temp, temp_s, press, hum, ts.strftime("%m-%d-%Y, %H:%M:%S"))
    forecasterZ.addData(r)
    forecas = forecasterZ.forecast()
    # packing everything

    data = { 
        "temp": temp,
        "temp_s": temp_s,
        "press": press,
        "hum": hum,
        "timestamp": ts.strftime("%m-%d-%Y, %H:%M:%S"),
        "forecast": forecas
    }
    
    response = requests.post(url_data+"?write_key=ciccione88", json = data)
    if response.status_code is 200:
        print("Data sent correctly")
    else:
        print("Error in sending data update")
        print(response.status_code)
        print(response.text)
    #except:
     #   print("error while retriving data from bme280")

    try:
        photo_path = '/home/pi/Desktop/snapshot.jpg'
        camera.awb_mode = "sunlight"
        camera.start_preview()
        sleep(5)
        camera.capture(photo_path)
        camera.stop_preview()
        files = {'photo': open(photo_path, 'rb')}
        response = requests.post(url_photo+"?write_key=ciccione88", files = files)
        if response.status_code is 200:
            print("Photo sent correctly to meteo-server")
        else:
            print("Photo sending error:")
            print(response.status_code)
            print(response.text)
    except:   
        print("error while sending the photo update")

    time.sleep(interval)
