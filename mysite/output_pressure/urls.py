from django.urls import path

from . import views

urlpatterns = [
    path('ajax/load-materials/', views.load_materials, name='ajax_load_materials'),
    path('ajax/load-groups/', views.load_groups, name='ajax_load_groups'),
    path('ajax/load-temperatures-pressures/', views.load_temperatures_pressures, name='ajax_load_temperatures_pressures'),
    path('pressure_calculation/', views.ResultView.as_view(), name='output_pressure_calculation'),

]