from django.contrib import admin
from rest_framework import routers
from users import views
from django.urls import path
from django.conf.urls import include



urlpatterns = [
    # path('',views.login_page),
    path('admin/',admin.site.urls),

    #rest-auth
    path('rest-auth/',include('rest_auth.urls')),
    path('rest-auth/signup/',include('rest_auth.registration.urls'))
    # path('addresses/',views.address_list),
    # path('addresses/<int:pk>',views.address),
    # path('login/',views.login),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]