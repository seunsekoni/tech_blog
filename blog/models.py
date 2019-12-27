import django
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete='models.PROTECT')
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=django.utils.timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    # this method allows a post to be published
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # this method allows a comment to be approved
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=django.utils.timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_list')

    def __str__(self):
        return self.text