from django.conf import settings
from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=36)
    slug = models.SlugField(unique=True, db_index=True)
    desc = models.SlugField(default='', blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=36)
    slug = models.SlugField(unique=True, db_index=True)
    desc = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, db_index=True)

    # https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#referencing-the-user-model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    content = models.TextField()

    allow_comment = models.BooleanField(default=True)
    allow_robots = models.BooleanField(default=True)
    is_page = models.BooleanField(default=False, blank=True, db_index=True)
    is_public = models.BooleanField(default=False, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, db_index=True)

    @property
    def comments(self):
        return Comment.objects.filter(post=self, parent=None).order_by('-created_at').all()

    @comments.setter
    def comments(self, _):
        raise AttributeError

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    content = models.TextField()

    author_name = models.CharField(max_length=256)
    author_email = models.EmailField()
    author_site = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.content
