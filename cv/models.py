from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from generics.models import Experiences, Educations, Skills, Countries, Grades


choice = (("Male", "Male"), ("Female", "Female"))


# Create your models here.
class CV(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    first_name = models.CharField(max_length=256, blank=False)
    last_name = models.CharField(max_length=256, blank=False)
    email = models.EmailField(blank=False)
    picture = models.ImageField(upload_to="cv/", blank=False)
    gender = models.CharField(blank=False, choices=choice, max_length=15, default="Male")
    interests = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    def get_url(self):
        return reverse('cv:preview', args=[self.id])


class EmpExperience(models.Model):
    experience = models.ForeignKey(Experiences, on_delete=models.CASCADE, blank=False, unique=False)
    start = models.DateField(blank=False)
    end = models.DateField(blank=False)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, blank=False)


class EmpEducations(models.Model):
    education = models.ForeignKey(Educations, on_delete=models.CASCADE, blank=False, unique=False)
    date = models.DateField(blank=False)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, blank=False)


class EmpSkills(models.Model):
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, blank=False)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, blank=False, unique=False)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, blank=False)


class EmpLocations(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, blank=False)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, blank=False)


class EmpPhoneNumber(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, blank=False)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
