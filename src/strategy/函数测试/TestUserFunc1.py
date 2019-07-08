import talib
import UserFunc1
from UserFunc2 import UserModel

code1 = "DCE|Z|I|MAIN"
code2 = "ZCE|Z|TA|MAIN"

g_UserFunc2 = UserModel()

def initialize(context): 
    SetBarInterval(code1, 'M', 1, 1)
    SetBarInterval(code2, 'M', 1, 1)
    SetTriggerType(3, 1000)


def handle_data(context):
    last1 = UserFunc1.getQLast(code1)
    last2 = UserFunc1.getQLast(code2)
    LogInfo(last1, last2,g_UserFunc2.getCurTime(code1))
    pass
