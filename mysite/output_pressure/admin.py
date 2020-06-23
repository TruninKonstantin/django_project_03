from django.contrib import admin

# Register your models here.

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Group, Material, Results, PressureClass, Pressure, Standard


class GroupAdmin(ImportExportModelAdmin):
    pass


class StandardAdmin(ImportExportModelAdmin):
    pass


class MaterialAdmin(ImportExportModelAdmin):
    list_display = (
        'name', 'standard', 'group', 't_min', 't_max')


class PressureClassAdmin(ImportExportModelAdmin):
    pass


class PressureAdmin(ImportExportModelAdmin):
    list_display = (
        'name', 'group', 'pressure_class', 'pressure_m29', 'pressure_38', 'pressure_50', 'pressure_100',
        'pressure_150', 'pressure_200', 'pressure_250', 'pressure_300', 'pressure_325', 'pressure_350',
        'pressure_375', 'pressure_400', 'pressure_425',
    )


admin.site.register(Standard, StandardAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Pressure, PressureAdmin)
admin.site.register(PressureClass, PressureClassAdmin)
