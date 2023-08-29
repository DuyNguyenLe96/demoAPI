from django.contrib.auth.models import AbstractUser
from django.db import models
from ..config import MYROLE
import uuid

app_name = 'account'


def get_random_string(string_length=10):
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace('-', '')
    return random[0:string_length]


class UserModel(AbstractUser):
    mkt_id = models.BigIntegerField(unique=True, null=True)
    google_id = models.BigIntegerField(unique=True, null=True)
    first_name = models.CharField(max_length=15, null=True)
    last_name = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=50, unique=True)
    email_verified_at = models.DateTimeField(null=True)
    phone = models.CharField(max_length=15, null=True)
    phone_verified_at = models.DateTimeField(null=True)
    avatar = models.CharField(max_length=255, null=True)
    role = models.SmallIntegerField(default=MYROLE['MEMBER'])
    two_fa_enabled_at = models.DateTimeField(null=True)
    two_fa_secret = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'account'
        managed = True
        db_table = 'user'
        ordering = ['-created_at', '-updated_at', '-id']
        indexes = [
            models.Index(fields=['email', 'id'])
        ]

    @property
    def has_two_factor_enabled(self):
        if not self.two_fa_secret:
            return False
        return True

    def save(self, *args, **kwargs):
        """
        when create a new user, change username,email to lowercase
        """
        if not self.id:
            self.username = self.email[0:6] + get_random_string(10)
            self.username = self.username.lower()
            if self.email:
                self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        when get str of object return username
        """
        return self.username
