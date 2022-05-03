from calendar import month
from rest_framework import serializers
from .models import Month, Users, Year, Day, Time, Now

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['api_id','email','password']

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = [ "year", "count","total" ]


class NowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Now
        fields = ["time","count","total"]

