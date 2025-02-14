from django.urls import path
from .views import calculate_equity

urlpatterns = [
    path('calculate/', calculate_equity, name='calculate_equity'),
]
