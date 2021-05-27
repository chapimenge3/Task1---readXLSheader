from django.urls import path 

from .views import redirect_home, analysis, Task1, Task2, Task3



urlpatterns = [
    path("", redirect_home),
    path("readXLSheader", Task1.as_view() , name="readXLSheader"),
    path("task2", Task2.as_view() , name="task2"),
    path("task3", Task3.as_view(), name="task3")
] 