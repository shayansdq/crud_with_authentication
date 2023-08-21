from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=32, null=False, verbose_name='Title')
    body = models.TextField(max_length=256)

    # slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return f"<Post-> title: {self.title},"

    # def get_absolute_url(self):
    #     return reverse("post_detail", kwargs={"slug": self.slug})

    # def save(self, *args, **kwargs):  # new
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)


"""
tests
filterset
pagination
mahyar.z@mtnirancell.ir
authenticated deletes, updates
safe methods
log
"""
