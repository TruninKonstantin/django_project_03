from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Group, Material, OutputPressure

admin.site.register(Group)
admin.site.register(Material)
admin.site.register(OutputPressure)