from django.urls import path

from . import views

urlpatterns = [
    path('ajax/load-materials/', views.load_materials, name='ajax_load_materials'),
    path('ajax/load-groups/', views.load_groups, name='ajax_load_groups'),
    path('pressure_calculation/', views.PersonCreateView.as_view(), name='output_pressure_calculation'),

]