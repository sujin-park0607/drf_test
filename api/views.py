from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from .serializers import UsersSerializer, StaySerializer

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

# @api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
# def year(request):
#     # data = Stay.objects.filter('years__').values()
#     # first_date = datetime.date(2021, 2, 20)
#     # last_date = datetime.date(2022, 5, 30)
#     year = Stay.objects.all().dates('dateTime','year')
#     total = Stay.objects.all().count()

#     result = []
#     for i in range(len(year)):
#         count = Stay.objects.filter(dateTime__year=int(str(year[i])[:4])).count()
#         result.append({"year":str(year[i])[:4], "count":count, "total":total})

#     return JsonResponse({"year":result})



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def year(request):
    total = Stay.objects.all().count()
    year = Stay.objects.values('dateTime__year').annotate(count=Count('id')).values('dateTime__year','count')

    result = []
    year_list = set()
    for i in range(len(year)):
        year[i]['total'] = total
        year_list.add(year[i]['dateTime__year'])
        result.append(year[i])
    print(result)
    print(year_list)

    return JsonResponse({"month":result})
    # return HttpResponse("hi")

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def month(request):
    result = dict()

    total = Stay.objects.all().count()
    year_list = Stay.objects.all().dates('dateTime', 'year')

    for years in year_list:
        content = []
        month = Stay.objects.filter(dateTime__year = years.year).values('dateTime__month').annotate(count=Count('id')).values('dateTime__month','count')
        for i in range(len(month)):
            month[i]['total'] = total
            content.append(month[i])
        
        result[str(years.year)] = content
    print(result)
    month = Stay.objects.values('dateTime__year').values('dateTime__month').annotate(count=Count('id')).values('dateTime__year','dateTime__month','count')
    # print(month)
    # total = Stay.objects.all().count()
    # year = Stay.objects.values('dateTime__month').annotate(count=Count('id')).values('dateTime__year','count')

    # result = []
    # for i in range(len(year)):
    #     year[i]['total'] = total
    #     result.append(year[i])
    # print(result)

    return JsonResponse({"month":result})


# 테스트 데이터를 위함
# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def year(request):
#     data = JSONParser().parse(request)
#     serializer = StaySerializer(data=data)
#     if serializer.is_valid(): 
#         serializer.save()
#         print(serializer.data)
#         return JsonResponse(serializer.data, status=201)
    
