from django.contrib.auth import get_user_model
from .models import *
from django import forms
from django.forms.widgets import SelectDateWidget
from datetime import datetime

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """A class that represents a registration form for the Django User model."""
    # Holds the password
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    # A field to renter the password and match it with the entered password to make sure the password is what the
    # user meant it to be and they didn't make any typos
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        """A class to describe aspects of this model (self-referencing)."""
        # The model this form class represents
        model = User
        # The form's fields
        fields = ("username", "email", "password", "confirm_password", "bio", "photo", "phone_number")
        # Remove the username validation text
        help_texts = {"username": None}

    def clean_confirm_password(self):
        """Validates and makes sure that the 2 password fields match."""
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('confirm_password')
        SpecialSym = ['$', '@', '#', '%']

        # Do passwords match ?
        if password != password_confirm:
            # Raise an exception
            raise forms.ValidationError("Passwords don't match")

        if len(password) < 8:
            # Raise an exception
            raise forms.ValidationError("password should be at least 8 character")

        if len(password) > 20:
            # Raise an exception
            raise forms.ValidationError("password should not be greater than 16 character")

        if not any(char.isdigit() for char in password):
            # Raise an exception
            raise forms.ValidationError("Password should have at least one numeral")

        if not any(char.isupper() for char in password):
            # Raise an exception
            raise forms.ValidationError("Password should have at least one uppercase letter")

        if not any(char.islower() for char in password):
            # Raise an exception
            raise forms.ValidationError("Password should have at least one lowercase letter")

        if not any(char in SpecialSym for char in password):
            raise forms.ValidationError("interview test")

        return cleaned_data


class EmployeeForm(forms.ModelForm):
    """A class that represents a registration form for the Employee model."""
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1970, datetime.today().year + 1, 1)))

    class Meta:
        model = Employee
        fields = ("date_of_birth", "gender")


class CompanyForm(forms.ModelForm):
    """A class that represents a registration form for the Company model."""

    class Meta:
        model = Company
        fields = ("website", "location")





class ProfileEditForm(forms.ModelForm):
    """A class that represents a form to edit user's profile."""

    class Meta:
        model = Profile
        fields = ("username", "photo", "email", "bio", "phone_number")
        help_texts = {"username": None}


class CompanyEditForm(forms.ModelForm):
    """A class that represents a form to edit Company's profile."""
    class Meta:
        model = Company
        fields = ("website", "location")


class EmployeeEditForm(forms.ModelForm):
    """A class that represents a form to edit Employee's profile."""
    class Meta:
        model = Employee
        fields = ("date_of_birth", "gender")
