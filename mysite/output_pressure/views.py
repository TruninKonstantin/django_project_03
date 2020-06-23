from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ResultsForm
from .models import Results, Material, Group, Pressure


# Create your views here.

class ResultView(CreateView):
    model = Results
    form_class = ResultsForm
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
    pressure_class_id = request.GET.get('pressure_class')
    group_id = request.GET.get('group')
    input_temperature = request.GET.get('input_temperature')

    pressures = Pressure.objects.filter(group_id=group_id).filter(pressure_class_id=pressure_class_id).order_by('name')

    pressure_object = pressures.first()
    temperature_field_names = ['pressure_m29', 'pressure_38', 'pressure_50', 'pressure_100',
        'pressure_150', 'pressure_200', 'pressure_250', 'pressure_300', 'pressure_325', 'pressure_350',
        'pressure_375', 'pressure_400', 'pressure_425']

    # all_fields = pressure_object._meta.get_fields()
    all_fields = []
    for field_name in temperature_field_names:
        all_fields.append(pressure_object._meta.get_field(field_name))




    field_temperature_lower_input = pressure_object._meta.get_field("pressure_m29")
    field_temperature_higher_input = pressure_object._meta.get_field("pressure_425")

    for field in all_fields:
        if "pressure_" in field.name:
            if get_temperature_from_field_name(field) < float(input_temperature):
                field_temperature_lower_input = field
            if get_temperature_from_field_name(field) > float(input_temperature):
                field_temperature_higher_input = field
                break

    # print(field_temperature_lower_input.name)
    # print(get_field_value(field_temperature_lower_input.name, Pressure, pressure_object))
    # print(field_temperature_higher_input.name)
    # print(get_field_value(field_temperature_higher_input.name, Pressure, pressure_object))
    # print(interpolation(input_temperature, field_temperature_lower_input, field_temperature_higher_input, Pressure, pressure_object))

    some_values = interpolation(input_temperature, field_temperature_lower_input, field_temperature_higher_input,
                                Pressure, pressure_object)

    return render(request, 'output_pressure/temperatures_pressures_dropdown_list_options.html',
                  {'pressures': some_values})


def interpolation(input_temperature, field_temperature_lower_input, field_temperature_higher_input, MyModel,
                  my_model_obj):
    if field_temperature_lower_input.name == field_temperature_higher_input.name:
        output_value = float(get_field_value(field_temperature_lower_input.name, MyModel, my_model_obj))
    else:
        x_one = float(field_temperature_lower_input.name.split("pressure_")[1])
        y_one = float(get_field_value(field_temperature_lower_input.name, MyModel, my_model_obj))

        x_two = float(field_temperature_higher_input.name.split("pressure_")[1])
        y_two = float(get_field_value(field_temperature_higher_input.name, MyModel, my_model_obj))

        input_temperature = float(input_temperature)

        output_value = (y_two - y_one) / (x_two - x_one) * (input_temperature - x_one) + y_one
    return round(output_value, 3)


def get_field_value(field_name, MyModel, my_model_obj):
    field_object = MyModel._meta.get_field(field_name)
    return field_object.value_from_object(my_model_obj)

def get_temperature_from_field_name(field):
    temperature = field.name.split("pressure_")[1]
    if "m" in temperature:
        temperature = temperature.split("m")[1]
    return float(temperature)
