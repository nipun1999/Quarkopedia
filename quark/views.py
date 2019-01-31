from django.shortcuts import render, redirect
from django.http import JsonResponse
import pyrebase
from .algo import algo
import time
from django.contrib import auth
from collections import OrderedDict
from authy.api import AuthyApiClient
from django.conf import settings

config = {
	'apiKey': "AIzaSyAqsYNzM3h74CDciLhKvQXaph5-VcdeG-4",
    'authDomain': "quark-o-pedia.firebaseapp.com",
    'databaseURL': "https://quark-o-pedia.firebaseio.com",
    'projectId': "quark-o-pedia",
    'storageBucket': "quark-o-pedia.appspot.com",
    'messagingSenderId': "794989305019"
}

DEFAULT_BAL=1000000

stockIdMap = {
    'cs01' : { 'name' : 'Neural Networks', 'industry' : 'Computer Science'},
    'cs02' : { 'name' : 'Computer Architecture', 'industry' : 'Computer Science'},
    'ece01' : { 'name' : 'Communication systems' , 'industry' : 'Electronics and Communication' },
    'ece02' : { 'name' : 'Microelectronic circuits' , 'industry' : 'Electronics and Communication' },
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

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()
authy_api= AuthyApiClient("8x9UksoV9DMM6T1fzMD1tFxayRLrkQnX")

user_id = None
user = None
ph = None

def signIn(request):

    if request.method == 'POST' and 'btn1' in request.POST:
        email = request.POST.get('email')
        passw = request.POST.get('pass')
        global user
        try:
            user = auth.sign_in_with_email_and_password(email,passw)
        except:
            message="Invalid Credentials"
            return render(request,"signIn.html",{"message":message})
        
        user = auth.refresh(user['refreshToken'])
        global session_id
        global user_id 
        session_id = user['idToken']
        user_id = auth.get_account_info(user['idToken'])['users'][0]['localId']
        request.session['uid']=str(session_id)
        email_verify=auth.get_account_info(user['idToken'])['users'][0]['emailVerified']
        ph_verify=database.child("users").child(user_id).child("user_verify").get().val()
        
        if ph_verify == "No":
            return render(request,'verification.html')
        if email_verify == False:
            return redirect(Email)

        return redirect(news)
    elif request.method == 'POST' and 'btn2' in request.POST:
        return render(request,'signUp.html')

    return render(request, 'signIn.html')

def forgotpass(request):
    if request.method == 'POST':
        getem = request.POST.get('getem')
        
        return render(request,'signIn.html')

    return render(request,'forgotpass.html')

def profile(request):

    if user_id is None:
        return redirect(signIn)

    idtoken= request.session['uid']
    a = user_id
    e = database.child("users").child(a).child("email").get().val()
    n = database.child("users").child(a).child("name").get().val()
    city = database.child("users").child(a).child("city").get().val()
    p = database.child("users").child(a).child("phone").get().val()
    c = database.child("users").child(a).child("college").get().val()
    r = database.child("users").child(a).child("rank").get().val()
    ac = database.child("users").child(a).child("accBal").get().val()
    return render(request,'profile.html',{"e":e,"n":n,"city":city,"p":p,"c":c,"r":r,"ac":ac})

def ranking(request):
    if user_id is None:
        return redirect(signIn)

    ranklist = []
    rank = database.child("ranking").get()
    if rank is None:
        return render(request, 'ranking.html', {'error' : 'T'})

    for i in rank.each():
        ranklist.append(i.val())

    return render(request, 'ranking.html', {'ranklist': ranklist })     


def home(request):
	return render(request, 'homepage.html', {"e":'sukdik'})

def news(request):
    if user_id is None:
        return redirect(signIn)

    newslist = []
    news = database.child("news").get()
    for i in news.each():
        newslist.append(i.val())
    return render(request, 'news.html', {'newsList': newslist })

def signOut(request):
    del request.session['uid']
    user_id = None
    return render(request,'signIn.html')


def Email(request):
    global user
    auth.send_email_verification(user['idToken'])
    return render(request,'Email.html')
def signUp(request):
    global uid
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        passw=request.POST.get('pass')
        conf_passw=request.POST.get('conf_pass')
        phone=request.POST.get('phone')
        college=request.POST.get('college')
        city=request.POST.get('city')
        print(passw)
        print(conf_passw)

        if passw!=conf_passw:
            message="Password does not match"
            return render(request,'signUp.html',{"message":message})
        elif len(passw)<6:
            message="Password Should be min 6 charachters long"
            return render(request,'signUp.html',{"message":message})
        else:
            emailDB = database.child("users").get()
            for i in emailDB.each():
                temp2 = i.val()
                if email==temp2['email']:
                    message="Email Already Exists"
                    return render(request,'signUp.html',{"message":message})
                             
            if "@goa.bits-pilani.ac.in" in email:
                user=auth.create_user_with_email_and_password(email,passw)
                uid = user['localId']
                data={'name':name,'email':email,'phone': phone, 'college':college,'city':city,'accBal': DEFAULT_BAL, 'rank': 0,'user_verify':"Yes",'userVal':DEFAULT_BAL}
                database.child("users").child(user_id).set(data)
                auth.send_email_verification(user['idToken'])
                return render(request,"signIn.html")
            else:
                phnum = database.child("users").get()
                for i in phnum.each():
                    temp=i.val()
                    if phone==temp['phone']:
                        message="Phone Number Already Exists"
                        return render(request,'signUp.html', {"message":message})

                user=auth.create_user_with_email_and_password(email,passw)
                uid = user['localId']
                data={'name':name,'email':email,'phone': phone, 'college':college,'city':city,'accBal': DEFAULT_BAL, 'rank': 0,'user_verify':"No",'userVal':DEFAULT_BAL}
                database.child("users").child(user_id).set(data)
                auth.send_email_verification(user['idToken'])
                return render(request,"verification.html")
        message="could not create account"
        return render(request,'signUp.html', {"message":message})

    return render(request,"signUp.html")

def stockPrices(request):
    if user_id is None:
        return redirect(signIn)

    data = {}
    if request.is_ajax():
        prices = database.child('stocks').get().val()
        for k,i in prices.items():
            data.update({k : i['currPrice']})
        return JsonResponse(data)
    
    return render(request,'stockPrices.html')

def portfolio(request):
    if user_id is None:
        return redirect(signIn)

    stocksList = [] #list of dictionaries of each individual stock
    stocks = database.child("users").child(user_id).child("stockInfo").get() 
    #Stocks is a dictionary of dictionaies
    
    
    if stocks.val() == None:
        return render(request, 'portfolio.html')

    for i in stocks.each():
        #temp is a dictionary
        #stocksList is a list of dictionaries
        price = database.child("stocks").child(i.key()).get().val()['currPrice'] 
        temp = i.val()
        temp2 = { 'name' : stockIdMap[i.key()]['name'], 'industry' : stockIdMap[i.key()]['industry'] }

        totalValue = temp['totalValue']
        totalQty = temp['totalQty']
        change = totalQty*price - totalValue
        change = round(change*100/totalValue, 2)
        
        temp.update({ 'change':  change })
        temp.update(temp2)
        #temp.update({'name' : stockIdMap[i.key()]['name'] })
        stocksList.append(temp)

    return render(request, 'portfolio.html', { 'purchasedStocksList' : stocksList })
 
def marketClosed(request):
    return render(request, 'marketClosed.html')

def trade(request):
    if user_id is None:
        return redirect(signIn)

    marketActive = database.child('marketActive').get().val()

    if marketActive != 'True':
        return redirect(marketClosed)

    if request.method == 'POST':

        errorMsg = ""
        stockQty = int(request.POST.get('stockQty'))
        stockId = str(request.POST.get('stockId'))
        transType = request.POST.get('transType')
        execType = request.POST.get('execType')
        askingPrice = 1

        if stockQty<=0 :
            errorMsg = 'Cannot place order for zero or lesser stocks'
        
        if execType == 'limit':
            if request.POST.get('limitAskingPrice') == '':
                askingPrice = 0
            else:
                askingPrice = int(request.POST.get('limitAskingPrice'))
        elif execType == 'stop':
            if request.POST.get('stopAskingPrice') == '':
                askingPrice = 0
            else:
                askingPrice = int(request.POST.get('stopAskingPrice'))

        if askingPrice <= 0:
            errorMsg = 'Cannot place an order with that value'

        print(user_id)
        currPrice = int(database.child("stocks").child(stockId).child('currPrice').get().val())
        currBal = int(database.child("users").child(user_id).child('accBal').get().val())
        userStocks = database.child("users").child(user_id).child('stockInfo').child(stockId).child('totalQty').get().val()
        if userStocks is None:
            userStocks = 0

        purValue = stockQty*currPrice
        print(purValue)

        if purValue > 500000:
            return render(request, 'trade.html', {'errorMsg' : 1})
        elif transType == "buy" and purValue > currBal:
            errorMsg = "Insufficient funds to place order"
        elif transType == "sell" and userStocks < stockQty:
            errorMsg = "You do not have enough stocks"

        if execType == "limit" and askingPrice < currPrice :
            errorMsg = 'Cannot demand lower than Stock price when in Limit mode'
        elif execType == "stop" and askingPrice > currPrice:
            errorMsg = 'Cannot demand higher than Stock price when in stop mode'
        elif errorMsg == "":
            errorMsg = algo(currPrice, currBal, purValue, stockQty, transType, execType, askingPrice, stockId, user_id)
            if errorMsg == "":
                return render(request, 'trade.html', { 'success' : 'T'})
            elif errorMsg == "Long Warning":
                return render(request, 'trade.html', { 'success' : 'T', 'warning' : 'T' })
            else:
                return render(request, 'trade.html', { 'errorMsg' : errorMsg })

        return render(request, 'trade.html', {'errorMsg' : errorMsg })

    return render(request, 'trade.html')     

def orderHistory(request):
    if user_id is None:
        return redirect(signIn)

    unorderList = database.child('users').child(user_id).child('orderInfo').order_by_key().get().val()

    if unorderList == None:
        return render(request, 'orderHistory.html', { 'error' : 'T'})

    orderList = OrderedDict(unorderList)
    newList = []


    pageSize = 6;
    st = 1
    n=0
    p=0
    reqn = None
    reqp = None

    if request.method == 'POST':
        reqn = request.POST.get('next')
        reqp = request.POST.get('prev')
        if reqn is not None and reqn >= '1':
            st = int(request.POST.get('next')) + pageSize
        elif reqp is not None and reqp >= '1':
            st = int(request.POST.get('prev')) - pageSize
    else:
        st=1

    j=1
    for k,i in reversed(orderList.items()):
        print(i)
        if j >= st:
            if j >= st+pageSize:
                break
            newList.append(i)
        j = j + 1

    if len(orderList) >= st+pageSize:
        n = st
    else:
        n = 0

    if st > 1:
        p = st 

    print(newList)
    return render(request, 'orderHistory.html', { 'newList' : newList, 'n' : n, 'p' : p })

def chemicalX(request):

    adminList = [
        'PDtt3WiroZOnjneL2YyyIiq4zCp2',
    ]

    if user_id is None:
        return redirect(signIn)
    elif user_id not in adminList:
        return redirect(signIn)

    msg = 'Welcome Powerpuff girls'

    if request.method == 'POST':
        check = request.POST.get('option')
        if check is not None:
            if check == '1':
                msg = 'Sorting'
                allUsers = database.child('users').get()
                finalList = []

                for i in allUsers.each():
                    user = i.val()
                    totVal = 0
                    print(user)

                    if 'stockInfo' in user:
                        print(user['stockInfo'])

                        for key,value in user['stockInfo'].items():
                            totVal += value['totalValue']

                    totVal += user['accBal']
                    listElement = {'rank' : 0, 'name' : user['name'], 'userValue' : totVal }
                    finalList.append(listElement)

                sortedList = sorted(finalList, key=lambda k: k['userValue'], reverse=True)

                j = 1
                for i in sortedList:
                    i.update({'rank' : j})
                    j = j+1

                database.child('ranking').set(sortedList)
                print('Done')


    return render(request, 'chemicalX.html', {'msg' : msg})

def About(request):
    return render(request,'About.html')

def Disclaimer(request):
    return render(request,'Disclaimer.html')

def FAQ(request):
    return render(request,'FAQ.html')


def stockpages(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'stockpages.html')

def AnalogElectronics(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'AnalogElectronics.html')

def PowerElectronics(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'PowerElectronics.html')

def DNA(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'DNA.html')

def Bioinformics(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'Bioinformics.html')

def ProcessDesign(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'ProcessDesign.html')

def HeatTransfer(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'HeatTransfer.html')

def FluidMechanics(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'FluidMechanics.html')

def MachineDesign(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'MachineDesign.html')

def Algebra1(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'Algebra1.html')

def ElementaryRealAnalysis(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'ElementaryRealAnalysis.html')

def Macroeconomics(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'Macroeconomics.html')

def AppliedEconometrics(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'AppliedEconometrics.html')

def AnalogAndDigital(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'AnalogAndDigital.html')

def IndustrialInstrumentation(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'IndustrialInstrumentation.html')

def CommunicationSystem(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'CommunicationSystem.html')

def Microelectronic(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'Microelectronic.html')

def NeuralNetwork(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'NeuralNetwork.html')

def ComputerArchitecture(request):
    if user_id is None:
        return redirect(signIn)
    return render(request,'ComputerArchitecture.html')

def verification(request):
    if request.method == 'POST':
        global ph
        ph = request.POST.get('ph')
        request.session['phone_number']=ph
        authy_api.phones.verification_start (
                ph,"91","sms"
        )
        return render(request,'otp.html')
    return render(request,'verification.html' )

def otp(request): 
    global ph
    global uid
    if request.method == 'POST':
        otp= request.POST.get('otp')
        request.session['otp']=otp
        print(otp)
        verification= authy_api.phones.verification_check (

            ph,"91",otp

        )
        if verification.ok():
            request.session['isverified']=True
            message="otp verified"
            database.child("users").child(user_id).update({'user_verify' :'Yes'})
            return render(request,'signIn.html')
        else:       
            return render(request,'otp.html')      
    return render(request,'otp.html')           

def returnPrice(request):
    if request.is_ajax():
        price = database.child('stocks').child(request.POST.get('stockId')).child('currPrice').get().val()
        data = {'price' : price}
        return JsonResponse(data)
    else:
        return redirect(news)

def credits(request):
    return render(request,'credits.html')
