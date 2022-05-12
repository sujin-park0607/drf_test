from django.urls import path, include
from api import views

urlpatterns = [
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('year/',views.year,name="year"),
    path('month/',views.month,name="month"),
    # path('month/',views.month,name="month"),
]