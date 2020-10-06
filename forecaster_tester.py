from forecaster import ZambrettiForecaster
from forecaster import Rilevazione
from datetime import datetime

f = ZambrettiForecaster()
for i in range(100):
    r = Rilevazione(10, 990+i, 50, datetime.now())
    f.addData(r)
f.forecast()