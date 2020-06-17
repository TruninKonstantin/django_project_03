from django.shortcuts import render

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import PersonForm

from .models import Person, City, Country


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'dropdown_list/name_model.html'
    success_url = reverse_lazy('person_changelist')

def load_cities(request):
    country_id = request.GET.get('country')
    if country_id == '':
        cities = City.objects.order_by('name')
    else:
        cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'dropdown_list/city_dropdown_list_options.html', {'cities': cities})

def load_countries(request):
    city_id = request.GET.get('city')
    if city_id == '':
        countries = Country.objects.order_by('name')
        return render(request, 'dropdown_list/country_dropdown_list_options.html', {'countries': countries})
    else:

        field_name = 'country_id'
        city = City.objects.get(id=city_id)
        field_object = City._meta.get_field(field_name)
        country_id = getattr(city, field_object.attname)
        countries = Country.objects.filter(id=country_id).order_by('name')

        return render(request, 'dropdown_list/country_dropdown_one.html', {'countries': countries})
