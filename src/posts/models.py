import pytz

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.conf import settings

from .managers import PostManager


class Post(models.Model):
    title = models.CharField(max_length=90)
    slug = models.SlugField(max_length=90)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name= "Author",
        on_delete=models.CASCADE
    )

    teaser_html = models.TextField(editable=False)
    content_html = models.TextField(editable=False)
    description = models.TextField(blank=True)
    
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)  # when first revision was created
    updated = models.DateTimeField(auto_now=True)  # when last revision was created (even if not published)
    published = models.DateTimeField(null=True, blank=True)  # when last published
    view_count = models.IntegerField(default=0, editable=False)

    @property
    def older_post(self):
        qs = Post.objects.published()
        if self.is_published:
            qs = qs.filter(published__lt=self.published)
        return next(iter(qs), None)

    @property
    def newer_post(self):
        if self.is_published:
            return next(iter(Post.objects.published().order_by("published").filter(published__gt=self.published)), None)

    @property
    def is_future_published(self):
        return self.is_published and self.published is not None and self.published > timezone.now()

    @property
    def is_published(self):
        return self.title

    @property
    def meta_description(self):
        if self.description:
            return self.description
        else:
            return strip_tags(self.teaser_html)

    class Meta:
        ordering = ("-published",)
        get_latest_by = "published"
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    objects = PostManager()

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.updated_at = timezone.now()
        if self.is_published and self.published is None:
            self.published = timezone.now()
        self.full_clean()
        super(Post, self).save(**kwargs)

    def inc_views(self):
        self.view_count += 1
        self.save()
        self.published().inc_views()
