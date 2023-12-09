from django.urls import path 
from . import views


app_name = 'db'

urlpatterns = [
    path('', views.corr_lst, name='corr_lst'),
    path('corr/<str:ticker_a>/<str:ticker_b>/', views.corr, name='corr'),
]
