from django.conf.urls import url,include
from users import views
from django.urls import path

urlpatterns = [
    path('addresses/',views.address_list),
    path('addresses/<int:pk>',views.address),
    path('login/',views.login),
    path('^api-auth/',include('rest_framework.urls', namespace='rest_framework'))
]