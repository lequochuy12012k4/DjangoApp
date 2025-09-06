from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='data/images/')
    document = models.FileField(upload_to='data/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_documents', blank=True)

    def __str__(self):
        return self.title
