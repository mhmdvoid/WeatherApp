from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
import requests
def getOtherData(request):
    url_of_db = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=Metric&APPID=77b00919299911fa2ff0def86d1ad705'

    city_form = CityForm()
    all_cities = City.objects.all()

    if request.method == 'POST':
        city_form = CityForm(request.POST)
        if city_form.is_valid():
            the_inserted_city = city_form.cleaned_data.get('city_name')
            if City.objects.filter(city_name=the_inserted_city).count() == 0:
                again_seeing_response = requests.get(url_of_db.format(the_inserted_city)).json()
                if again_seeing_response['cod'] == 200:
                    city_form.save()
                    messages.success(request, 'has been submitted successfully')

                    return redirect('weather')
                else:
                    messages.info(request, 'No This City, we do not have in our DB .. ')
            else:
                messages.info(request, 'No This City you have inserted already ')

    weather_list = []
    for city in all_cities:
        the_data = requests.get(url_of_db.format(city)).json()
        the_city_weather = {
            'main_weather': the_data['main']['temp'],
            'describe_weather': the_data['weather'][0]['description'],
            'city_name': the_data['name'],
            'icon': the_data['weather'][0]['icon'],
        }

        weather_list.append(the_city_weather)
    # print(weather_list)
    # for each in weather_list:
    #     print(each['city_name'])
    # print(each_object)
    context = {
        'form': city_form,
        'weather': weather_list
    }
    return render(request, 'find_wether.html', context)
def deleteCity(request, city_name):
    ci = City.objects.filter(city_name=city_name)
    if ci.exists():
        ci[0].delete()
        messages.success(request, 'Has been successfully deleted')
    return redirect('weather')