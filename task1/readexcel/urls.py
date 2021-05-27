from django.urls import path 

from .views import renderexcel,redirect_home

urlpatterns = [
    path("", redirect_home),
    path("readXLSheader", renderexcel, name="readXLSheader")
]