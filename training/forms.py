from django import forms
from .models import Training


class TrainingForm(forms.ModelForm):
    price = forms.DecimalField(label="Price")

    class Meta:
        model = Training
        fields = ("title", "email", "country", "description", "price", "category", "tags", "phone_number")
        help_texts = {"tags": None}
