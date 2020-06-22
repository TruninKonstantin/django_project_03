from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import OutputPressureForm
from .models import OutputPressure, Material, Group, Pressure


# Create your views here.

# TODO rename
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
    input_temperature = request.GET.get('input_temperature')

    pressures = Pressure.objects.filter(group_id=group_id).filter(material_class_id=material_class_id).order_by('name')

    some_values = []
    some_values.append([p.temperature_50 for p in pressures])
    some_values.append([p.temperature_100 for p in pressures])
    some_values.append([p.temperature_150 for p in pressures])

    p = pressures.first()
    all_fields = p._meta.get_fields()
    field_temperature_lower_input = p._meta.get_field("temperature_50")
    field_temperature_higher_input = p._meta.get_field("temperature_150")

    for field in all_fields:
        if "temperature_" in field.name:
            if float(field.name.split("temperature_")[1]) < float(input_temperature):
                field_temperature_lower_input = field
            if float(field.name.split("temperature_")[1]) > float(input_temperature):
                field_temperature_higher_input = field
                break

    print(field_temperature_lower_input.name)
    print(get_field_value(field_temperature_lower_input.name, Pressure, p))
    print(field_temperature_higher_input.name)
    print(get_field_value(field_temperature_higher_input.name, Pressure, p))
    print(interpolation(input_temperature, field_temperature_lower_input, field_temperature_higher_input, Pressure, p))

    some_values = interpolation(input_temperature, field_temperature_lower_input, field_temperature_higher_input,
                                Pressure, p)

    return render(request, 'output_pressure/temperatures_pressures_dropdown_list_options.html',
                  {'pressures': some_values})


def interpolation(input_temperature, field_temperature_lower_input, field_temperature_higher_input, MyModel,
                  my_model_obj):
    if field_temperature_lower_input.name == field_temperature_higher_input.name:
        output_value = float(get_field_value(field_temperature_lower_input.name, MyModel, my_model_obj))
    else:
        x_one = float(field_temperature_lower_input.name.split("temperature_")[1])
        y_one = float(get_field_value(field_temperature_lower_input.name, MyModel, my_model_obj))

        x_two = float(field_temperature_higher_input.name.split("temperature_")[1])
        y_two = float(get_field_value(field_temperature_higher_input.name, MyModel, my_model_obj))

        input_temperature = float(input_temperature)

        output_value = (y_two - y_one) / (x_two - x_one) * (input_temperature - x_one) + y_one
    return round(output_value, 3)


def get_field_value(field_name, MyModel, my_model_obj):
    field_object = MyModel._meta.get_field(field_name)
    return field_object.value_from_object(my_model_obj)
