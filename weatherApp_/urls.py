from django.urls import path
from .views import *
urlpatterns = [
    path('', getOtherData, name='weather'),
    path('delete/<city_name>', deleteCity, name='delete')
]