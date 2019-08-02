import numpy as np

class StatisticsModel(object):
    '''金融及统计数据模型'''
    def __init__(self, strategy, config):
        '''
        '''
        self._strategy = strategy
        self.logger = strategy.logger
        self._config = config
            

    def SMA(self, price:np.array, period, weight):
        sma = 0.0
        smas = []

        if period <= 0:
            return np.array(smas)

        if weight > period or weight <= 0:
            return np.array(smas)

        for i, p in enumerate(price):
            if np.isnan(p):
                p = 0.0
            if i == 0:
                sma = p
            else:
                sma = (sma*(period-weight)+p*weight)/period

            smas.append(sma)

        return np.array(smas)
        
    def ParabolicSAR(self, High:np.array, Low:np.array, AfStep, AfLimit):
    
        #输出参数
        roParClose,roParOpen,roPosition,roTransition = [], [], [], []
        #中间参数
        oParClose, oTransition = 0, 0
        HHValue, LLValue, PHHValue,  PLLValue= 0, 0, 0, 0
        Af, ParOpen, Position = 0, 0, 0
        
        
        for i in range(len(High)):
            if i == 0:
                Position = 1
                oTransition = 1
                
                Af = AfStep
                
                HHValue  = High[i]
                LLValue  = Low[i]
         
                oParClose = LLValue
                
                ParOpen = oParClose + Af * ( HHValue - oParClose)
                
                if ParOpen > Low[i]:
                    ParOpen = Low[i]
                
            else:
                oTransition = 0

                PHHValue = HHValue
                PLLValue = LLValue
                
                if High[i] > HHValue:
                    HHValue = High[i] 
                if Low[i] < LLValue:
                    LLValue = Low[i]
                    
                if Position == 1:
                    if Low[i] <= ParOpen:
                        Position = -1
                        oTransition = -1
                        oParClose = HHValue
                        
                        PHHValue = HHValue
                        PLLValue = LLValue
                
                        HHValue = High[i]
                        LLValue = Low[i]
                        
                        Af = AfStep
                        ParOpen = oParClose + Af * ( LLValue - oParClose)
                        if ParOpen < High[i]:
                            ParOpen = High[i]
                        if ParOpen < High[i-1]:
                            ParOpen = High[i-1]
                    else:
                        oParClose = ParOpen
                        
                        if HHValue > PHHValue and Af < AfLimit:
                            if Af + AfStep > AfLimit:
                                Af = AfLimit
                            else:
                                Af = Af + AfStep
                                
                        ParOpen = oParClose + Af * ( HHValue - oParClose)
                        if ParOpen > Low[i]:
                            ParOpen = Low[i]
                        if ParOpen > Low[i-1]:
                            ParOpen = Low[i-1]
                        
                else:
                    if High[i] >= ParOpen:
                        Position = 1
                        oTransition = 1
                        oParClose = LLValue

                        PHHValue = HHValue
                        PLLValue = LLValue
                        HHValue  = High[i]
                        LLValue  = Low[i]
                        
                        Af = AfStep
                        ParOpen = oParClose + Af * ( HHValue - oParClose)
                        if ParOpen > Low[i]:
                            ParOpen = Low[i]
                        if ParOpen > Low[i-1]:
                            ParOpen = Low[i-1]
                    else:
                        oParClose = ParOpen
                        
                        if LLValue < PLLValue and Af < AfLimit:
                            if Af+ AfStep > AfLimit:
                                Af = AfLimit
                            else:
                                Af = Af + AfStep

                        ParOpen = oParClose + Af * ( LLValue - oParClose)
                        if ParOpen < High[i]:
                            ParOpen = High[i]
                        if ParOpen < High[i-1]:
                            ParOpen = High[i-1]
            
            roParOpen.append(ParOpen)
            roPosition.append(Position)
            roParClose.append(oParClose)
            roTransition.append(oTransition)
            
        return roParClose, roParOpen, roPosition, roTransition

    def ParabolicSAR2(self, high:np.array, low:np.array, afstep, aflimit):
        oParClose = None
        oParOpen = None
        oPosition = None
        oTransition = None

        opc_s = []
        opo_s = []
        opos_s = []
        otran_s = []

        hlen = len(high)
        llen = len(low)

        if hlen <=0 or llen <= 0:
            return np.array(opc_s), np.array(opo_s), np.array(opos_s), np.array(otran_s)

        arr = high if hlen < llen else low

        Af = 0
        ParOpen = 0
        Position = 0
        HHValue = 0
        LLValue = 0
        pHHValue = 0
        pLLValue = 0

        for i, a in enumerate(arr):
            if i == 0:
                Position = 1
                oTransition = 1
                Af = afstep
                HHValue = high[i]
                LLValue = low[i]
                oParClose = LLValue
                ParOpen = oParClose + Af * (HHValue - oParClose)
                if ParOpen > LLValue:
                    ParOpen = LLValue
            else:
                oTransition = 0

                pHHValue = HHValue
                pLLValue = LLValue
                HHValue = HHValue if HHValue > high[i] else high[i]
                LLValue = LLValue if LLValue < low[i] else low[i]

                if Position == 1:
                    if low[i] <= ParOpen:
                        Position = -1
                        oTransition = -1
                        oParClose = HHValue
                        pHHValue = HHValue
                        pLLValue = LLValue
                        HHValue = high[i]
                        LLValue = low[i]

                        Af = afstep
                        ParOpen = oParClose + Af * (LLValue - oParClose)

                        if ParOpen < high[i]:
                            ParOpen = high[i]

                        if ParOpen < high[i-1]:
                            ParOpen = high[i-1]

                    else:
                        oParClose = ParOpen
                        if HHValue > pHHValue and Af < aflimit:
                            if Af + afstep > aflimit:
                                Af = aflimit
                            else:
                                Af = Af + afstep

                        ParOpen = oParClose + Af * (HHValue - oParClose)

                        if ParOpen > low[i]:
                            ParOpen = low[i]

                        if ParOpen > low[i-1]:
                            ParOpen = low[i-1]

                else:
                    if high[i] >= ParOpen:
                        Position = 1
                        oTransition = 1

                        oParClose = LLValue
                        pHHValue = HHValue
                        pLLValue = LLValue
                        HHValue = high[i]
                        LLValue = low[i]

                        Af = afstep
                        ParOpen = oParClose + Af * (HHValue - oParClose)

                        if ParOpen > low[i]:
                            ParOpen = low[i]

                        if ParOpen > low[i-1]:
                            ParOpen = low[i-1]

                    else:
                        oParClose = ParOpen

                        if LLValue < pLLValue and Af < aflimit:
                            if Af + afstep > aflimit:
                                Af = aflimit
                            else:
                                Af = Af + afstep

                        ParOpen = oParClose + Af * (LLValue - oParClose)

                        if ParOpen < high[i]:
                            ParOpen = high[i]

                        if ParOpen < high[i-1]:
                            ParOpen = high[i-1]


            oParOpen = ParOpen
            oPosition = Position

            opc_s.append(oParClose)
            opo_s.append(oParOpen)
            opos_s.append(oPosition)
            otran_s.append(oTransition)

        return np.array(opc_s), np.array(opo_s), np.array(opos_s), np.array(otran_s)



