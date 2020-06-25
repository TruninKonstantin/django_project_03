# Links to files:
#
# * [[admin.py]]
# * [[apps.py]]
# * [[forms.py]]
# * [[models.py]]
# * [[tests.py]]
# * [[urls.py]]
# * [[views.py]]
# * [[app.js]]
# * [[constants.py]]

# All the views for our Pressure calculation application
# Currently we support the only one views:
#
# 1. **Home** - The main view for Pressure calculation (jump to section in [[views.py#home]] )


from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

# defined in [[constants.py]]
from .constants.constants import Constants
# defined in [[forms.py]]
from .forms import ResultsForm
# defined in [[models.py]]
from .models import Results, Material, Group, Pressure, Standard


# === home ===
class ResultView(CreateView):
    model = Results
    form_class = ResultsForm
    template_name = 'output_pressure/pressure_calculation.html'
    success_url = reverse_lazy('output_pressure_calculation')


# *  Returns list of all Materials from DB.
# *  Ajax request.
# *  Html response.
def reload_materials(request):
    materials = Material.objects.order_by('name')
    return render(request, 'output_pressure/material_dropdown_list_options.html', {'materials': materials})


# *  Updates the list of Materials on Standard change.
# *  Ajax request.
# *  Html response.
def load_materials_on_standard_change(request):
    standard_id = request.GET.get('standard')
    if standard_id == '':
        materials = Material.objects.order_by('name')
    else:
        materials = Material.objects.filter(standard_id=standard_id).order_by('name')
    return render(request, 'output_pressure/material_dropdown_list_options.html', {'materials': materials})


# *  Updates the list of Groups on Standard change.
# *  Ajax request.
# *  Html response.
def load_groups_on_material_changed(request):
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


# *  Updates the list of Standards on Material change.
# *  Ajax request.
# *  Html response.
def load_standards_on_material_changed(request):
    material_id = request.GET.get('material')
    if material_id == '':
        standards = Standard.objects.order_by('name')
        return render(request, 'output_pressure/standard_dropdown_list_options.html', {'standards': standards})
    else:

        field_name = 'standard_id'
        material_obj = Material.objects.get(id=material_id)
        standard_id = get_field_value(field_name, Material, material_obj)

        standards = Standard.objects.filter(id=standard_id).order_by('name')
        return render(request, 'output_pressure/standard_dropdown_one.html', {'standards': standards})


# * Returns interpolated value of pressure to home view.
# * Ajax request.
# * Json response.
def interpolate_pressure(request):
    pressure_class_id = request.GET.get('pressure_class')
    material_id = request.GET.get('material')
    input_temperature = request.GET.get('input_temperature')

    field_name = 'group_id'
    material_obj = Material.objects.get(id=material_id)
    group_id = get_field_value(field_name, Material, material_obj)

    pressures = Pressure.objects.filter(group_id=group_id).filter(pressure_class_id=pressure_class_id).order_by('name')
    pressure_object = pressures.first()
    temperature_field_names = Constants.TEMPERATURE_FIELD_NAMES.value

    all_fields = []
    for field_name in temperature_field_names:
        all_fields.append(pressure_object._meta.get_field(field_name))

    field_temperature_lower_input = pressure_object._meta.get_field(Constants.LOWEST_TEMPERATURE_FIELD_NAME.value)
    field_temperature_higher_input = pressure_object._meta.get_field(Constants.HIGHEST_TEMPERATURE_FIELD_NAME.value)

    for field in all_fields:
        if get_temperature_from_field_name(field) <= float(input_temperature):
            field_temperature_lower_input = field
        if get_temperature_from_field_name(field) >= float(input_temperature):
            field_temperature_higher_input = field
            break

    interpolated_pressure = interpolation(input_temperature, field_temperature_lower_input,
                                          field_temperature_higher_input,
                                          Pressure, pressure_object)

    data = {'interpolated_pressure': interpolated_pressure}
    return JsonResponse(data)


# * Updates the Table field.
# * Ajax request.
# * Json response.
def update_table(request):
    material_id = request.GET.get('material')

    field_name = 'group_id'
    material_obj = Material.objects.get(id=material_id)
    group_id = get_field_value(field_name, Material, material_obj)

    group_obj = Group.objects.get(id=group_id)
    group = get_field_value("name", Group, group_obj)
    str_table = "Table 2-" + str(group)
    data = {'str_table': str_table}

    return JsonResponse(data)


# * Updates the Notes field.
# * Ajax request.
# * Json response.
def update_notes(request):
    material_id = request.GET.get('material')
    temperature = float(request.GET.get('temperature_value'))

    material_obj = Material.objects.get(id=material_id)
    material_minimum_temperature = get_field_value("t_min", Material, material_obj)
    material_maximum_temperature = get_field_value("t_max", Material, material_obj)

    if material_minimum_temperature <= temperature <= material_maximum_temperature:
        str_note = "\nYou are inside material temperature range"
        textarea_class = "color_white"

    else:
        str_note = "\nYou are outside material temperature range"
        textarea_class = "color_red"

    str_material_temperatures = ("Material minimum temperature ="
                                 + str(material_minimum_temperature)
                                 + "\nMaterial maximun temperature ="
                                 + str(material_maximum_temperature))

    str_temperatures = (str_material_temperatures + str_note)

    data = {'str_temperatures': str_temperatures, 'textarea_class': textarea_class}

    return JsonResponse(data)


# * Returns interpolated pressure.
# * inputs:     input_temperature  -- temperature from view,
#               field_temperature_lower_input  -- field with the temperature lower than input_temperature,
#               field_temperature_higher_input -- field with the temperature higher than input_temperature,
#               MyModel -- Model of the field,
#               my_model_obj -- Object of the field,
# * output:     interpolated_pressure
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


# * Returns field value.
# * inputs:   field_name -- field name,
#           MyModel -- Model of the field,
#           my_model_obj -- Object of the field,
# * output:   field_value
def get_field_value(field_name, MyModel, my_model_obj):
    field_object = MyModel._meta.get_field(field_name)
    return field_object.value_from_object(my_model_obj)


# * Returns temperature from field.
# * inputs:   field -- field,
# * output:   temperature
def get_temperature_from_field_name(field):
    temperature = field.name.split(Constants.STR_PART_PRESSURE_FIELD.value)[Constants.NUMBER_POSITION_AFTER_SPLIT.value]
    if Constants.STR_FOR_MINUS.value in temperature:
        temperature = temperature.split(Constants.STR_FOR_MINUS.value)[Constants.NUMBER_POSITION_AFTER_SPLIT.value]
    return float(temperature)
