from django.db import models

from profiles_app import models as profiles_models

# Create your models here.

class FollowingModel(models.Model):
    """Represents User following item in our System"""

    following_to = models.ForeignKey(profiles_models.UserProfile, on_delete=models.DO_NOTHING, related_name='following_to')
    following_by = models.ForeignKey(profiles_models.UserProfile, on_delete=models.DO_NOTHING, related_name='following_by')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('following_to', 'following_by'),)

    def __str__(self):
        """Djang uses this when its need to convert the object to a string."""

        return self.following_by.email+ ' ' + self.following_to.email + ' '
