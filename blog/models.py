import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.
class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, blank=True)
    registration_date = models.DateField()

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("blogger_detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['-registration_date']
        permissions = [('can_comment_blogs', 'Comment blogs as user')]

class Blog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, help_text='Unique ID for each blog')
    title = models.CharField(max_length=100)
    post_date = models.DateTimeField()
    author = models.ForeignKey("Blogger", on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['-post_date']

class Comment(models.Model):
    author = models.ForeignKey("Blogger", on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField()
    description = models.TextField(max_length=500, help_text='Enter comment about blog here', 
                                   validators=[MinLengthValidator(3, 'Too short comment')])
    blog = models.ForeignKey("Blog", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} - {self.description}'
    
    class Meta:
        ordering = ['post_date']