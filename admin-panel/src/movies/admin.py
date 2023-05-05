from django.contrib import admin
from .models import Genre, Person, Filmwork, GenreFilmwork, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['genres']


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ['genre_id']


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ['person_id']


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    list_display = ('title', 'type', 'creation_date', 'rating')



@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ['person']

