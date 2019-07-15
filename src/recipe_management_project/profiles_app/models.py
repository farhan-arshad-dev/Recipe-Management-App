"""
Models definitive source of information about your data. It contains the
essential fields and behaviors of the data you’re storing. Generally, each
model maps to a single database table.
"""
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

# Create your models here.


class UserProfileManager(BaseUserManager):
    """Helps Django work with our cutsom model."""

    def create_user(self, email, name, password=None):
        """Creates a new user profile object."""
        # if user not have an email that raise the ValueError
        if not email:
            raise ValueError('User must have an email address.')

        # convert the email char case to small and Comes with BaseUserManager
        email = self.normalize_email(email)
        # set user's email, and name
        user = self.model(email=email, name=name)

        # set password separately to encrypt.
        user.set_password(password)
        # save user data in database
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
    """
    Represent a "user profiles" inside our system. Custom user model that
    supports using email instated of username
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    # necessary by the django while create a model.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # helps the django to create user using custom model
    objects = UserProfileManager()

    # Customizes the username field to email.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    # optional helper methods
    def get_full_name(self):
        """Use to get users full name."""

        return self.name

    def get_short_name(self):
        """Use to get users full name."""

        return self.name

    def __str__(self):
        """Djang uses this when its need to convert the object to a string."""

        return self.email
