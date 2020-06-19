from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import OutputPressureForm
from .models import OutputPressure, Material, Group, Pressure


# Create your views here.


class PersonCreateView(CreateView):
    model = OutputPressure
    form_class = OutputPressureForm
    template_name = 'output_pressure/pressure_calculation.html'
    success_url = reverse_lazy('output_pressure_calculation')

def load_materials(request):
    group_id = request.GET.get('group')
    if group_id == '':
        materials = Material.objects.order_by('name')
    else:
        materials = Material.objects.filter(group_id=group_id).order_by('name')
    return render(request, 'output_pressure/material_dropdown_list_options.html', {'materials': materials})

def load_groups(request):
    material_id = request.GET.get('material')
    if material_id == '':
        groups = Group.objects.order_by('name')
        return render(request, 'output_pressure/group_dropdown_list_options.html', {'groups': groups})
    else:

        field_name = 'group_id'
        material = Material.objects.get(id=material_id)
        field_object = Material._meta.get_field(field_name)
        group_id = getattr(material, field_object.attname)
        groups = Group.objects.filter(id=group_id).order_by('name')

        return render(request, 'output_pressure/group_dropdown_one.html', {'groups': groups})


def load_temperatures_pressures(request):
    material_class_id = request.GET.get('material_class')
    group_id = request.GET.get('group')

    pressures = Pressure.objects.filter(group_id=group_id).filter(material_class_id=material_class_id).order_by('name')
    #
    # field_name = 'temperature_50'
    # obj = Pressure.objects.filter(group_id=group_id).filter(material_class_id=material_class_id)
    # field_object = Pressure._meta.get_field(field_name)
    # field_value = getattr(obj, field_object.attname)
    print([p.temperature_50 for p in pressures])
    print([p.temperature_100 for p in pressures])
    print([p.temperature_150 for p in pressures])

    some_values = []
    some_values.append([p.temperature_50 for p in pressures])
    some_values.append([p.temperature_100 for p in pressures])
    some_values.append([p.temperature_150 for p in pressures])


    return render(request, 'output_pressure/temperatures_pressures_dropdown_list_options.html', {'pressures': some_values})