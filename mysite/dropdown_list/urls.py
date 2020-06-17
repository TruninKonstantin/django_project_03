from django.urls import path

from . import views

urlpatterns = [
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-countries/', views.load_countries, name='ajax_load_countries'),
    path('name_model/', views.PersonCreateView.as_view(), name='person_changelist'),

]