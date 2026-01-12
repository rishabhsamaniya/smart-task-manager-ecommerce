from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

# Create your models here.

# Custom User manager

class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None):
        if not mobile:
            raise ValueError("Mobile number is required")
        
        user = self.model(mobile=mobile)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None):
        user = self.create_user(mobile, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

# Custom User model

class User(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=10, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "mobile" # Login Field
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mobile


############## User Company ##############

class Company(models.Model):
    name = models.CharField(max_length=150, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owner_name"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

############## User Profile ##############

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("employee", "Employee"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_profile"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="emoloyee"
    )

    photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return F"{self.first_name} ({self.user.mobile})"
    


