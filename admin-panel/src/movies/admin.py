from django.contrib import admin
from .models import Genre, Person, Filmwork, GenreFilmwork, PersonFilmwork
from billing.models import SubscriptionFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['genres']


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ['genre_id']


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ['person_id']


class SubscriptionFilmworkInline(admin.TabularInline):
    model = SubscriptionFilmwork
    autocomplete_fields = ['subscription_id']


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline, SubscriptionFilmworkInline)

    list_display = ('title', 'type', 'creation_date', 'rating')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ['person']
