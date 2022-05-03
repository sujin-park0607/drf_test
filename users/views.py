from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Addresses
from .serializers import AddressesSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate



#전체주소록리스트
@csrf_exempt 
def address_list(request):
    #주소 전체 조회
    if request.method == 'GET':
        query_set = Addresses.objects.all()
        serializer = AddressesSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)
    #신규주소 생성
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors,status=400)

#단건 주소록 조회, 수정, 삭제
@csrf_exempt
def address(request, pk):

    obj = Addresses.objects.get(pk=pk)

    #단건 조회
    if request.method == 'GET':
        serializer = AddressesSerializer(obj)
        return JsonResponse(serializer.data, dafe = False)

    #수정
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    #삭제  
    elif request=='DELETE':
        obj.delete()
        return HttpResponse(status=204)

def login_page(request):
    return render(request,"addresses/login.html")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        print("request"+str(request))
        print("body" + str(request.body))
        userid = request.POST.get("userid", "")
        userpw = request.POST.get("userpw", "")
        login_result = authenticate(username=userid,password=userpw)
        
        print("userid = " + userid + "  userpw = "+ userpw)

        if login_result:
            return HttpResponse(status=200)
        else:
            return render(request,"addresses/login.html",status=401)


        # data = JSONParser().parse(request)
        # search_name = data['name']
        
        # obj = Addresses.objects.get(name=search_name)

        # if data['phone_number'] == obj.phone_number:
        #     return HttpResponse(status=200)
        # else:
        #     return HttpResponse(status=400)
    return HttpResponse(status=200)

