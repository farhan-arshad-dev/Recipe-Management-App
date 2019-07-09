"""
Models definitive source of information about your data. It contains the
essential fields and behaviors of the data you’re storing. Generally, each
model maps to a single database table.
"""
from django.db import models

from profiles_app import models as profiles_models

# Create your models here.


class RecipeModel(models.Model):
    """ Represent a "Recipe" inside our system"""

    user_profile = models.ForeignKey(
        profiles_models.UserProfile,
        on_delete=models.CASCADE
        )
    title = models.CharField(max_length=255)
    brief_description = models.TextField()
    directions = models.TextField()
    ingredients = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string."""

        return self.title
