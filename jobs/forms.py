from django import forms
from jobs.models import JobPost, Locations, JobApply, PhoneNumber, RequiredExperience, RequiredEducation, \
    RequiredSkills
from django.forms import modelformset_factory


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ("heading", "description", "gender",
                  "category", "job_type", "email", "salary", "tags")


class LocationsForm(forms.ModelForm):
    class Meta:
        model = Locations
        fields = ("country",)


class JobApplyForm(forms.ModelForm):
    class Meta:
        model = JobApply
        fields = ("note",)


class RequiredExperienceForm(forms.ModelForm):
    class Meta:
        model = RequiredExperience
        fields = ("experience",)


class RequiredEducationForm(forms.ModelForm):
    class Meta:
        model = RequiredEducation
        fields = ("education",)


class RequiredSkillsForm(forms.ModelForm):
    class Meta:
        model = RequiredSkills
        fields = ("skill",)


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ("phone_number",)


ExperienceFormset = modelformset_factory(
    RequiredExperience,
    form=RequiredExperienceForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)

EducationFormset = modelformset_factory(
    RequiredEducation,
    form=RequiredEducationForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)

SkillFormset = modelformset_factory(
    RequiredSkills,
    form=RequiredSkillsForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)

LocationsFormset = modelformset_factory(
    Locations,
    form=LocationsForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
    max_num=1,
)

PhoneNumberFormset = modelformset_factory(
    PhoneNumber,
    form=PhoneNumberForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)
