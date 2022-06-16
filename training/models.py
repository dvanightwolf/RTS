from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager
from django.urls import reverse
from generics.models import Category, Countries


class Training(models.Model):
    # A foreign key to the user when the user is deleted the corresponding threads are deleted as well.
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="training_created", on_delete=models.CASCADE)
    # The review's title.
    title = models.CharField(max_length=256)
    # A field to make SEO friendly links.
    slug = models.SlugField(max_length=256)
    # An opening describes what this thread is about.
    description = models.TextField(blank=True)
    # Decimal field holds the price.
    price = models.DecimalField(decimal_places=2, max_digits=10)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, blank=False)
    # Is this still available or not.
    is_available = models.BooleanField(default=True)
    # The time and date the review was posted, and it's added automatically.
    created = models.DateTimeField(auto_now_add=True)
    # Tags to mark the post.
    tags = TaggableManager()
    # Post's category.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    # Post's Update time.
    updated = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)

    def get_absolute_url(self):
        """Returns a Training object URL."""
        # Build and return a unique and SEO friendly URL for a Training object.
        return reverse('training:training_details', args=[self.id])

    def get_absolute_edit_url(self):
        """Returns a Training object URL to edit."""
        # Build and return a unique for a Training object.
        return reverse('training:edit_training', args=[self.id])

    def get_absolute_delete_url(self):
        """Returns a Training object URL to edit."""
        # Build and return a unique for a Training object.
        return reverse('training:training_delete', args=[self.id])

    def __str__(self):
        return self.title


