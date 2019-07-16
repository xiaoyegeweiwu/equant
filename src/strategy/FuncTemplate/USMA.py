import numpy as np

class USMA:
    def __init__(self):
        self._sma = []

    def SMA(self, price, period, weight):
        '''增量计算'''
        xprice = price[-1] if not np.isnan(price[-1]) else 0.0
        if len(price) > 1:
            sma = (self._sma[-1] *(period-weight) + xprice * weight) / period
            self._sma.append(sma)
        else:
            self._sma.append(xprice)
        
        return np.array(self._sma)

class UEMA:
    def __init__(self):
        self._ema = []

    def EMA(self, price, period):
        '''增量计算'''
        xprice = price[-1] if not np.isnan(price[-1]) else 0.0
        sfactor = 2 / ( period + 1 )
        if len(price) > 1:
            ema = self._ema[-1] + sfactor * (xprice-self._ema[-1])
            self._ema.append(ema)
        else:
            self._ema.append(xprice)

        return np.array(self._ema)

class UMA:
    def __init__(self):
        self._ma = []

    def MA(self, price, period):
        '''保证每一个周期执行到'''
        isum = 0
        for i in range(len(price)-1, len(price)-period-1, -1):
            isum = isum + price[i]
            if i == 0: break
        ma = isum / period
        self._ma.append(ma)
        return np.array(self._ma)
