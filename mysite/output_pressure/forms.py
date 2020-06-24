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
                                    # 'style': 'background-color: #FF0000;',
                                    'class': 'color_white',
                                    'rows':4,
                                }
                            ))

    class Meta:
        model = Results
        fields = ('standard',
                  # 'group',
                  'material',
                  'pressure_class')
        # labels = {
        #     "interpolated_pressure": "interpolated_pressure, bars"
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.order_by('name')
        self.fields['standard'].queryset = Standard.objects.order_by('name')
