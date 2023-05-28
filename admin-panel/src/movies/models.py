import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from billing.models import Subscription, SubscriptionFilmwork

class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(verbose_name=_('Full name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmType(models.TextChoices):
        movie = 'movie', _('Movie')
        tv_show = 'tv_show', _('TV Show')

    title = models.CharField(verbose_name=_('title'), max_length=255)
    description = models.TextField(verbose_name=_('description'), blank=True, null=True)
    creation_date = models.DateField(verbose_name=_('creation date'), blank=True, null=True)
    rating = models.FloatField(verbose_name=_('rating'), blank=True, validators=[
        MinValueValidator(0), MaxValueValidator(100),
    ], null=True)
    type = models.TextField(choices=FilmType.choices, blank=False)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    person = models.ManyToManyField(Person, through='PersonFilmwork')
    subscriptions = models.ManyToManyField(Subscription, related_name='films_relations',
                                           through=SubscriptionFilmwork)
    file_path = models.FileField(verbose_name=_('File'), blank=True, null=True, upload_to='movies/')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = _('Film work')
        verbose_name_plural = _('Film works')
        indexes = [models.Index(fields=['creation_date'], name='film_work_creation_date_idx')]


class GenreFilmwork(UUIDMixin):
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name=_('Genre id'), db_column='genre_id')
    film_work_id = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('Filmwork id'),
                                     db_column='film_work_id')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'
        verbose_name = _('Film genres')
        verbose_name_plural = _('Film genres')
        constraints = [models.UniqueConstraint(fields=['genre_id', 'film_work_id'], name='genre_film_work_idx')]


class PersonFilmwork(UUIDMixin):
    class RoleType(models.TextChoices):
        actor = 'actor', _('Actor')
        writer = 'writer', _('Writer')
        director = 'director', _('Director')

    film_work_id = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name=_('Filmwork id'),
                                     db_column='film_work_id')
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_('Person id'),
                                  db_column='person_id')
    role = models.TextField(verbose_name=_('Role'), choices=RoleType.choices, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'content\".\"person_film_work'
        verbose_name = _('Role in film')
        verbose_name_plural = _('Roles in film')
        constraints = [
            models.UniqueConstraint(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_idx')]
