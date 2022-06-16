from django.conf import settings
from taggit.managers import TaggableManager
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from generics.models import *


# Create your models here.
class JobPost(models.Model):
    # A foreign key to the user when the user is deleted the corresponding threads are deleted as well
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="jobpost_created", on_delete=models.CASCADE)
    # The review's title
    heading = models.CharField(max_length=110)
    # A field to make SEO friendly links
    slug = models.SlugField(max_length=110)
    # An opening describes what this thread is about
    description = models.TextField()
    # The time and date the review was posted and it's added automatically
    created = models.DateTimeField(auto_now_add=True)
    # Updates the time when the thread is updated
    updated = models.TimeField(auto_now_add=True)
    # Tags to mark the post
    tags = TaggableManager()
    gender_choices = (('male', 'Male'), ('female', 'Female'))
    gender = models.CharField(choices=gender_choices, max_length=7)
    # poster email
    email = models.EmailField()
    job_type_choices = (('full_time', 'Full_Time'), ('half_time', 'Half_Time'))
    job_type = models.CharField(choices=job_type_choices, max_length=10)
    salary = models.DecimalField(decimal_places=2, max_digits=8)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)

    def get_absolute_url(self):
        """Returns a jobpost object URL"""
        # Build and return a unique and SEO friendly URL for a Thread object
        return reverse('jobs:job_details', args=[self.id])

    def edit_url(self):
        return reverse('jobs:job_edit', args=[self.id])

    def delete_url(self):
        return reverse('jobs:job_delete', args=[self.id])

    def apply_url(self):
        return reverse('jobs:add_apply', args=[self.id])

    def applies_url(self):
        return reverse('jobs:show_applies', args=[self.id])

    def __str__(self):
        return self.heading


class Locations(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, blank=False)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, blank=False)

    def delete_url(self):
        return reverse('jobs:job_delete', args=[self.id])


class JobApply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, blank=False)
    note = models.TextField()
    evaluation = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("jobs:apply_details", args=[self.id])

    def get_job_url(self):
        return reverse("jobs:job_details", args=[self.job.id])

    def delete_url(self):
        return reverse('account:delete_apply', args=[self.id])


class RequiredExperience(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, blank=False)
    experience = models.ForeignKey(Experiences, on_delete=models.CASCADE, blank=False, unique=False)

    def delete_url(self):
        return reverse('jobs:job_delete', args=[self.id])


class RequiredEducation(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, blank=False)
    education = models.ForeignKey(Educations, on_delete=models.CASCADE, blank=False, unique=False)

    def delete_url(self):
        return reverse('jobs:job_delete', args=[self.id])


class RequiredSkills(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, blank=False)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, blank=False, unique=False)

    def delete_url(self):
        return reverse('jobs:job_delete', args=[self.id])


class PhoneNumber(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, blank=False)
    phone_number = PhoneNumberField(unique=False, null=True, blank=True)

    def delete_url(self):
        return reverse('jobs:job_delete', args=[self.id])
