from django.urls import path

from . import views

urlpatterns = [
    path('ajax/load-cities/', views.load_materials, name='ajax_load_cities'),
    path('ajax/load-countries/', views.load_groups, name='ajax_load_countries'),
    path('name_model/', views.PersonCreateView.as_view(), name='person_changelist'),

]