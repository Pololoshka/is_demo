from django import forms

from duplicatefinder.handlers import MODELS_DATA


class ChoiceModelForm(forms.Form):
    model = forms.ChoiceField(choices=tuple(((key, value['field_name']) for key, value in MODELS_DATA.items())))
