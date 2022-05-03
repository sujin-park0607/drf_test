from django.db import models


class Users(models.Model):
    api_id = models.TextField()
    email = models.TextField()
    password = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

class Year(models.Model):
    year = models.IntegerField()
    count = models.IntegerField()
    total = models.IntegerField()

class Month(models.Model):
    year = models.IntegerField()
    month = models.CharField(max_length=5)
    count = models.IntegerField()
    total = models.IntegerField()

class Day(models.Model):
    year = models.IntegerField()
    month = models.TextField()
    day = models.CharField(max_length=5)
    count = models.IntegerField()
    total = models.IntegerField()

class Time(models.Model):
    year = models.IntegerField()
    month = models.TextField()
    day = models.TextField()
    time = models.CharField(max_length=2)
    count = models.IntegerField()
    total = models.IntegerField()

class Now(models.Model):
    time = models.CharField(max_length=2)
    count = models.IntegerField()
    total = models.IntegerField()
    