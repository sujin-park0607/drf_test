from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from .serializers import UsersSerializer, StaySerializer

from .models import Users,Stay

import datetime
from django.db.models import Count

import math

#login
def login(request):
    data = Users.objects.all()
    serializer = UsersSerializer(data, many=True)
    return JsonResponse(serializer.data,safe=False)

#logout
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


#main graph
#year
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

    return JsonResponse({"year":result})

#month
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

    return JsonResponse({"month":result})

#day
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def day(request):
    result = dict()
    month_result = dict()

    total = Stay.objects.all().count()
    year_list = Stay.objects.all().dates('dateTime', 'year')
    month_list = Stay.objects.all().dates('dateTime', 'month')

    for years in year_list:
        year_content = []
        year_filter = Stay.objects.filter(dateTime__year = years.year)

        for months in month_list:
            month_content = []
            month_filter = year_filter.filter(dateTime__month = months.month)
            day = month_filter.values('dateTime__day').annotate(count=Count('id')).values('dateTime__day','count')
            
            for i in range(len(day)):
                day[i]['total'] = total
                month_content.append(day[i])
            
            month_result[str(months.month)] = month_content
            year_content.append(month_result)
        
        result[str(years.year)] = year_content
    return JsonResponse({"day":result})


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def time(request):
    result = dict()
    month_result = dict()
    day_result = dict()

    total = Stay.objects.all().count()
    year_list = Stay.objects.all().dates('dateTime', 'year')
    month_list = Stay.objects.all().dates('dateTime', 'month')
    day_list = Stay.objects.all().dates('dateTime','day')

    for years in year_list:
        year_content = []
        year_filter = Stay.objects.filter(dateTime__year = years.year)

        for months in month_list:
            month_content = []
            month_filter = year_filter.filter(dateTime__month = months.month)

            for days in day_list:
                day_content = []
                day_filter = month_filter.filter(dateTime__day = days.day)
                time = day_filter.values('dateTime__time').annotate(count=Count('id')).values('dateTime__time','count')
            
                for i in range(len(time)):
                    time[i]['total'] = total
                    day_content.append(time[i])
                
                day_result[str(days.day)] = day_content
                month_content.append(day_result)

            month_result[str(months.month)] = month_content
            year_content.append(month_result)
                
        result[str(years.year)] = year_content
    return JsonResponse({"time":result})

#sub graph
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def subyear(request):
    result = dict()
    percent = list()
    num = list()
    content = list()

    total = Stay.objects.all().count()
    year_num = Stay.objects.values('dateTime__year').annotate(count=Count('id')).values('dateTime__year','count')
    year_percent = Stay.objects.values('dateTime__year').annotate(count=Count('id')).values('dateTime__year','count')

    for i in range(len(year_percent)):
        year_percent[i]['count'] = round(year_percent[i]['count']/total * 100)
        percent.append(year_percent[i])
        num.append(year_num[i])
    
    content.append(percent)
    content.append(num)
    
    result['total'] = content
    return JsonResponse({'subyear':result})

# 테스트 데이터를 위함
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def year(request):
    data = JSONParser().parse(request)
    serializer = StaySerializer(data=data)
    if serializer.is_valid(): 
        serializer.save()
        print(serializer.data)
        return JsonResponse(serializer.data, status=201)
    
