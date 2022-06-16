from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse

Gender = (
    ('male', "Male"),
    ('female', "Female"),

)


class Profile(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    # Holds the user's bio
    bio = models.CharField(max_length=255, blank=True)
    # Holds the user's photo
    photo = models.ImageField(upload_to="users_profile_photo/", blank=True,
                              default="users_profile_photo/default_profile_photo.jpg")
    # Holds the user's phone number
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)

    def pic(self):
        return self.photo

    def get_user_id(self):
        return reverse('account:show_profile', args=[self.pk])


class Company(models.Model):
    # If the company was deleted the profile will be deleted as well.
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True, related_name='company')
    # Holds the user's website
    website = models.URLField(max_length=200)
    # Holds the location
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.website


class Employee(models.Model):
    # If the employee was deleted the profile will be deleted as well.
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True, related_name='employee')
    # Holds the user's date of birth
    date_of_birth = models.DateField()
    # Holds the user's gender
    gender = models.CharField(choices=Gender, max_length=6)

    def __str__(self):
        return self.gender

    def name(self):
        return f"{self.user.username}'s Profile"
