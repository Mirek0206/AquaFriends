from django import forms
from .models import WaterParameter

class WaterParameterForm(forms.ModelForm):
    class Meta:
        model = WaterParameter
        fields = ['no2', 'no3', 'gh', 'kh', 'ph']
        labels = {
            'no2': 'NO2',
            'no3': 'NO3',
            'gh': 'GH',
            'kh': 'KH',
            'ph': 'pH'
        }
        widgets = {
            'no2': forms.NumberInput(attrs={'class': 'input'}),
            'no3': forms.NumberInput(attrs={'class': 'input'}),
            'gh': forms.NumberInput(attrs={'class': 'input'}),
            'kh': forms.NumberInput(attrs={'class': 'input'}),
            'ph': forms.NumberInput(attrs={'class': 'input'}),
        }

    def __init__(self, *args, **kwargs):
        super(WaterParameterForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
