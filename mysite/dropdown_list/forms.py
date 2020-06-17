from django import forms

from .models import OutputPressure, Material


class OutputPressureForm(forms.ModelForm):
    calculated_value = forms.CharField()

    class Meta:
        model = OutputPressure
        fields = ('group', 'material')




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'group' in self.data:
            try:
                group_id = int(self.data.get('group'))
                self.fields['material'].queryset = Material.objects.filter(group_id=group_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty material queryset
        elif self.instance.pk:
            self.fields['material'].queryset = self.instance.group.material_set.order_by('name')