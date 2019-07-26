from __future__ import unicode_literals
from django.db import models
import re
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



class User(models.Model):
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
    state = models.CharField(max_length=225)
    drivers = models.ForeignKey(User, related_name="users_drivers")
    riders = models.ManyToManyField(User, related_name="users_riders")
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class To(models.Model):
    from_where = models.OneToOneField(From,on_delete=models.CASCADE, related_name='to')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=225)
    zipcode = models.CharField(max_length=45)
    state = models.CharField(max_length=225)
    price = models.FloatField()
    estimate_time_arrival = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)