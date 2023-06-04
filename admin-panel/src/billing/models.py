import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class UUIDMixinBilling(models.Model):
    uuid = models.UUIDField(db_column='uuid', primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Subscription(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name=_('Name'), max_length=255, null=False, blank=False)
    description = models.TextField(verbose_name=_('Description'), null=False, blank=False)
    cost = models.IntegerField(verbose_name=_('Subscribe price per day'), blank=False, null=False)
    duration = models.IntegerField(verbose_name=_('Duration of subscription'), blank=False, null=False)
    all_time_cost = models.IntegerField(verbose_name=_('All time cost '), blank=True, null=False, default=0)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='subscriptions_created')
    payment_gw_product_id = models.CharField(verbose_name=_('Actual Product ID on payment gateway'), max_length=255,
                                             null=False, blank=True)
    payment_gw_price_id = models.CharField(
        verbose_name=_('Latest Price ID for this subscription plan on payment gateway'),
        max_length=255, null=False, blank=True)
    films = models.ManyToManyField('movies.Filmwork', through='SubscriptionFilmwork',
                                   related_name='subscriptions_relations')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content\".\"subscribe'
        verbose_name = _('Subscribe plan')
        verbose_name_plural = _('Subscribe plans')


class SubscriptionFilmwork(UUIDMixin):
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name=_('Subscription_id'),
                                        db_column='subscription_id')
    filmwork_id = models.ForeignKey('movies.Filmwork', on_delete=models.DO_NOTHING, verbose_name=_('Filmwork_id'),
                                    db_column='filmwork_id')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'content\".\"subscription_filmwork'
        verbose_name = _('Subscription films')
        verbose_name_plural = _('Subscription films')
        indexes = [
            models.Index(fields=['subscription_id', 'filmwork_id'], name='subscription_filmwork_idx')
        ]


class UnmanagedMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        raise NotImplementedError("This model is read-only")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("This model is read-only")


class TransactionMixin(models.Model):
    user_uuid = models.UUIDField(editable=False, verbose_name=_('User id'))
    cost = models.IntegerField(verbose_name=_('Transaction amount'))
    timestamp = models.DateTimeField(verbose_name=_('Transaction complete date'))

    class Meta:
        abstract = True


class Transaction(TransactionMixin, UUIDMixinBilling, TimeStampedMixin, UnmanagedMixin):
    class TypeEnum(models.TextChoices):
        topup = 'topup', _('Top up')
        spending = 'spending', _('Spending')
        refund = 'refund', _('Refund')

    type = models.TextField(choices=TypeEnum.choices, verbose_name=_('Transaction type'))

    class Meta:
        managed = False
        db_table = 'billing\".\"transaction'
        verbose_name = _('Transaction (read-only)')
        verbose_name_plural = _('Transactions (read-only)')


class FundsOnHold(TransactionMixin, UUIDMixinBilling, TimeStampedMixin, UnmanagedMixin):
    class TypeEnum(models.TextChoices):
        spending = 'spending', _('Spending')
        refund = 'refund', _('Refund')

    type = models.TextField(choices=TypeEnum.choices, verbose_name=_('Hold type'))

    class Meta:
        managed = False
        db_table = 'billing\".\"funds_hold'
        verbose_name = _('Fund on hold (read-only)')
        verbose_name_plural = _('Funds on hold (read-only)')


class Balance(UUIDMixinBilling, TimeStampedMixin):
    user_uuid = models.UUIDField(verbose_name=_('User id'))
    balance = models.IntegerField(verbose_name=_('User balance'))
    timestamp_offset = models.DateTimeField(verbose_name=_('Actual balance time'))

    class Meta:
        managed = False
        db_table = 'billing\".\"balance'
        verbose_name = _('User balance')
        verbose_name_plural = _('Users balances')


class GrantedAccess(UUIDMixinBilling, TimeStampedMixin):
    user_uuid = models.UUIDField(verbose_name=_('User id'))
    subscription_id = models.UUIDField(verbose_name=_('Subscription id'))
    granted_at = models.DateTimeField(verbose_name=_('Granted at'))
    available_until = models.DateTimeField(verbose_name=_('Grant available until'))
    is_active = models.BooleanField(verbose_name=_('Is active grant'))
    cost_per_day = models.IntegerField(verbose_name=_('Cost this grant per day'))

    class Meta:
        managed = False
        db_table = 'billing\".\"granted_access'
        verbose_name = _('Grant')
        verbose_name_plural = _('Grants')


class GrantedFilms(UUIDMixinBilling, TimeStampedMixin):
    user_uuid = models.UUIDField(verbose_name=_('User id'))
    movie_uuid = models.UUIDField(verbose_name=_('Movie id'))
    granted_at = models.DateTimeField(verbose_name=_('Granted at (same as parent grant)'))
    grant_uuid = models.UUIDField(verbose_name=_('Grant id'))
    is_active = models.BooleanField(verbose_name=_('Is active grant for film (same as parent grant'))

    class Meta:
        managed = False
        db_table = 'billing\".\"granted_films'
        verbose_name = _('Grant filmworks')
        verbose_name_plural = _('Grants filmworks')
