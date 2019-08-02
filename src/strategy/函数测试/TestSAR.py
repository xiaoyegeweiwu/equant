import talib
from EsTaClass import UC_SAR
from EsSeries import NumericSeries

runsVar = 4

mySAR = UC_SAR()

OParCl2        = NumericSeries()
OParOp2        = NumericSeries()
OPosition2     = NumericSeries()
OTRansition2   = NumericSeries()


def initialize(context): 
    SetBarInterval("DCE|F|J|1909", 'M', 1, 2000)


def handle_data(context):
    global OParCl2,OParOp2,OPosition2,OTRansition2
    afStep  = runsVar / 100 
    afLimit = afStep  * 10
    sar = talib.SAR(High(), Low(), afStep,afLimit)

    OParCl, OParOp, OPosition, OTRansition = ParabolicSAR(High(), Low(), afStep, afLimit)

    OParCl2[-1], OParOp2[-1], OPosition2[-1], OTRansition2[-1] = mySAR.U_SAR(High(), Low(), afStep, afLimit)
    
    #LogInfo("SAR", Date(), Time(), sar[-1], OParCl[-1])
    PlotNumeric("SAR", sar[-1])
    PlotNumeric("ESAR", OParCl[-1], color=RGB_Blue())
    PlotNumeric("USAR", OParCl2[-1], color=RGB_Green())
    #LogInfo("AAAA:", Date(), Time(), OParCl[-1], OParOp[-1], OPosition[-1], OTRansition[-1])
