from django.urls import path 
from . import views


app_name = 'db'

urlpatterns = [
    path('', views.corr_lst, name='corr_lst'),
    path('<str:ticker>/', views.corr, name='corr'),
]
