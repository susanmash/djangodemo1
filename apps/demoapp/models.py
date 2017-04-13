from __future__ import unicode_literals
from django.db import models
from django_admin_dialog.mixins import DjangoAdminDialogMixin
from datetime import datetime, timedelta, tzinfo
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# User managers
class UserManager(models.Manager):
    def validation(self, email, password, conf_password, name):
        fields=[]
        userExists = Users.objects.filter(email=email)
        if userExists:
            fields.append("Account with this email already exists.")
        if not EMAIL_REGEX.match(email):
            fields.append("Email is invalid")
        if len(name) < 2:
            fields.append("Name is requird")
        if len(password) < 6:
            fields.append("Password is requird")
        if len(conf_password) < 1:
            fields.append("Confirm password")
        if password != conf_password:
            fields.append("Password must match")
        if len(fields) > 0:
            print(fields)
            return fields
        elif fields == False:
            return fields

    def loginValid(self, email, password):
        l_fields=[]
        try:
            user = Users.objects.get(email=email)
            if user:
                if user.pw_hash == bcrypt.hashpw(password.encode(), user.pw_hash.encode()):
                    return user
                else:
                    l_fields.append("Incorrect password")
        except:
            l_fields.append("Email is invalid")
            return l_fields
#models
class Users(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    pw_hash=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
