import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, name, phone, **extra_fields):
        if not email:
            raise ValueError("You have not specified a valid e-mail address")
        
        if not name:
            raise ValueError("You have not specified a valid name")
        
        if not phone:
            raise ValueError("You have not specified a valid phone number")
        
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, email=None, password=None, name =None, phone=None, **extra_fields):
        extra_fields.setdefault('role', 'I')
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( email, password, name ,phone ,**extra_fields)
    
    def create_superuser(self, email=None, password=None, name=None, phone=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', 'A')
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user( email, password, name, phone, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('U', 'User'),
        ('I', '인턴'),
        ('E', '사원'),
        ('A', '관리자'),
    )
    ACTIVE_CHOICES = (
        ('W', 'Work'),
        ('R', 'Rest'),
        ('O', 'Off'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, null=False, unique=True)
    name = models.CharField(max_length=255 )
    avatar = models.ImageField(upload_to='uploads/avatars', blank=True, null=True)
    counts = models.IntegerField(default=0, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    active = models.CharField(max_length=1, default='O', choices=ACTIVE_CHOICES)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=1, default='I', choices=ROLE_CHOICES)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email