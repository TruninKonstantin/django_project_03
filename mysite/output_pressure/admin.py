from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Group, Material, OutputPressure, MaterialClass, Pressure, Standard

admin.site.register(Standard)
admin.site.register(Group)
admin.site.register(Material)
admin.site.register(Pressure)
admin.site.register(MaterialClass)
admin.site.register(OutputPressure)
