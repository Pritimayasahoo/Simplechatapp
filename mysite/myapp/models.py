from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Room(models.Model):
    roomname=models.CharField(max_length=1000,unique=True)
    roompassword=models.CharField(max_length=1000,default=123)

class Message(models.Model):
    message=models.CharField(max_length=10000,blank=True)    
    roomname=models.CharField(max_length=1000,blank=True)
    posttime=models.DateField(default=datetime.now)
    user=models.CharField(max_length=100)    

class Account(models.Model):
    email=models.EmailField(unique=True)    
    name=models.CharField(max_length=1000)

    def __str__(self):
        return self.name