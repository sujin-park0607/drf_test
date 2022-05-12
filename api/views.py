from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from .serializers import UsersSerializer

from .models import Users,Stay

import datetime
from django.db.models import Count

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
    if serializer.is_valid(): 
        serializer.save()
        suc_tru = {
            'id' : data['api_id'],
            'success': "True"
            }
        print(suc_tru)
        return JsonResponse(suc_tru)
    else:
        print(serializer.errors)
    
    # return Response(serializer.data, status=)
    suc_fal = {'success': "False"}
    return JsonResponse(suc_fal)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def year(request):
    # data = Stay.objects.filter('years__').values()
    # first_date = datetime.date(2021, 2, 20)
    # last_date = datetime.date(2022, 5, 30)
    year = Stay.objects.all().dates('dateTime','year')
    total = Stay.objects.all().count()

    result = []
    for i in range(len(year)):
        count = Stay.objects.filter(dateTime__year=int(str(year[i])[:4])).count()
        result.append({"year":str(year[i])[:4], "count":count, "total":total})

    return JsonResponse({"year":result})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def month(request):
    # month = Stay.objects.all().dates('dateTime','month')
    # total = Stay.objects.all().count()
    # print(str(month[0])[5:7])

    what = Stay.objects.values('dateTime__year').annotate(count=Count('id')).values('dateTime__year','count')
    what[0].total = 127
    print(what)
    # result = []
    # for i in range(len(year)):
    #     count = Stay.objects.filter(dateTime__month=int(str(month[0])[5:7])).count()
    #     result.append({"month":str(year[i])[:4], "count":count, "total":total})

    # return JsonResponse({"month":what})
    return HttpResponse("hi")


#테스트 데이터를 위함
# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def year(request):
#     data = JSONParser().parse(request)
#     serializer = StaySerializer(data=data)
#     if serializer.is_valid(): 
#         serializer.save()
#         return JsonResponse(serializer.data, status=201)
    
