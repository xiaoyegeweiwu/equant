import talib

count = 0

def initialize(context): 
    SetBarInterval("NYMEX|F|CL|1909", 'M', 1, 50)


def handle_data(context):
    global count
    count += 1
    if count > 10:
        return
    Alert(str(count), True, 'Info')
