import datetime
import uuid
import json

import stripe
from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db.database import get_db
from db.redis import get_redis
from core.config import SETTINGS
from services import subscribe

router = APIRouter()
stripe.api_key = SETTINGS.STRIPE.STRIPE__API_KEY


@router.get('/buy/{subscribe_id}/')
async def buy_from_card(subscribe_id: uuid.UUID, user_id: uuid.UUID = None, db: Session = Depends(get_db),
                        redis: Redis = Depends(get_redis)):
    cached_data = await redis.get(key=f'{subscribe_id}_{user_id}')
    if not cached_data:
        price_id = subscribe.get_price_id(db=db, subscribe_id=subscribe_id)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {"price": price_id,
                 "quantity": 1},
            ],
            mode='payment',
            success_url=f"""{SETTINGS.PROJECT_URL}/api/v1/payment/after/success/?subscribe_id={subscribe_id}&user_id={user_id}""",
            cancel_url=f"""{SETTINGS.PROJECT_URL}/api/v1/payment/after/cancel/?subscribe_id={subscribe_id}&user_id={user_id}"""
        )
        await redis.set(key=f'{subscribe_id}_{user_id}', value=json.dumps({
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


@router.get('/after/success/')
async def success(subscribe_id: uuid.UUID = None, user_id: uuid.UUID = None, redis: Redis = Depends(get_redis)):
    await redis.delete(key=f'{subscribe_id}_{user_id}')
    return f"You bought Subscription {subscribe_id}"


@router.get('/after/cancel/')
async def cancel(subscribe_id: uuid.UUID = None, user_id: uuid.UUID = None, redis: Redis = Depends(get_redis)):
    await redis.delete(key=f'{subscribe_id}_{user_id}')
    return f"You canceled the purchase - Subscription {subscribe_id}"
