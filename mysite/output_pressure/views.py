from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .constants.constants import Constants
from .forms import ResultsForm
from .models import Results, Material, Group, Pressure


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
        material_obj = Material.objects.get(id=material_id)
        group_id = get_field_value(field_name, Material, material_obj)

        groups = Group.objects.filter(id=group_id).order_by('name')
        return render(request, 'output_pressure/group_dropdown_one.html', {'groups': groups})

# TODO there is no update of the fields on first material choose
def interpolate_pressure(request):
    pressure_class_id = request.GET.get('pressure_class')
    group_id = request.GET.get('group')
    input_temperature = request.GET.get('input_temperature')

    pressures = Pressure.objects.filter(group_id=group_id).filter(pressure_class_id=pressure_class_id).order_by('name')
    pressure_object = pressures.first()
    temperature_field_names = Constants.TEMPERATURE_FIELD_NAMES.value

    all_fields = []
    for field_name in temperature_field_names:
        all_fields.append(pressure_object._meta.get_field(field_name))

    field_temperature_lower_input = pressure_object._meta.get_field(Constants.LOWEST_TEMPERATURE_FIELD_NAME.value)
    field_temperature_higher_input = pressure_object._meta.get_field(Constants.HIGHEST_TEMPERATURE_FIELD_NAME.value)

    for field in all_fields:
        if get_temperature_from_field_name(field) < float(input_temperature):
            field_temperature_lower_input = field
        if get_temperature_from_field_name(field) > float(input_temperature):
            field_temperature_higher_input = field
            break

    interpolated_pressure = interpolation(input_temperature, field_temperature_lower_input,
                                          field_temperature_higher_input,
                                          Pressure, pressure_object)

    return render(request, 'output_pressure/interpolated_pressure.html',
                  {'pressure': interpolated_pressure})


def interpolation(input_temperature, field_temperature_lower_input, field_temperature_higher_input, MyModel,
                  my_model_obj):
    if field_temperature_lower_input.name == field_temperature_higher_input.name:
        output_value = float(get_field_value(field_temperature_lower_input.name, MyModel, my_model_obj))
    else:
        x_one = float(field_temperature_lower_input.name.split(Constants.STR_PART_PRESSURE_FIELD.value)[
                          Constants.NUMBER_POSITION_AFTER_SPLIT.value])
        y_one = float(get_field_value(field_temperature_lower_input.name, MyModel, my_model_obj))

        x_two = float(field_temperature_higher_input.name.split(Constants.STR_PART_PRESSURE_FIELD.value)[
                          Constants.NUMBER_POSITION_AFTER_SPLIT.value])
        y_two = float(get_field_value(field_temperature_higher_input.name, MyModel, my_model_obj))

        input_temperature = float(input_temperature)

        output_value = (y_two - y_one) / (x_two - x_one) * (input_temperature - x_one) + y_one
    return round(output_value, Constants.NUMBER_OF_DECIMALS.value)


def get_field_value(field_name, MyModel, my_model_obj):
    field_object = MyModel._meta.get_field(field_name)
    return field_object.value_from_object(my_model_obj)


def get_temperature_from_field_name(field):
    temperature = field.name.split(Constants.STR_PART_PRESSURE_FIELD.value)[Constants.NUMBER_POSITION_AFTER_SPLIT.value]
    if Constants.STR_FOR_MINUS.value in temperature:
        temperature = temperature.split(Constants.STR_FOR_MINUS.value)[Constants.NUMBER_POSITION_AFTER_SPLIT.value]
    return float(temperature)
