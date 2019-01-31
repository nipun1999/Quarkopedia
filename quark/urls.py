"""quark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signIn, name='signin'),
    path('news/', views.news, name='news'),
    path('profile/', views.profile, name='profile'),
    path('signout/', views.signOut, name='signout'),
    path('signup/', views.signUp, name='signup'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('trade/', views.trade, name='trade'),
    path('notrade/', views.marketClosed, name='marketClosed'),
    path('stockPrices/', views.stockPrices, name='stockPrices'),
    path('ranks/', views.ranking, name='ranking'),
    path('history/', views.orderHistory, name='history'),
    path('Email/', views.Email, name='Email'),
    path('chemicalX', views.chemicalX, name='chemicalX'),
    path('About/', views.About, name='About'),
    path('FAQ/', views.FAQ, name='FAQ'),
    path('otp/', views.otp, name='otp'),
    path('verification/', views.verification, name='verification'),
    path('stockpages/', views.stockpages, name='stockpages'),
    path('AnalogElectronics/', views.AnalogElectronics, name='AnalogElectronics'),
    path('PowerElectronics/', views.PowerElectronics, name='PowerElectronics'),
    path('DNA/', views.DNA, name='DNA'),
    path('Bioinformics/', views.Bioinformics, name='Bioinformics'),
    path('ProcessDesign/', views.ProcessDesign, name='ProcessDesign'),
    path('HeatTransfer/', views.HeatTransfer, name='HeatTransfer'),
    path('FluidMechanics/', views.FluidMechanics, name='FluidMechanics'),
    path('MachineDesign/', views.MachineDesign, name='MachineDesign'),
    path('Algebra1/', views.Algebra1, name='Algebra1'), 
    path('ElementaryRealAnalysis/', views.ElementaryRealAnalysis, name='ElementaryRealAnalysis'),
    path('Macroeconomics/', views.Macroeconomics, name='Macroeconomics'),
    path('AppliedEconometrics/', views.AppliedEconometrics, name='AppliedEconometrics'),
    path('AnalogAndDigital/', views.AnalogAndDigital, name='AnalogAndDigital'),
    path('IndustrialInstrumentation/', views.IndustrialInstrumentation, name='IndustrialInstrumentation'),  
    path('CommunicationSystem/', views.CommunicationSystem, name='CommunicationSystem'),
    path('Microelectronic/', views.Microelectronic, name='Microelectronic'),
    path('NeutralNetworks/', views.NeuralNetwork, name='NeuralNetwork'),
    path('ComputerArchitecture/', views.ComputerArchitecture, name='ComputerArchitecture'), 
    path('Disclaimer/',views.Disclaimer,name='Disclaimer'),
    path('credits/',views.credits,name='credits'),
    
    #path('', views.home, name='qpHome'),

   ]
