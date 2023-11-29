from django import forms

from decom.models import Fujian


class FujianForm(forms.ModelForm):
    class Meta:
        model = Fujian
        fields = ('file',)