from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from .serializers import UsersSerializer

from .models import Users,Stay

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
# def year(request):
#     data = Stay.objects.get()
#     return JsonResponse()

# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# def month(request):
#     data = JSONParser().parse(request)
#     serializer = MonthSerializer(data=data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return JsonResponse(serializer.data, safe=False)

    
