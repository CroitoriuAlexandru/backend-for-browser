from django.db import models

# Create your models here.

# create a table that will store social login for google with the fields:
# user, google_user_id, email, verified_email, picture_url

class GoogleUser(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    google_user_id = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    verified_email = models.BooleanField()
    picture_url = models.URLField()
    def __str__(self):
        return self.user.username 