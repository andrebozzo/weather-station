from forecaster import ZambrettiForecaster
from forecaster import Rilevazione
from datetime import datetime
import math

f = ZambrettiForecaster()
p = 990
for i in range(7):
    for j in range(24):
        for k in range(4):
            r = Rilevazione(10, p+0.01, 50, datetime(2020, 1, i+1, j, k*15, 0, 0))
            p = p +0.01
            f.addData(r)
f.forecast()