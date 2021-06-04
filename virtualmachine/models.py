from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your models here.
class VirtualMachine(models.Model):
    root_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    os = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
