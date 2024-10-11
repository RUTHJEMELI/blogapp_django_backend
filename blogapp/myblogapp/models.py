from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .managers import CustomUserManager
from django.db.models import CASCADE

class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name=_('email'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name',  ]  # Adjust as needed

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Post(models.Model):
    text_content = models.TextField(max_length=1000, null=False, blank=True)  # Text content for the post
    media = models.FileField(upload_to='media/', null=True, blank=True)  # File field for media (e.g., images or videos)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text_content[:30]  # Return the first 30 characters of the text content

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name='likes')
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} likes {self.post.text_content[:20]}"

class Comments(models.Model):
    comment = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name='comments')  # Link to the post

    def __str__(self):
        return self.comment[:20]
