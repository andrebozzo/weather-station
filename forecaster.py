import numpy as np
import pandas as pd
import statsmodels.api as sm

class Rilevazione:
    def __init__(self, temp, press, hum, timestamp):
        self.temp = temp
        self.press = press
        self.hum = hum
        self.timestamp = timestamp

class ZambrettiForecaster:
    
    def __init__(self, h=981):
        self.h = h
        self.data = []

    def addData(self, rilevazione):
        self.data.append(rilevazione)

    def forecast(self):
        print("starting forecast")
        P0 = self.data[-1].press*(1-(0.0065 * self.h)/(self.data[-1].temp + 0.0065 * self.h + 273.15))
        pressureValues = pd.DataFrame()
        for d in self.data:
            pressureValues["y"] = d.press
            pressureValues["ts"] = d.timestamp
        decomposition = sm.tsa.seasonal_decompose(pressureValues)
        fig1 = decomposition.plot()


    

