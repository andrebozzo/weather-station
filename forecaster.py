import math
import numpy as np
import pandas as pd
import statsmodels.tsa.seasonal as seasonal

class Rilevazione:
    def __init__(self, temp, press, hum, timestamp):
        self.temp = temp
        self.press = press
        self.hum = hum
        self.timestamp = timestamp

class ZambrettiForecaster:
    
    def __init__(self, h=981):
        self.h = h
        self.pressList = []
        self.timestampList = []
        self.tempList = []
        self.humList = []

    def addData(self, rilevazione):
        self.pressList.append(rilevazione.press)
        self.timestampList.append(rilevazione.timestamp)
        self.tempList.append(rilevazione.temp)
        self.humList.append(rilevazione.hum)
        if len(self.pressList) > (96*2):
            self.pressList.pop(0)
            self.timestampList.pop(0)
            self.tempList.pop(0)
            self.humList.pop(0)

    def trendDetector(self, index, data, order=1):
        result = np.polyfit(index, list(data), order)
        slope = result[-2]
        return float(slope)

    def forecast(self):
        print("starting forecast")
        print(self.pressList[-1])
        P0 = self.pressList[-1]* math.pow((1-((0.0065 * self.h)/(self.tempList[-1] + 0.0065 * self.h + 273.15))), -5.257)
        index = range(len(self.pressList))
        pressureTrend = self.trendDetector(index, self.pressList)
        z = 0
        if pressureTrend > 1:
            z = 130 - P0 / 81
        elif pressureTrend >= -1 and pressureTrend <= 1:
            z = 147 - (5*P0)/376
        else:
            z = 179 - (2*P0)/129
            
        #adjustment for wind skipped
        '''
        if(winddir = N)
            z = z + 1
        else:
            z = z - 2
        '''
        print(z)
    

    
    

