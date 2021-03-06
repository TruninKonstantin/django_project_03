# Links to files:
#
# * [[admin.py]]
# * [[apps.py]]
# * [[forms.py]]
# * [[models.py]]
# * [[tests.py]]
# * [[urls.py]]
# * [[views.py]]
# * [[app.js]]
# * [[constants.py]]

from django.contrib import admin
# Class for implementation of import-export feature
from import_export.admin import ImportExportModelAdmin

from .constants.constants import Constants
from .models import Group, Material, PressureClass, Pressure, Standard


class GroupAdmin(ImportExportModelAdmin):
    pass


class StandardAdmin(ImportExportModelAdmin):
    pass


class MaterialAdmin(ImportExportModelAdmin):
    # Fields that will be shown on admin page
    list_display = (
        'name', 'standard', 'group', 't_min', 't_max')


class PressureClassAdmin(ImportExportModelAdmin):
    pass


class PressureAdmin(ImportExportModelAdmin):
    # Fields that will be shown on admin page
    list_display = (
        'name', 'group', 'pressure_class',
    )

    list_from_tuple = list(list_display)
    for elem in Constants.TEMPERATURE_FIELD_NAMES.value:
        list_from_tuple.append(elem)
    list_display = tuple(list_from_tuple)


admin.site.register(Standard, StandardAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Pressure, PressureAdmin)
admin.site.register(PressureClass, PressureClassAdmin)
