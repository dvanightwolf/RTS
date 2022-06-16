from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.urls import reverse
from generics.models import Category

# Create your models here.


class CareerAdvice(models.Model):
    # A foreign key to the user when the user is deleted the corresponding threads are deleted as well
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="careeradvice_created", on_delete=models.CASCADE)
    # The review's title
    heading = models.CharField(max_length=256)
    # A field to make SEO friendly links
    slug = models.SlugField(max_length=256)
    # An opening describes what this thread is about
    text = models.TextField()
    # The time and date the review was posted and it's added automatically
    created = models.DateTimeField(auto_now_add=True)
    # Updates the time when the thread is updated
    updated = models.TimeField(auto_now_add=True)
    # Tags to mark the post
    tags = TaggableManager()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)

    def get_absolute_url(self):
        """Returns a Thread object URL"""
        # Build and return a unique and SEO friendly URL for a Thread object
        return reverse('careeradvice:advice_details', args=[self.id])

    def __str__(self):
        return self.heading

    def edit_url(self):
        return reverse('careeradvice:advice_edit', args=[self.id])

    def delete_url(self):
        return reverse('careeradvice:advice_delete', args=[self.id])
