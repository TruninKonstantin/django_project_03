from django import forms

from .models import Results


class ResultsForm(forms.ModelForm):
    input_temperature = forms.FloatField()
    calculated_value = forms.CharField()

    class Meta:
        model = Results
        fields = ('standard',
                  'group',
                  'material',
                  'pressure_class')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
