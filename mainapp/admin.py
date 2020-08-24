from django.contrib import admin

# Register your models here.
from mainapp.models import Service, Masters

admin.site.register(Service)
admin.site.register(Masters)
