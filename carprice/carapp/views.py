import re
from tkinter import Y
from turtle import st
from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.


def home(request):
    #return HttpResponse("hi this is home")
    NM = request.POST.get('NM',False)
    RPM = request.POST.get('RPM',False)
    print(NM)
    print(RPM)
    power = int(NM) * int(RPM)
    hp = int(int(power)/7127)
    print(power)
    data = {'power':power,'hp' : hp}
    return render(request,'home.html',data) 

def predict(request):
    return render(request,'predict.html')     




# load model and cars list 
from fuzzywuzzy import process
import numpy as np
import pickle



def load_model():
    with open('model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
data = load_model()
model = data["model"]
le_name = data["le_name"]
le_fuel = data["le_fuel"]
le_sell = data["le_sell"]
le_trans= data["le_trans"]
le_owner= data["le_owner"]


with open("cars.pkl","rb") as f:
    cars =pickle.load(f)








def predictprice(request):
    print(request.method)
    name = request.POST.get('name',False)
    year = request.POST.get('year',False)
    fuel = request.POST.get('fuel',False)
    seller_type = request.POST.get('seller_type',False)
    o_type = request.POST.get('o_type',False)
    trans =request.POST.get('trans', False)
    seat = request.POST.get('seat',False)
    km_drive = request.POST.get('km_drive',False)
    engine = request.POST.get('engine',False)
    mileage = request.POST.get('mileage',False)
    max_power = request.POST.get('max_power',False)
    nm =request.POST.get('nm', False)

    result = process.extractOne(name,cars)
    name = result[0]
    

    input_data = np.array([[name,year,km_drive,fuel,seller_type,trans,o_type,mileage,engine,max_power,seat,nm]])
    input_data[:,0] = le_name.transform(input_data[:,0])
    input_data[:,3] = le_fuel.transform(input_data[:,3])
    input_data[:,4] = le_sell.transform(input_data[:,4])
    input_data[:,5] = le_trans.transform(input_data[:,5])
    input_data[:,6] = le_owner.transform(input_data[:,6])
    input_data = input_data.astype(float)
    print(input_data)
    y_pred = model.predict(input_data)
    y_pred = np.round(y_pred)
    y_pred = y_pred.astype(str)
    print(type(y_pred))
    y_pred = str(y_pred).replace("["," ").replace("]"," ")
    print(type(y_pred))
    print(y_pred)
    a =y_pred
    a =list(a)
    b = a[-7]
    a[-7] = ','+b 
    b = a[-9]
    a[-9] = ','+b 
    a = ''.join(a)
    y_pred =a
    context = {"pred" : a,
              "name" :name,
              "fuel" :fuel,
              "seller_type":seller_type,
              "o_type" :o_type,
              "trans" :trans,
              "seat" :seat,
              "year" : year,
              "km_drive":km_drive,
              "engine":engine,
              "mileage":mileage,
              "max_power":max_power,
              "nm": nm
              }
    return render(request,"predictprice.html",context)   




