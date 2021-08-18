from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Name')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Name'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Name'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Category'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Genre'
    )
    year = models.PositiveSmallIntegerField(
        validators=[year_validator],
        verbose_name='Year'
    )

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_name_year'
            )
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Title'
    )
    text = models.TextField(verbose_name='Text')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Author'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Score must be in range [1..10]'),
            MaxValueValidator(10, message='Score must be in range [1..10]')
        ],
        verbose_name='Score'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Date published'
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Review'
    )
    text = models.TextField(verbose_name='Text')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Date published'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
