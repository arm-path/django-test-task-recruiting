from django import forms

from django_applications.models import Recruit, Sith


class RecruitForm(forms.ModelForm):
    """ Форма представления Рекрута """

    class Meta:
        model = Recruit
        fields = ['name', 'planet', 'age', 'email', 'orden_code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'planet': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'max': 100}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'orden_code': forms.Select(attrs={'class': 'form-select'}),
        }


class SithChoicesForm(forms.Form):
    """ Форма представления выбора ситха """
    sith = forms.ModelChoiceField(queryset=Sith.objects.all(),
                                  label='Ситх',
                                  widget=forms.Select(attrs={'class': 'form-select'}))
