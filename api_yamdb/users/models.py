from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Enter email.')
        if not username:
            raise ValueError('Enter username.')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    bio = models.TextField(
        max_length=500,
        verbose_name='About me',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )

    class UserRole:
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        choices = [
            (USER, 'user'),
            (ADMIN, 'admin'),
            (MODERATOR, 'moderator'),
        ]

    role = models.CharField(
        max_length=25,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR
