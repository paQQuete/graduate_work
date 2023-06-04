import datetime
import uuid

from celery import shared_task
from django.db.models import Sum
from django.db import transaction
from django.utils import timezone
from .models import Transaction, FundsOnHold, Balance, GrantedAccess, GrantedFilms


@shared_task(bind=True)
def aggregate_balance(user_uuid: uuid.UUID):
    """
    Aggregate all transactions and holds-transactions for user
    :param user_uuid: uuid of target
    :return: actual balance
    """
    transactions_sum = Transaction.objects.filter(user_uuid=user_uuid).aggregate(Sum('cost')).get('cost__sum') or 0
    holds_sum = FundsOnHold.objects.filter(user_uuid=user_uuid).aggregate(Sum('cost')).get('cost__sum') or 0

    balance_value = transactions_sum + holds_sum

    with transaction.atomic():
        Balance.objects.update_or_create(
            user_uuid=user_uuid,
            defaults={
                'balance': balance_value,
                'timestamp_offset': timezone.now()
            }
        )

    return balance_value


@shared_task(bind=True)
def aggregate_balance_for_all_users():
    user_uuids = Transaction.objects.values_list('user_uuid', flat=True).distinct()
    for user_uuid in user_uuids:
        aggregate_balance.delay(user_uuid)


@shared_task(bind=True)
def check_granted_access():
    now = timezone.now()

    expired_grants = GrantedAccess.objects.filter(is_active=True, available_until__lte=now)

    for grant in expired_grants:
        grant.is_active = False
        grant.save()

        GrantedFilms.objects.filter(grant_uuid=grant.uuid, is_active=True).update(is_active=False)
