from django.db import models


# Create your models here.


class Experiences(models.Model):
    experience = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return self.experience


class Educations(models.Model):
    education = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return self.education


class Skills(models.Model):
    Skill = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return self.Skill


class Countries(models.Model):
    country = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return self.country


class Grades(models.Model):
    grade = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return self.grade


class Category(models.Model):
    """A model that represents a category."""
    # Category name
    name = models.CharField(max_length=1000)
    # A field to make SEO friendly URLs
    slug = models.SlugField(max_length=1000)

    def __str__(self):
        """Makes a human readable representation of the category object in the admin site."""
        return self.name


class Templates(models.Model):
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.color
