from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import UsersSerializer, YearSerializer, MonthSerializer, DaySerializer, TimeSerializer, NowSerializer

from .models import Users

# Create your views here.
def login(request):
    data = Users.objects.all()
    serializer = UsersSerializer(data, many=True)
    return JsonResponse(serializer.data,safe=False)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    data = JSONParser().parse(request)
    serializer = UsersSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # return Response(serializer.data, status=)
    return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/')

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def year(request):
    data = JSONParser().parse(request)
    serializer = YearSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def month(request):
    data = JSONParser().parse(request)
    serializer = MonthSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return JsonResponse(serializer.data, safe=False)

    
