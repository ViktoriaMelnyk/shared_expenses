from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    groups = models.ManyToManyField('groups.Group', blank=True, through='groups.GroupUser')

    def __str__(self):
        return self.username
