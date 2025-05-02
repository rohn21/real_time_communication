from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

GENDER_CHOICE = [
        ('male', 'MALE'),
        ('female', 'FEMALE'),
]

class User(AbstractUser):
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(_('email address'), unique = True)
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)