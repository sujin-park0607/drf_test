from django.urls import path, include
from api import views

urlpatterns = [
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('year/',views.year,name="year"),
    path('month/',views.month,name="month"),
    path('day/',views.day,name="day"),
    path('time/',views.time,name="time"),

    path('subyear/',views.subyear,name="subyear"),
    path('submonth/',views.submonth,name="submonth"),
    # path('subday/',views.subday,name="subday"),
    # path('subtime/',views.subtime,name="subtime"),

    path('test_data/',views.test_data,name="test_data"),
]