import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from movies.models import Filmwork


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Subscription(UUIDMixin, TimeStampedMixin):
    class SubscriptionType(models.TextChoices):
        one = 'one', _('One')
        batch = 'batch', _('Batch')

    class ChargeType(models.TextChoices):
        daily = 'daily', _('Daily')
        one_time = 'one-time', _('One-Time')

    name = models.CharField(verbose_name=_('Name'), max_length=255, null=False, blank=False)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    periodic_type = models.TextField(choices=SubscriptionType.choices, blank=False, null=False)
    cost = models.IntegerField(verbose_name=_('Subscribe price'), blank=False, null=False)
    charge_type = models.TextField(choices=ChargeType.choices, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='subscriptions_created')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content\".\"subscribe'
        verbose_name = _('Subscribe plan')
        verbose_name_plural = _('Subscribe plans')
        indexes = [models.Index(fields=['periodic_type'], name='subscription_periodic_type_idx')]


class SubscriptionFilmwork(UUIDMixin):
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name=_('Subscription_id'),
                                        db_column='subscription_id')
    filmwork_id = models.ForeignKey(Filmwork, on_delete=models.DO_NOTHING, verbose_name=_('Filmwork_id'),
                                    db_column='filmwork_id')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'content\".\"subscription_filmwork'
        verbose_name = _('Subscription films')
        verbose_name_plural = _('Subscription films')
        indexes = [
            models.Index(fields=['subscription_id', 'filmwork_id'], name='subscription_filmwork_idx')
        ]
