from __future__ import unicode_literals
from django.db import models
import re
from pygeocoder import Geocoder
EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if postData['email'] and not re.match(EMAIL_REGEX, postData['email']) and len(postData['email']) < 5:
            errors["email"] = 'Invalid email'
        if len(postData['password1'])<8 :
            errors["password1"] = 'Password at least 8 characters'
        if postData['password1'] != postData['password2']:
            errors["password2"]=' password not match'
        return errors



class Users(models.Model):
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class From(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=225)
    zipcode = models.CharField(max_length=45)
    driver = models.ForeignKey(Users, related_name="driver")
    time_departure = models.DateTimeField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class To(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=225)
    zipcode = models.CharField(max_length=45)
    passenger = models.ManyToManyField(Users, related_name="passenger")
    price = models.FloatField()
    time_arrival = models.DateTimeField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)