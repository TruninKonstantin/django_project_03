from django.urls import path

from . import views

urlpatterns = [
    path('pressure_calculation/', views.ResultView.as_view(), name='output_pressure_calculation'),
    path('ajax/load-materials/', views.load_materials_on_standard_change, name='ajax_load_materials'),
    path('ajax/load-groups/', views.load_groups_on_material_changed, name='ajax_load_groups'),
    path('ajax/load-standards/', views.load_standards_on_material_changed, name='ajax_load_standards'),
    path('ajax/re-load-materials/', views.reload_materials, name='ajax_re_load_materials'),
    path('ajax/load-interpolated-pressure/', views.interpolate_pressure, name='ajax_load_interpolated_pressure'),
]