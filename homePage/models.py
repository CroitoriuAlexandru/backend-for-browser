from django.db import models
from authentication.models import User

# Create your models here.
class HomeBackground(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    image = models.ImageField(upload_to='test/', default="test.png")

    def __str__(self):
        return self.title

class HomeLayout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(null=False, blank=False)
    position = models.IntegerField(null=False, blank=False)
    width = models.IntegerField(null=False, blank=False)
    height = models.IntegerField(null=False, blank=False)
    
    def __str__(self):
        return self.url