from django import forms
from .models import CV, EmpEducations, EmpSkills, EmpExperience, EmpLocations, EmpPhoneNumber
from django.forms import modelformset_factory


class CvForm(forms.ModelForm):
    class Meta:
        model = CV
        # List of input to make cv.
        fields = ("first_name", "last_name", "email", "gender", "picture", "interests")


class EmpEducationsForm(forms.ModelForm):
    class Meta:
        model = EmpEducations
        fields = ("education", "date")
        help_texts = {"date": "yyyy-mm-dd"}


class EmpSkillsForm(forms.ModelForm):
    class Meta:
        model = EmpSkills
        fields = ("skill", "grade")


class EmpExperienceForm(forms.ModelForm):
    class Meta:
        model = EmpExperience
        fields = ("experience", "start", "end")
        help_texts = {"start": "yyyy-mm-dd", "end": "yyyy-mm-dd"}


class EmpLocationsForm(forms.ModelForm):
    class Meta:
        model = EmpLocations
        fields = ("country",)


class EmpPhoneNumberForm(forms.ModelForm):
    class Meta:
        model = EmpPhoneNumber
        fields = ("phone_number",)


SkillFormset = modelformset_factory(
    model=EmpSkills,
    form=EmpSkillsForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)


ExperienceFormset = modelformset_factory(
    EmpExperience,
    form=EmpExperienceForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)

EducationsFormset = modelformset_factory(
    EmpEducations,
    form=EmpEducationsForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)

LocationsFormset = modelformset_factory(
    EmpLocations,
    form=EmpLocationsForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
    max_num=1,
)

PhoneNumberFormset = modelformset_factory(
    EmpPhoneNumber,
    form=EmpPhoneNumberForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)
