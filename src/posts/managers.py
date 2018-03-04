from django.db import models
from django.utils import timezone


class PostManager(models.Manager):

    def active(self):
        return self.filter(active=True)

    def published(self):
        return self.filter(published__lte=timezone.now())

    def current(self):
        return self.published().order_by("-published")
