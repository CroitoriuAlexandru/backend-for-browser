from django.db import models

# Create your models here.

# create a table that will store social login for google with the fields:
# user, google_user_id, email, verified_email, picture_url

class GoogleUser(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    google_user_id = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, blank=True)
    verified_email = models.BooleanField()
    picture = models.URLField()
    family_name = models.CharField(max_length=100, null=True, blank=True)
    given_name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.user.username 
    
    
    
    

# ic| request.data: {'email': 'partyentertainers93@gmail.com',
#     'family_name': 'Alex',
#     'given_name': 'Eu sunt',
#     'id': '101866336601974016801',
#     'locale': 'en',
#     'name': 'Eu sunt Alex',
#     'picture': 'https://lh3.googleusercontent.com/a/ACg8ocK3J5h5KBYa1pCTvbD_A7ixZav9YI8LK1folHsSKtfqKpk=s96-c',
#     'verified_email': True}