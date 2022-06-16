from django import forms
from careeradvice.models import CareerAdvice


class CareerAdviceForm(forms.ModelForm):
    class Meta:
        model = CareerAdvice
        fields = ['heading', 'text', 'category', 'tags']

