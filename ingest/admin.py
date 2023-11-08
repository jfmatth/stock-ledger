from django.contrib import admin

# Register your models here.
from .models import Rawcsv, Rawtransactions

admin.site.register(Rawcsv)
admin.site.register(Rawtransactions)