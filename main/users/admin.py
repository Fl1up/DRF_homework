
from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import TokenProxy

from main.users.models import User

# Register your models here.
admin.site.register(User)
