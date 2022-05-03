from django.contrib import admin
from rest_framework import routers
from users import views
from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
# from django.views.generic import AddressesView

# class HomeTemplateView(AddressesView):
#     template_name = 'index.html'

urlpatterns = [
    # path('',HomeTemplateView.as_view(),name='home'),
    # path('',views.login_page),
    path('admin/',admin.site.urls),
    path('',TemplateView.as_view(template_name='index.html')),
    path('api/',include('api.urls')),

    #rest-auth
    # path('rest-auth/',include('rest_auth.urls')),
    # path('rest-auth/signup/',include('rest_auth.registration.urls'))
    # path('addresses/',views.address_list),
    # path('addresses/<int:pk>',views.address),
    # path('login/',views.login),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]