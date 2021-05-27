from django.urls import path 

from .views import renderexcel,redirect_home, analysis

urlpatterns = [
    path("", redirect_home),
    path("readXLSheader", renderexcel, name="readXLSheader"),
    path("analysisreadXLSheader", analysis, name="analysisreadXLSheader")
]