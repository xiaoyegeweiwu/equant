class NumericSeries(list):
    def __init__(self, rawList=[], isOpenLog=True):
        super().__init__(rawList)
        self._curBarIndex = -1
        self._isOpenLog = isOpenLog

    def __setitem__(self, key, value):
        length = super().__len__()
        curBarIndex = CurrentBar()

        if length == 0:
            super().append(value)
            self._curBarIndex = curBarIndex
        elif 0<=key<length-1 or -length<=key<-1:
            super().__setitem__(key, value)
        elif key==-1 or key==length-1:
            if self._curBarIndex == curBarIndex:  # curBarIndex是一样的
                super().__setitem__(key, value)
            elif self._curBarIndex+1 == curBarIndex:
                super().append(value)
                self._curBarIndex = curBarIndex
            elif self._isOpenLog:
                LogInfo(f"无效的参数, 当前self._curBarIndex = {self._curBarIndex}, currentBarIndex={curBarIndex}")
        elif self._isOpenLog:
            LogInfo(f"无效的参数,{key} {value}")

    #
    def __getitem__(self, item):
        length = len(self)
        if length == 0:
            return None
        elif 0<=item<length or -length<=item<=-1:
            return super().__getitem__(item)
        elif item<0 and item<-length:
            if self._isOpenLog:
                LogInfo(f"无效的参数{item}, 实际返回下标{-length}")
            return super().__getitem__(-length)
        elif item>0 and item>length-1:
            if self._isOpenLog:
                LogInfo(f"无效的参数{item}, 实际返回下标{length-1}")
            return super().__getitem__(length-1)

    def __iter__(self):
        return super().__iter__()

    def append(self, value):
        self[-1] = value

    def __len__(self):
        return super().__len__()

    def __add__(self, other):
        if len(self) != len(other):
            if self._isOpenLog:
                LogInfo(f"长度不一样,{len(self)}, {len(other)}")
            return
        result = [a+b for a,b in zip(super().__iter__(), other)]
        resultObj = self.__class__(result, self._isOpenLog)
        return resultObj

