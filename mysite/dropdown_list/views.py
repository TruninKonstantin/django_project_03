from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import OutputPressureForm
from .models import OutputPressure, Material, Group


# Create your views here.


class PersonCreateView(CreateView):
    model = OutputPressure
    form_class = OutputPressureForm
    template_name = 'dropdown_list/name_model.html'
    success_url = reverse_lazy('person_changelist')

def load_materials(request):
    group_id = request.GET.get('group')
    if group_id == '':
        cities = Material.objects.order_by('name')
    else:
        cities = Material.objects.filter(group_id=group_id).order_by('name')
    return render(request, 'dropdown_list/material_dropdown_list_options.html', {'cities': cities})

def load_groups(request):
    material_id = request.GET.get('material')
    if material_id == '':
        countries = Group.objects.order_by('name')
        return render(request, 'dropdown_list/group_dropdown_list_options.html', {'countries': countries})
    else:

        field_name = 'group_id'
        material = Material.objects.get(id=material_id)
        field_object = Material._meta.get_field(field_name)
        group_id = getattr(material, field_object.attname)
        countries = Group.objects.filter(id=group_id).order_by('name')

        return render(request, 'dropdown_list/group_dropdown_one.html', {'countries': countries})
