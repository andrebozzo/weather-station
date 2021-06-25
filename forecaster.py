import math
class Rilevazione:
    def __init__(self, temp, temp_sonda, press, hum, timestamp):
        self.temp = temp
        self.press = press
        self.hum = hum
        self.timestamp = timestamp
        self.temp_sonda = temp_sonda

class ZambrettiForecaster:
    
    def __init__(self, h=981, sample_interval_seconds=1800):
        self.sample_interval_seconds = sample_interval_seconds
        self.n_sample = 0
        self.n_sample_per_hour = math.floor(3600*1.0/self.sample_interval_seconds)
        self.h = h
        self.pressList = []
        self.timestampList = []
        self.tempList = []
        self.tempSondaList = []
        self.humList = []

    def addData(self, rilevazione):
        self.pressList.append(rilevazione.press)
        self.timestampList.append(rilevazione.timestamp)
        self.tempList.append(rilevazione.temp)
        self.humList.append(rilevazione.hum)
        self.n_sample += 1
        self.tempSondaList.append(rilevazione.temp_sonda)
        if self.n_sample > (3*self.n_sample_per_hour):#keep the trend of 3 hours
            self.pressList.pop(0)
            self.timestampList.pop(0)
            self.tempList.pop(0)
            self.tempSondaList.pop(0)
            self.humList.pop(0)

    def trendDetector(self):
        press_diff = self.pressList[-1] - self.pressList[0]
        if press_diff > 1.6:
            return 1
        elif press_diff < -1.6:
            return -1
        return 0

    def parseZ(self, z, pressure_trend):
        if pressure_trend == 1: #Rising pressure
            if z == 20:
                return "Settled Fine"
            if z == 21:
                return "Fine Weather"
            if z == 22:
                return "Becoming Fine"
            if z == 23:
                return "Fairly Fine, Improving"
            if z == 24:
                return "Fairly Fine, Possibly Showers Early"
            if z == 25:
                return "Showery Early, Improving"
            if z == 26:
                return "Changeable, Mending"
            if z == 27:
                return "Rather Unsettled, Clearing Later"
            if z == 28:
                return "Unsettled, Probably Improving"
            if z == 29:
                return "Unsettled, Short Fine Intervals"
            if z == 30:
                return "Very Unsettled, Finer at Times"
            if z == 31:
                return "Stormy, Possibly Improving"
            if z == 31:
                return "Stormy, Much Rain"
        if pressure_trend == 0:
            if z == 10:
                return "Settled Fine"
            if z == 11:
                return "Fine Weather"
            if z == 12:
                return "Fine, Possible Showers"
            if z == 13:
                return "Fairly Fine, Showers Likely"
            if z == 14:
                return "Showery, Bright Intervals"
            if z == 15:
                return "Changeable, Some Rain"
            if z == 16:
                return "Unsettled, Rain at Times"
            if z == 17:
                return "Rain at Frequent Intervals"
            if z == 18:
                return "Very Unsettled, Rain"
            if z == 19:
                return "Stormy, Much Rain"
        if pressure_trend == -1:
            if z == 1:
                return "Settled Fine"
            if z == 2:
                return "Fine Weather"
            if z == 3:
                return "Fine, Becoming Less Settled"
            if z == 4:
                return "Fairly Fine, Showery Later"
            if z == 5:
                return "Showery, Becoming More Unsettled"
            if z == 6:
                return "Unsettled, Rain Later"
            if z == 7:
                return "Rain at Times, Worse Later"
            if z == 8:
                return "Rain at Times, Becoming Very Unsettled"
            if z == 9:
                return "Very Unsettled, Rain"

    def forecast(self):
        print("Trying to forecast weather...")
        if self.n_sample < (3*self.n_sample_per_hour):
            print("Yet insufficient data to forecast!")
            return
        print(self.pressList[-1])
        P0 = self.pressList[-1]* math.pow((1-((0.0065 * self.h)/(self.tempList[-1] + 0.0065 * self.h + 273.15))), -5.257)
        pressure_trend = self.trendDetector()
        p = self.pressList[-1]
        z = 0
        if pressure_trend == 1:
            z = 185 - 0.16*p
        elif pressure_trend == -1:
            z = 127 - 0.12*p
        else:
            z = 144 - 0.13*p            
        #adjustment for wind skipped
        '''
        if(winddir = N)
            z = z + 1
        else:
            z = z - 2
        '''
        return self.parseZ(z, pressure_trend)
        
    

    
    

