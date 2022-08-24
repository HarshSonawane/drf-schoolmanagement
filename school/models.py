from django.contrib.auth.models import User
from django.db import models


class School(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # name                = models.CharField(max_length=255, unique=True, db_index=True)
    # email               = models.CharField(max_length=255, unique=True, db_index=True)
    # password            = models.CharField(max_length=255)

    city                = models.CharField(max_length=50)
    pincode             = models.CharField(max_length=50)

    is_active           = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' ' + self.city.capitalize() + ' ' + self.pincode


class Grade(models.Model):
    name   = models.CharField(max_length=255, unique=True)

    is_active           = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    user                 = models.OneToOneField(User, on_delete=models.CASCADE)

    # name                 = models.CharField(max_length=255)
    # username             = models.CharField(max_length=255)
    # password            = models.CharField(max_length=255)

    
    school               = models.ForeignKey(School, on_delete=models.CASCADE)
    grade                = models.ForeignKey(Grade, on_delete=models.CASCADE)

    is_active           = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' ' + self.school.name