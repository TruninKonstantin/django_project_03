from django import forms

from .models import Results, Material, Standard


class ResultsForm(forms.ModelForm):
    input_temperature = forms.FloatField()
    # TODO add bar
    calculated_value = forms.CharField()

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
