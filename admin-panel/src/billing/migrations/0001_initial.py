# Generated by Django 3.2 on 2023-05-23 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [

        migrations.CreateModel(
            name='Balance',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(db_column='uuid', default=uuid.uuid4, editable=False, primary_key=True,
                                          serialize=False)),
                ('user_uuid', models.UUIDField(verbose_name='User id')),
                ('balance', models.IntegerField(verbose_name='User balance')),
                ('timestamp_offset', models.DateTimeField(verbose_name='Actual balance time')),
            ],
            options={
                'verbose_name': 'User balance',
                'verbose_name_plural': 'Users balances',
                'db_table': 'billing"."balance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FundsOnHold',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(db_column='uuid', default=uuid.uuid4, editable=False, primary_key=True,
                                          serialize=False)),
                ('user_uuid', models.UUIDField(editable=False, verbose_name='User id')),
                ('cost', models.IntegerField(verbose_name='Transaction amount')),
                ('timestamp', models.DateTimeField(verbose_name='Transaction complete date')),
                ('type',
                 models.TextField(choices=[('spending', 'Spending'), ('refund', 'Refund')], verbose_name='Hold type')),
            ],
            options={
                'verbose_name': 'Fund on hold (read-only)',
                'verbose_name_plural': 'Funds on hold (read-only)',
                'db_table': 'billing"."funds_hold',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('uuid', models.UUIDField(db_column='uuid', default=uuid.uuid4, editable=False, primary_key=True,
                                          serialize=False)),
                ('user_uuid', models.UUIDField(editable=False, verbose_name='User id')),
                ('cost', models.IntegerField(verbose_name='Transaction amount')),
                ('timestamp', models.DateTimeField(verbose_name='Transaction complete date')),
                ('type', models.TextField(choices=[('topup', 'Top up'), ('spending', 'Spending'), ('refund', 'Refund')],
                                          verbose_name='Transaction type')),
            ],
            options={
                'verbose_name': 'Transaction (read-only)',
                'verbose_name_plural': 'Transactions (read-only)',
                'db_table': 'billing"."transaction',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('periodic_type', models.TextField(choices=[('one', 'One'), ('batch', 'Batch')])),
                ('cost', models.IntegerField(verbose_name='Subscribe price')),
                ('charge_type', models.TextField(choices=[('daily', 'Daily'), ('one-time', 'One-Time')])),
                ('created_by',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='subscriptions_created',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Subscribe plan',
                'verbose_name_plural': 'Subscribe plans',
                'db_table': 'content"."subscribe',
            },
        ),
        migrations.CreateModel(
            name='SubscriptionFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('filmwork_id',
                 models.ForeignKey(db_column='filmwork_id', on_delete=django.db.models.deletion.DO_NOTHING,
                                   to='movies.filmwork', verbose_name='Filmwork_id')),
                ('subscription_id',
                 models.ForeignKey(db_column='subscription_id', on_delete=django.db.models.deletion.CASCADE,
                                   to='billing.subscription', verbose_name='Subscription_id')),
            ],
            options={
                'verbose_name': 'Subscription films',
                'verbose_name_plural': 'Subscription films',
                'db_table': 'content"."subscription_filmwork',
            },
        ),
        migrations.AddIndex(
            model_name='subscriptionfilmwork',
            index=models.Index(fields=['subscription_id', 'filmwork_id'], name='subscription_filmwork_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['periodic_type'], name='subscription_periodic_type_idx'),
        ),
    ]
