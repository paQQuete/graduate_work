import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import sentry_sdk
import aioredis

from api.v1 import transactions, balance, refund, subscribe, payment, webhook
from core.config import SETTINGS
from core.logger import LOGGING
from db import redis

if SETTINGS.SENTRY.SENTRY_ENABLED:
    sentry_sdk.init(
        dsn=SETTINGS.SENTRY.SENTRY_DSN)

app = FastAPI(
    title=SETTINGS.PROJECT.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (SETTINGS.REDIS.REDIS_HOST, SETTINGS.REDIS.REDIS_PORT), minsize=10, maxsize=20
    )


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()


app.include_router(transactions.router, prefix='/api/v1/transactions', tags=['transactions'])
app.include_router(balance.router, prefix='/api/v1/balance', tags=['balance'])
app.include_router(refund.router, prefix='/api/v1/refund', tags=['refund'])
app.include_router(subscribe.router, prefix='/api/v1/subscribe', tags=['subscribe'])
app.include_router(payment.router, prefix='/api/v1/payment', tags=['payment'])
app.include_router(webhook.router, prefix='/api/v1/webhook', tags=['webhooks'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=9000,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
