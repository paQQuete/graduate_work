import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
    migrations.RunSQL('''CREATE SCHEMA IF NOT EXISTS content;
ALTER ROLE app SET search_path TO content,public;
CREATE EXTENSION "uuid-ossp";'''),


    migrations.CreateModel(
        name='Filmwork',
        fields=[
            ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('title', models.CharField(max_length=255, verbose_name='title')),
            ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ('creation_date', models.DateField(blank=True, null=True, verbose_name='creation date')),
            ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0),
                                                                            django.core.validators.MaxValueValidator(
                                                                                100)], verbose_name='rating')),
            ('type', models.TextField(choices=[('movie', 'Movie'), ('tv_show', 'TV Show')])),
            ('file_path', models.FileField(blank=True, null=True, upload_to='movies/', verbose_name='File')),
        ],
        options={
            'verbose_name': 'Film work',
            'verbose_name_plural': 'Film works',
            'db_table': 'content"."film_work',
        },
    ),
    migrations.CreateModel(
        name='Genre',
        fields=[
            ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('name', models.CharField(max_length=255, verbose_name='Name')),
            ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
        ],
        options={
            'verbose_name': 'Genre',
            'verbose_name_plural': 'Genres',
            'db_table': 'content"."genre',
        },
    ),
    migrations.CreateModel(
        name='Person',
        fields=[
            ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('full_name', models.CharField(max_length=255, verbose_name='Full name')),
        ],
        options={
            'verbose_name': 'Person',
            'verbose_name_plural': 'Persons',
            'db_table': 'content"."person',
        },
    ),
    migrations.CreateModel(
        name='PersonFilmwork',
        fields=[
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('role',
             models.TextField(choices=[('actor', 'Actor'), ('writer', 'Writer'), ('director', 'Director')], null=True,
                              verbose_name='Role')),
            ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ('film_work_id', models.ForeignKey(db_column='film_work_id', on_delete=django.db.models.deletion.CASCADE,
                                               to='movies.filmwork', verbose_name='Filmwork id')),
            ('person_id',
             models.ForeignKey(db_column='person_id', on_delete=django.db.models.deletion.CASCADE, to='movies.person',
                               verbose_name='Person id')),
        ],
        options={
            'verbose_name': 'Role in film',
            'verbose_name_plural': 'Roles in film',
            'db_table': 'content"."person_film_work',
        },
    ),
    migrations.CreateModel(
        name='GenreFilmwork',
        fields=[
            ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ('film_work_id', models.ForeignKey(db_column='film_work_id', on_delete=django.db.models.deletion.CASCADE,
                                               to='movies.filmwork', verbose_name='Filmwork id')),
            ('genre_id',
             models.ForeignKey(db_column='genre_id', on_delete=django.db.models.deletion.CASCADE, to='movies.genre',
                               verbose_name='Genre id')),
        ],
        options={
            'verbose_name': 'Film genres',
            'verbose_name_plural': 'Film genres',
            'db_table': 'content"."genre_film_work',
        },
    ),
    migrations.AddField(
        model_name='filmwork',
        name='genres',
        field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.Genre'),
    ),
    migrations.AddField(
        model_name='filmwork',
        name='person',
        field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.Person'),
    ),
    migrations.AddConstraint(
        model_name='personfilmwork',
        constraint=models.UniqueConstraint(fields=('film_work_id', 'person_id', 'role'), name='film_work_person_idx'),
    ),
    migrations.AddConstraint(
        model_name='genrefilmwork',
        constraint=models.UniqueConstraint(fields=('genre_id', 'film_work_id'), name='genre_film_work_idx'),
    ),
    migrations.AddIndex(
        model_name='filmwork',
        index=models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
    ),
    ]
