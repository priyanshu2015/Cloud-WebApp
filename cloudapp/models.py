from django.db import models
from .managers import UserManager
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q
from datetime import timedelta

# Create your models here.
class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = LowercaseEmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    class Types(models.TextChoices):
        Root = "Root", "ROOT"
        IAM = "IAM"
    
    default_type = Types.Root

    #type = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True)
    type = models.CharField(_('Type'), max_length=255, choices=Types.choices, default=default_type)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.default_type
        return super().save(*args, **kwargs)

class RootUserAdditional(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)


class IAMUserAdditional(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    root_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='root_user')
    

# Model Managers for proxy models
class RootUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type = User.Types.Root)

class IAMUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type = User.Types.IAM)


# Proxy Models. They do not create a seperate table
class RootUser(User):
    default_type = User.Types.Root
    objects = RootUserManager()
    class Meta:
        proxy = True

    @property
    def showAdditional(self):
        return self.rootuseradditional

class IAMUser(User):
    default_type = User.Types.IAM
    objects = IAMUserManager()
    class Meta:
        proxy = True 

    @property
    def showAdditional(self):
        return self.iamuseradditional
