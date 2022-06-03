from django.urls import path, include
from api import views

urlpatterns = [
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('year/',views.year,name="year"),
    path('month/',views.month,name="month"),
    path('day/',views.day,name="day"),
    path('time/',views.time,name="time"),
    path('now/',views.now,name="now"),

    path('subyear/',views.subyear,name="subyear"),
    path('submonth/',views.submonth,name="submonth"),
    path('subday/',views.subday,name="subday"),
    path('subtime/',views.subtime,name="subtime"),
    path('subnow/',views.subnow,name="subnow"),
    path('streaming/',views.streaming,name="streaming"),
    path('getStream/',views.getStream,name="getStream"),
]

from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)