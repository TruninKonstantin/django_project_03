from django import forms

from .models import Results, Material, Standard


class ResultsForm(forms.ModelForm):
    temperature = forms.FloatField()
    # TODO add bar
    interpolated_pressure = forms.CharField()
    # labels = {
    #     "interpolated_pressure": "interpolated_pressure, bars"
    # }

    class Meta:
        model = Results
        fields = ('standard',
                  'group',
                  'material',
                  'pressure_class')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.order_by('name')
        self.fields['standard'].queryset = Standard.objects.order_by('name')
