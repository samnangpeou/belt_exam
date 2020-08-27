from django.db import models

# Create your models here.
from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'Your first name must be more than 2 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Your last name must be more than 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be in valid format'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Password and confirm password do not match'
        return errors
    def log_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be in valid format'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class WishManager(models.Manager):
    def validator(self,form):
        errors={}
        if len(form['content']) < 3:
            errors['length'] = 'Message must be at least 3 characters'
        if len(form['desc']) < 1:
            errors['desc'] = 'You have to add something to the description'
        return errors

class Wish(models.Model):
    content = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='wishes', on_delete=models.CASCADE)
    grants = models.CharField(max_length=3)
    likes = models.ManyToManyField(User, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()

    