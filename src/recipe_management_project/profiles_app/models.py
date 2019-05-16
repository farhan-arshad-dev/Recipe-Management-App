from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

# Create your models here.


class UserProfileManager(BaseUserManager):
    """Helps Django work with our cutsom model."""

    def create_user(self, email, name, password=None):
        """Creates a new user profile object."""

        if not email:
            raise ValueError('User must have an email address.')

        # convert the email char case to small.
        email = self.normalize_email(email)
        # set user's email, and name
        user = self.model(email=email, name=name)

        # set password separately to encrypt.
        user.set_password(password)
        # save use data in database
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new supper with given detatils."""

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represent a "user profiles" inside our system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    # necessory by the django while create a model.
    is_actvie = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # helps the django to create user using custom model
    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Use to get users full name."""

        return self.name

    def get_short_name(self):
        """Use to get users full name."""

        return self.name

    def __str__(self):
        """Djang uses this when its need to convert the object to a string."""

        return self.email
