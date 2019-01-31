import pyrebase 
import time
from threading import Thread

config = {
    'apiKey': "AIzaSyDS_XIGRfuaSIwTQbwWF_nSdVlXdM6uvyY",
    'authDomain': "quarkstocksapp.firebaseapp.com",
    'databaseURL': "https://quarkstocksapp.firebaseio.com",
    'projectId': "quarkstocksapp",
    'storageBucket': "quarkstocksapp.appspot.com",
    'messagingSenderId': "779348030725"
}

firebase = pyrebase.initialize_app(config)  
database = firebase.database()

stockIdMap = {
    'cs01' : { 'name' : 'Neural Networks', 'industry' : 'Computer Science'},
    'cs02' : { 'name' : 'Computer Architecture', 'industry' : 'Computer Science'},
    'ece01' : { 'name' : 'Communication systems' , 'industry' : 'Electronics and Communication' },
    'ece02' : { 'name' : 'Microelectronic circuits' , 'industry' : 'Electronics ad Communication' },
    'eee01' : { 'name' : 'Analog Electronics', 'industry' : 'Electrical and Electronics' },
    'eee02' : { 'name' : 'Power Electronics', 'industry' : 'Electrical and Electronics' },
    'bio01' : { 'name' : 'Recombinant DNA Technology', 'industry' : 'Biological Sciences' },
    'bio02' : { 'name' : 'Bioinformatics', 'industry' : 'Biological Sciences' },
    'chem01' : { 'name' : 'Process Design Principles', 'industry' : 'Chemical Engineering' },
    'chem02' : { 'name' : 'Heat Transfer', 'industry' : 'Chemical Engineering' },
    'mech01' : { 'name' : 'Fluid Mechanics', 'industry' : 'Mechanical Engineering' },
    'mech02' : { 'name' : 'Machine Design and Drawing', 'industry' : 'Mechanical Engineering' },
    'math01' : { 'name' : 'Algebra 1', 'industry' : 'Mathematics' },
    'math02' : { 'name' : 'Elementary Real Analysis', 'industry' : 'Mathematics' },
    'eco01' : { 'name' :  'Macro Economics', 'industry' : 'Economics' },
    'eco02' : { 'name' :  'Applied Econometrics', 'industry' : 'Economics' },
    'eni01' : { 'name' : 'Analog and Digital VLSI Design' , 'industry' : 'Electronics and Instrumentation' },
    'eni02' : { 'name' : 'Industrial Instrumentation and Control' , 'industry' : 'Electronics and Instrumentation' }
}

def algo(currPrice, currBal, purValue, stockQty, transType, execType, askPrice, stockId, user_id):

    askRatio = askPrice/currPrice

    if stockQty >= 1500:
        delayTime = 60
    elif stockQty >= 1200:
        delayTime = 45
    elif stockQty >= 1000:
        delayTime = 30
    elif stockQty >= 750:
        delayTime = 10
    elif stockQty >= 250:
        delayTime = 4
    else: 
        delayTime = 0
    
    if execType == "stop" or execType == "limit":
        if currPrice < 100 and askRatio >= 0.95 and askRatio <= 1.05: #
            if askRatio >= 0.995 and askRatio <= 1.005: #0.005 times
                delayTime += 4
            elif askRatio >= 0.988 and askRatio <= 1.012: #0.012 times
                delayTime += 10
            elif askRatio >= 0.98 and askRatio <= 1.02: #0.02 times
                delayTime += 20
            elif askRatio >= 0.96 and askRatio <= 1.04: # 0.04 times
                delayTime += 40
            else:
                delayTime += 75
        
        elif currPrice < 300 and askRatio >= 0.98 and askRatio <= 1.02: #
            if askRatio >= 0.997 and askRatio <= 1.003:
                delayTime += 4
            elif askRatio >= 0.9945 and askRatio <= 1.0055:
                delayTime += 10
            elif askRatio >= 0.992 and askRatio <= 1.008:
                delayTime += 20
            elif askRatio >= 0.985 and askRatio <= 1.015:
                delayTime += 45
            else:
                delayTime += 90
        
        elif currPrice < 400 and askRatio >= 0.988 and askRatio <= 1.012:
            if askRatio >= 0.996 and askRatio <= 1.004:
                delayTime += 4
            elif askRatio >= 0.994 and askRatio <= 1.006:
                delayTime += 12
            elif askRatio >= 0.992 and askRatio <= 1.008:
                delayTime += 35
            elif askRatio >= 0.99 and askRatio <= 1.01:
                delayTime += 60
            else:
                delayTime += 80

        elif currPrice < 800 and askRatio >= 0.988 and askRatio <= 1.012:
            if askRatio >= 0.998 and askRatio <= 1.002:
                delayTime += 4
            elif askRatio >= 0.9975 and askRatio <= 1.0025:
                delayTime += 12
            elif askRatio >= 0.996 and askRatio <= 1.004:
                delayTime += 18
            elif askRatio >= 0.993 and askRatio <= 1.007:
                delayTime += 45
            elif askRatio >= 0.991 and askRatio <= 1.009:
                delayTime += 75
            else:
                delayTime += 120
        
        elif currPrice < 1200 and askRatio >= 0.992 and askRatio <= 1.008:
            if askRatio >= 0.998 and askRatio <= 1.002:
                delayTime += 4
            elif askRatio >= 0.9975 and askRatio <= 1.0025:
                delayTime += 12
            elif askRatio >= 0.996 and askRatio <= 1.004:
                delayTime += 18
            elif askRatio >= 0.9945 and askRatio <= 1.0055:
                delayTime += 45
            elif askRatio >= 0.993 and askRatio <= 1.007:
                delayTime += 75
            else:
                delayTime += 120
        else:
            return "The order will not be possible at this time. No available buyers/sellers at the price"
    
    print("Delaying for " + str(delayTime))

    if execType == "market":
        data = {'currPrice' : currPrice}
    elif execType == "stop" or execType == "limit":
        data = {'currPrice' : askPrice}
    else:
        return "Invalid trade execution type. Don't fuck with the website."
    

    if transType == 'buy':
        print('buying')
        currBal = currBal - purValue
        data2 = {'accBal' : currBal}
        t = Thread(target = placeOrderBuy, args=(data, user_id, data2, stockId, stockQty, delayTime,))

    elif transType == 'sell':
        print('selling')
        currBal = currBal + purValue
        data2 = {'accBal' : currBal}
        t = Thread(target = placeOrderSell, args=(data, user_id, data2, stockId, stockQty, delayTime,))
    else:
        return "Invalid transaction type. Don't fuck with the website."

    t.start()
    
    if delayTime > 45:
        return "Long Warning"
    
    return ""

def placeOrderBuy(data, user_id, data2, stockId, stockQty, t):
    time.sleep(t)
    timeStr = str(time.strftime('%d %H_%M_%S_'))+ stockId
    timeStr2 = str(time.strftime('%d %b, %I:%M %p'))
    currStock = database.child("users").child(user_id).child('stockInfo').child(stockId).child('totalQty').get().val()
    currStockValue = database.child("users").child(user_id).child('stockInfo').child(stockId).child('totalValue').get().val()
    
    if currStock is None:
        currStock = stockQty
        currStockValue = stockQty*data['currPrice']
    else:
        currStock += stockQty
        currStockValue += stockQty*data['currPrice']

    dataStock = {'totalQty' : currStock, 'totalValue' : currStockValue }
    dataOrder = { 
                'name' : stockIdMap[stockId]['name'], 
                'orderQty' : stockQty, 
                'orderPrice' : data['currPrice'], 
                'type' : 'buy', 
                'time' : timeStr2
            }

    database.child("users").child(user_id).update(data2)    #user balance update
    database.child("users").child(user_id).child('stockInfo').child(stockId).set(dataStock)  
    database.child("users").child(user_id).child('orderInfo').child(timeStr).set(dataOrder)  
    database.child("stocks").child(stockId).update(data)    #commodity price update

def placeOrderSell(data, user_id, data2, stockId, stockQty, t):
    time.sleep(t)
    timeStr = str(time.strftime('%d %H_%M_%S_'))+ stockId
    timeStr2 = str(time.strftime('%d %b, %I:%M %p'))
    currStock = database.child("users").child(user_id).child('stockInfo').child(stockId).child('totalQty').get().val()
    currStockValue = database.child("users").child(user_id).child('stockInfo').child(stockId).child('totalValue').get().val()
    
    currStock -= stockQty
    currStockValue -= stockQty*data['currPrice']
    
    dataStock = {'totalQty' : currStock, 'totalValue' : currStockValue}
    dataOrder = { 
                'name' :  stockIdMap[stockId]['name'], 
                'orderQty' : stockQty, 
                'orderPrice' : data['currPrice'], 
                'type' : 'sell', 
                'time' : timeStr2
            }

    database.child("users").child(user_id).update(data2)
    database.child("users").child(user_id).child('stockInfo').child(stockId).set(dataStock)
    database.child("users").child(user_id).child('orderInfo').child(timeStr).set(dataOrder)
    database.child("stocks").child(stockId).update(data)
