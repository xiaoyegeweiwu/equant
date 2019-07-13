import numpy as np

class USMA:
    def __init__(self):
        self._sma = []

    def SMA(self, price, period, weight):
        '''增量计算'''
        xprice = price[-1] if not np.isnan(price[-1]) else 1.0
        if len(price) > 1:
            sma = (self._sma[-1] *(period-weight) + xprice * weight) / period
            self._sma.append(sma)
        else:
            self._sma.append(xprice)
        
        return np.array(self._sma)

