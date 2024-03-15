from django.db import models
import secrets
# Create your models here.

class SingleTokenAccess(models.Model):

    def token_default():
        return secrets.token_urlsafe(36);

    slug = models.CharField(max_length=60, primary_key=True)
    create_date = models.DateField(auto_now_add=True)
    contact = models.EmailField(max_length=100)
    token = models.CharField(default=token_default, max_length=50)
