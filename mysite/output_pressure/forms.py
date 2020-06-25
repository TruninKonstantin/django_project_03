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

from django import forms

from .models import Results, Material, Standard


class ResultsForm(forms.ModelForm):
    temperature = forms.FloatField()
    interpolated_pressure = forms.CharField(
        label="Interpolated pressure, bar"
    )
    table = forms.CharField()
    notes = forms.CharField(required=False,
                            widget=forms.Textarea(
                                attrs={
                                    'class': 'color_white',
                                    'rows':4,
                                }
                            ))

    class Meta:
        model = Results
        fields = ('standard',
                  'material',
                  'pressure_class')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.order_by('name')
        self.fields['standard'].queryset = Standard.objects.order_by('name')
