from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.parsers import JSONParser

from api.broker import BASE_DIR
from .serializers import UsersSerializer, StaySerializer

from .models import Users,Stay
from people_counter.opencv_counter import PeopleCounter

import cv2
from collections import defaultdict
import json
from datetime import datetime, timedelta
import datetime
import base64

# from VideoStreaming import VideoStreaming
# peoplecounter = PeopleCounter()
# peoplecounter.run()


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

        return JsonResponse(suc_tru)
    #error confirm
    # else:
    #     print(serializer.errors)
    
    # return Response(serializer.data, status=)
    suc_fal = {'success': "False"}
    return JsonResponse(suc_fal)


def getDatetimeDic():
    df_dic = lambda: [defaultdict(df_dic)]
    result = df_dic()
    dt_list = Stay.objects.values("dateTime")
    for dt in dt_list:
        Y = str(dt['dateTime'].year)
        M = str(dt['dateTime'].month).zfill(2)
        D = str(dt['dateTime'].day).zfill(2)
        h = str(dt['dateTime'].hour).zfill(2)
        m = str(dt['dateTime'].minute).zfill(2)
        s = str(dt['dateTime'].second).zfill(2)

        YM = f"{Y}-{M}"
        YMD = f"{YM}-{D}"
        
        tmp = result[0][Y][0][YM][0][YMD]

        # 해당 일에 모든 시간이 없을 때, 아예 처음
        if len(tmp[0].keys()) == 0:
            result[0][Y][0][YM][0][YMD] = [{
                "time" : h,
                "count" : 1,
                "total" : 1
            }]
        else:
            found = False

            # 일단 모든 시를 total 1씩 증가
            for d in result[0][Y][0][YM][0][YMD]:
                d["total"] += 1

                #만약 현재 넣을 시가 있으면
                if d["time"] == h:
                    found = True

            # 만약 현재 넣을 시가 있으면 카운트만 증가
            if found:
                d["count"] += 1

            # 현재 넣을 시가 없으면 새로 추가
            else:
                result[0][Y][0][YM][0][YMD].append({
                    "time" : h,
                    "count" : 1,
                    "total" : result[0][Y][0][YM][0][YMD][0]["total"]
                })
    return result

#main graph
#year
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def year(request):
    mon = json.loads(month(request._request).getvalue())["month"]
    result = []

    S = sum([i[0][0]["total"] for i in mon[0].values()])
    for k, v in mon[0].items():
        result.append({
            "year" : f"{k}년",
            "count" : v[0][0]["total"],
            "total" : S
        })

    return JsonResponse({"year" : result})

#month
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def month(request):
    result = json.loads(day(request._request).getvalue())["day"]

    for Y in result[0]:
        M = result[0][Y][0]
        result[0][Y][0] = []
        S = sum([i[0][0]["total"] for i in M.values()])
        for k, v in M.items():
            result[0][Y][0].append({
                "month" : f"{int(k.split('-')[-1])}월",
                "count" : v[0][0]["total"],
                "total" : S
            })

    return JsonResponse({"month" : result})

#day
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def day(request):
    result = getDatetimeDic()

    for Y in result[0]:
        for M in result[0][Y][0]:
            D = result[0][Y][0][M][0]
            result[0][Y][0][M][0] = []
            S = sum([i[0]["total"] for i in D.values()])
            for k, v in D.items():
                result[0][Y][0][M][0].append({
                    "day" : k,
                    "count" : v[0]["total"],
                    "total" : S
                })

    return JsonResponse({"day" : result})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def time(request):
    result = getDatetimeDic()
    return JsonResponse({"time" : result})


#sub graph
#subyear
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def subyear(request):
    mon = json.loads(month(request._request).getvalue())["month"]

    S = sum([i[0][0]["total"] for i in mon[0].values()])
    total = []
    total.append( [
        {
            "name" : f"{k}년",
            "value" : round(v[0][0]["total"]/S * 100),
        }
        for k, v in mon[0].items()
    ])

    total.append([
        {
            "name" : f"{k}년",
            "value" : v[0][0]["total"],
        }
        for k, v in mon[0].items()
    ])
    total_dic = dict()
    total_dic["total"] = total

    return JsonResponse({"subyear" : [total_dic]})

#submonth
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def submonth(request):
    mon = json.loads(month(request._request).getvalue())["month"]
    years = [2020,2021,2022]
    result = dict()
    cnt = 0

    content = [[[],[]] for i in range(len(years))]
    for year in years:
        total_sum = 0
        for k,v in mon[0].items():
            if int(k) == year or int(k) == year-1:
                total_sum += v[0][0]["total"]

        for k,v in mon[0].items():
            if int(k) == year or int(k) == year-1:
                content[cnt][0].append({
                    "name" : f"{k}년",
                    "value" : v[0][0]["total"]
                })

                content[cnt][1].append({
                    "name" : f"{k}년",
                    "value" : round(v[0][0]["total"]/total_sum * 100)
                })
  
        result[year] = content[cnt]
        cnt += 1

    return JsonResponse({"submonth" : result})
        

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def now(request):
    now = list()
    total = 0
    for i in range(24):
        current = datetime.datetime.now()
        hour_nac = Stay.objects.filter(dateTime__year=current.year, dateTime__month=current.month, dateTime__day=current.day, dateTime__hour = i)
        count = hour_nac.filter(inout=1).count()
        total += count

        now.append({
            "time" : f"{i}시",
            "count" : count,
            "total": total 
        })  
    
    return JsonResponse({"now" : now})


#subday
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def subday(request):
    result = json.loads(day(request._request).getvalue())["day"]
    months = [i for i in range(1,13)]
    result1 = dict()
    result2 = dict()
    cnt = 0
    
    
    for Y in result[0]:
        M = result[0][Y][0]
        
        content = [[[],[]] for _ in range(len(months))]
        for month in M:
            month_num = int(month[-2:])
            total_sum = 0

            for k,v in M.items():
                if int(k[-2:]) == month_num or int(k[-2:]) == month_num-1:
                    total_sum += v[0][0]["total"]

            for k,v in M.items():
                if int(k[-2:]) == month_num or int(k[-2:]) == month_num-1:
                    content[cnt][0].append({
                        "name" : f"{month[-2:]}",
                        "value" : v[0][0]["total"]
                    })

                    content[cnt][1].append({
                        "name" : f"{month[-2:]}",
                        "value" : round(v[0][0]["total"]/total_sum * 100)
                    })
            result1[month[-2:]] = content[cnt]
            cnt += 1
            
        result2[Y] = [result1]

    return JsonResponse({"subday" : [result2]})

#subtime
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def subtime(request):
    result = getDatetimeDic()
    days = [i for i in range(1,31)]
    result1 = dict()
    result2 = dict()
    result3 = dict()
    cnt = 0
    
    
    for Y in result[0]:
        for M in result[0][Y][0]:
            D = result[0][Y][0][M][0]

            content = [[[],[]] for _ in range(len(days))]
            for day in D:
                day_num = int(day[-2:])
                total_sum = 0
        
                for k,v in D.items():
                    if int(k[-2:]) == day_num or int(k[-2:]) == day_num-1:
                        total_sum += v[0]["total"]

                for k,v in D.items():
                    if int(k[-2:]) == day_num or int(k[-2:]) == day_num-1:
                        content[cnt][0].append({
                            "name" : f"{day[-2:]}일",
                            "value" : v[0]["total"]
                        })

                        content[cnt][1].append({
                            "name" : f"{day[-2:]}일",
                            "value" : round(v[0]["total"]/total_sum * 100)
                        })
                
                result1[day[-2:]] = content[cnt]
                cnt += 1
                
            result2[M[-2:]] = [result1]

        result3[Y] = [result2]

    return JsonResponse({"subtime" : result3})



#subnow
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def subnow(request):
    now = list()
    current_total = 0
    before_total = 0

    current = datetime.datetime.now()
    current_day = Stay.objects.filter(dateTime__year=current.year, dateTime__month=current.month, dateTime__day=current.day)
    before=datetime.datetime.now()-datetime.timedelta(days=1)
    before_day = Stay.objects.filter(dateTime__year=before.year, dateTime__month=before.month, dateTime__day=before.day)


    before_count = before_day.filter(inout=1).count()
    current_count = current_day.filter(inout=1).count()

    current_total += current_count
    before_total += before_count

    total = current_total + before_total

    now.append(
    [{
        "name" : f"{before.day}일",
        "value" : before_total, 
    },
    {
        "name" : f"{current.day}일",
        "value" : current_total, 
    }]),
 

    if before_total != 0 and current_total != 0:
        now.append(
        [{
            "name" : f"{before.day}일",
            "value" : round(before_total/total * 100), 
        },
        {
            "name" : f"{current.day}일",
            "value" : round(current_total/total * 100), 
        }])
    else:
        now.append(
        [{
            "name" : f"{before.day}일",
            "value" : 0, 
        },
        {
            "name" : f"{current.day}일",
            "value" : 0, 
        }])  
    
    return JsonResponse({"subnow" : now})

    




# @api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
def streaming(request):
    return render(request,'streaming/streaming.html')


# def getStream(request):
#     # POST 요청일 때
#     if request.method == 'POST':
#         context = {
#             'result': f"/static/result_stream_img.png",
#         }
#         # frame = cv2.imread(f"/static/result_stream_img.png")
#         # resulkt = base64(frame)
#         return JsonResponse(context)


# VideoStreaming
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def video_check(request):
    # frame = cv2.imread(f"/static/result_stream_img.png")
    # # frame.encode("base64")
    # base64_string = base64.b64encode(frame)
    # print(base64_string)
    # return JsonResponse(base64_string)

    with open('static/result_stream_img.png', 'rb') as img:
        base64_string = base64.b64encode(img.read())
    print("Success")
    return JsonResponse(base64_string)



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def video_origin(request):

    with open('static/origin_stream_img.png', 'rb') as img:
        base64_string = base64.b64encode(img.read())
    print("Success")

    return JsonResponse(base64_string)





    
