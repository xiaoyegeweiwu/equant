import numpy as np

class StatisticsModel(object):
    '''即时行情数据模型'''
    def __init__(self, strategy, config):
        '''
        '''
        self._strategy = strategy
        self.logger = strategy.logger
        self._config = config

    def SMA(self, price:np.array, period, weight):
        sma = 0.0

        if period <= 0:
            return -1, np.nan

        if weight > period or weight <= 0:
            return -2, np.nan

        for i, p in enumerate(price):
            if i == 0:
                sma = p
            else:
                sma = (sma*(period-weight)+p*weight)/period

        return 0, sma
