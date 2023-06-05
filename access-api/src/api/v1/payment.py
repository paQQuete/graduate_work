import datetime
import uuid
import json

import stripe
from aioredis import Redis
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db.database import get_db
from db.redis import get_redis
from core.config import SETTINGS
from models.models import Currency
from services import subscribe

router = APIRouter()
stripe.api_key = SETTINGS.STRIPE.STRIPE__API_KEY


@router.get('/card/{subscribe_id}/')
async def buy_from_card(subscribe_id: uuid.UUID, user_id: uuid.UUID = None, db: Session = Depends(get_db),
                        redis: Redis = Depends(get_redis)):
    """Buy subscription for user using Stripe checkout"""
    redis_key = f'buy_{subscribe_id}_{user_id}'
    cached_data = await redis.get(key=redis_key)
    if not cached_data:
        price_id = subscribe.get_price_id(db=db, subscribe_id=subscribe_id)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {'price': price_id,
                 'quantity': 1},
            ],
            mode='payment',
            client_reference_id=redis_key,
            success_url=f"""{SETTINGS.PROJECT_URL}/api/v1/payment/success/?cache={redis_key}""",
            cancel_url=f"""{SETTINGS.PROJECT_URL}/api/v1/payment/cancel/?cache={redis_key}"""
        )
        await redis.set(key=redis_key, value=json.dumps({
            'checkout_id': checkout_session.id,
            'checkout_url': checkout_session.url,
            'subscribe_id': str(subscribe_id),
            'user_id': str(user_id),
            'created_at': str(datetime.datetime.now()),
        }))
        return RedirectResponse(url=checkout_session.url)
    else:
        cached_data = json.loads(cached_data)
        return RedirectResponse(url=cached_data['checkout_url'])


@router.get('/topup/{user_id}/')
async def topup_balance(user_id: uuid.UUID, amount: int = None, db: Session = Depends(get_db),
                        redis: Redis = Depends(get_redis)):
    """Top-up user balance using Stripe checkout"""
    redis_key = f'topup_{user_id}_{amount}'
    cached_data = await redis.get(key=redis_key)

    if not cached_data:
        stripe_price = stripe.Price.create(
            unit_amount=amount * 100,
            currency=Currency.USD.value,
            product=SETTINGS.STRIPE.STRIPE__BALANCE_PROD_ID
        )
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {'price': stripe_price.id,
                 'quantity': 1},
            ],
            mode='payment',
            client_reference_id=redis_key,
            success_url=f"""{SETTINGS.PROJECT_URL}/api/v1/payment/success/?cache={redis_key}""",
            cancel_url=f"""{SETTINGS.PROJECT_URL}/api/v1/payment/cancel/?cache={redis_key}"""
        )
        await redis.set(key=redis_key, value=json.dumps({
            'checkout_id': checkout_session.id,
            'checkout_url': checkout_session.url,
            'amount': amount,
            'user_id': str(user_id),
            'created_at': str(datetime.datetime.now()),
        }))

        return RedirectResponse(url=checkout_session.url)
    else:
        cached_data = json.loads(cached_data)
        return RedirectResponse(url=cached_data['checkout_url'])


@router.get('/success/')
async def success(cache: str = None, redis: Redis = Depends(get_redis)):
    """Callback endpoint for users browser, for return user browser after Stripe checkout session. Don't call this
    directly"""
    await redis.delete(key=cache)
    return f"Payment completed successfully"


@router.get('/cancel/')
async def cancel(cache: str = None, redis: Redis = Depends(get_redis)):
    """Callback endpoint for users browser, for return user browser after Stripe checkout session. Don't call this
    directly"""
    await redis.delete(key=cache)
    return f"Payment canceled successfully"
