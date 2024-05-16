from django import forms
from .models import Aquarium

class AquariumForm(forms.ModelForm):
    class Meta:
        model = Aquarium
        fields = ['name', 'x', 'y', 'z', 'light', 'pump', 'heater', 'filters']
        labels = {
            'name': 'Nazwa',
            'x': 'Szerokość (cm)',
            'y': 'Wysokość (cm)',
            'z': 'Głębokość (cm)',
            'light': 'Oświetlenie',
            'pump': 'Pompa',
            'heater': 'Grzałka',
            'filters': 'Filtry',
        }
        widgets = {
            'light': forms.Select(attrs={'class': 'input'}),
            'pump': forms.Select(attrs={'class': 'input'}),
            'heater': forms.Select(attrs={'class': 'input'}),
            'filters': forms.CheckboxSelectMultiple(attrs={'class': 'input'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super(AquariumForm, self).__init__(*args, **kwargs)
        self.user = user
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
    
    def clean_filters(self):
        filters = self.cleaned_data.get('filters')
        if not filters:
            raise forms.ValidationError('Wybierz przynajmniej jeden filtr.')
        return filters