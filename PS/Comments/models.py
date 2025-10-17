from django.db import models
from datetime import date
import uuid
from tinymce.models import HTMLField
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):

    # Auto-generate unique UUID
    # id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,   
    #     editable=False
    # )

    title = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    content = HTMLField(default="")   # TinyMCE rich text editor
    overview = models.CharField(max_length=300, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
   

    date_created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.title} by {self.author.username}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # oldest first for proper display

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"

    @property
    def is_parent(self):
        return self.parent is None