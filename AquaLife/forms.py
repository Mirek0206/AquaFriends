from django import forms
from django_select2.forms import Select2MultipleWidget
from .models import Aquarium, Fish

class AquariumForm(forms.ModelForm):
    class Meta:
        model = Aquarium
        fields = ['name', 'x', 'y', 'z', 'light', 'pump', 'heater', 'filters', 'decorators']
        labels = {
            'name': 'Nazwa',
            'x': 'Szerokość (cm)',
            'y': 'Wysokość (cm)',
            'z': 'Głębokość (cm)',
            'light': 'Oświetlenie',
            'pump': 'Pompa',
            'heater': 'Grzałka',
            'filters': 'Filtry',
            'decorators': 'Dekoracje',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'required': True}),
            'x': forms.NumberInput(attrs={'class': 'input', 'required': True}),
            'y': forms.NumberInput(attrs={'class': 'input', 'required': True}),
            'z': forms.NumberInput(attrs={'class': 'input', 'required': True}),
            'light': forms.Select(attrs={'class': 'input', 'required': True}),
            'pump': forms.Select(attrs={'class': 'input', 'required': True}),
            'heater': forms.Select(attrs={'class': 'input', 'required': True}),
            'filters': Select2MultipleWidget(attrs={'class': 'input'}),
            'decorators': Select2MultipleWidget(attrs={'class': 'input'}),
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

class FishForm(forms.ModelForm):
    class Meta:
        model = Fish
        fields = ['name', 'age', 'species']
        labels = {
            'name': 'Imię',
            'age': 'Wiek [msc]',
            'species': 'Gatunek',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'required': True}),
            'age': forms.NumberInput(attrs={'class': 'input', 'required': True}),
            'species': forms.Select(attrs={'class': 'input', 'required': True}),
        }
