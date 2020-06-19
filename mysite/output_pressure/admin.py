from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Group, Material, OutputPressure, MaterialClass, Pressure, Standard

class PressureAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'material_class', 'temperature_50', 'temperature_100', 'temperature_150')

admin.site.register(Standard)
admin.site.register(Group)
admin.site.register(Material)
admin.site.register(Pressure, PressureAdmin)
admin.site.register(MaterialClass)
admin.site.register(OutputPressure)


