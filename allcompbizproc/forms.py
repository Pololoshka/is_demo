from django import forms

from allcompbizproc.models import BusinessProcessModel


class BusinessProcessForm(forms.ModelForm):
    class Meta:
        model = BusinessProcessModel
        fields = []

    bp = forms.ModelChoiceField(
        queryset=BusinessProcessModel.objects.all(),
        to_field_name="process_id",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Не выбрано",
        label="Выберите бизнесс-процесс, который хотите запустить",
    )
