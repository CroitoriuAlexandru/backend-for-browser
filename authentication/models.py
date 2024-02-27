from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    picture = models.CharField(max_length=250, null=True, blank=True)
    username = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=250, null=True, blank=True)
    
    REGISTRATION_CHOICES = [
        ('email', 'Email'),
        ('google', 'Google'),
    ]
    
    registration_method = models.CharField(
        max_length=10,
        choices=REGISTRATION_CHOICES,
        default='email'
    )

    def __str__(self):
       return self.email
   
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    

class GoogleAccessTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=250, null=False, blank=False)
    access_token = models.CharField(max_length=250, null=False, blank=False)
    
    
   
# from django.db import models
# from django.contrib.auth.validators import UnicodeUsernameValidator
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
# from django.utils.translation import gettext_lazy as _
# from django.utils import timezone
# from django.contrib.auth.hashers import make_password
# from django.apps import apps
# import jwt
# from django.conf import settings
# from datetime import datetime, timedelta

# class MyUserManager(UserManager):
#     def _create_user(self, username, email, password, **extra_fields):
#         """
#         Create and save a user with the given username, email, and password.
#         """
#         if not username:
#             raise ValueError("The given username must be set")
        
#         if not email:
#             raise ValueError("The given email must be set")
        
#         email = self.normalize_email(email)
#         # Lookup the real model class from the global app registry so this
#         # manager method can be used in migrations. This is fine because
#         # managers are by definition working on the real model.
#         GlobalUserModel = apps.get_model(
#             self.model._meta.app_label, self.model._meta.object_name
#         )
#         username = GlobalUserModel.normalize_username(username)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.password = make_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(username, email, password, **extra_fields)

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self._create_user(username, email, password, **extra_fields)


# # Create your models here.
# class User(AbstractBaseUser, PermissionsMixin, models.Model):
#     """
#     An abstract base class implementing a fully featured User model with
#     admin-compliant permissions.

#     Username and password are required. Other fields are optional.
#     """
#     REGISTRATION_CHOICES = [
#         ('email', 'Email'),
#         ('google', 'Google'),
#     ]
#     registration_method = models.CharField(
#         max_length=10,
#         choices=REGISTRATION_CHOICES,
#         default='email'
#     )
#     username_validator = UnicodeUsernameValidator()

#     username = models.CharField(
#         _("username"),
#         max_length=150,
#         unique=True,
#         help_text=_(
#             "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
#         ),
#         validators=[username_validator],
#         error_messages={
#             "unique": _("A user with that username already exists."),
#         },
#     )
    
#     picture = models.CharField(max_length=250, null=True, blank=True)
#     first_name = models.CharField(_("first name"), max_length=150, blank=True)
#     last_name = models.CharField(_("last name"), max_length=150, blank=True)
#     email = models.EmailField(_("email address"), blank=False, unique=True)
#     is_staff = models.BooleanField(
#         _("staff status"),
#         default=False,
#         help_text=_("Designates whether the user can log into this admin site."),
#     )
#     is_active = models.BooleanField(
#         _("active"),
#         default=True,
#         help_text=_(
#             "Designates whether this user should be treated as active. "
#             "Unselect this instead of deleting accounts."
#         ),
#     )
#     date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
#     email_verified = models.BooleanField(
#         _("active"),
#         default=False,
#         help_text=_(
#             "Designates whether this user email is validated. "
#         ),
#     )
#     objects = MyUserManager()

#     EMAIL_FIELD = "email"
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]

#     @property
#     def token(self):
#         token = jwt.encode(
#             {'username': self.username, 'email': self.email, 'exp': datetime.utcnow() + timedelta(hours=24)}, 
#             settings.SECRET_KEY, 
#             algorithm="HS256"
#             )
#         return token
    