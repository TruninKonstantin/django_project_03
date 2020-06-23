from django.urls import path

from . import views

urlpatterns = [
    path('pressure_calculation/', views.ResultView.as_view(), name='output_pressure_calculation'),
    path('ajax/load-materials/', views.load_materials, name='ajax_load_materials'),
    path('ajax/load-groups/', views.load_groups, name='ajax_load_groups'),
    path('ajax/load-interpolated-pressure/', views.interpolate_pressure, name='ajax_load_interpolated_pressure'),
]