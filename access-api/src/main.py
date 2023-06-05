import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import sentry_sdk
from redis import asyncio as aioredis

from api.v1 import transactions, balance, refund, subscribe, payment, webhook
from core.config import SETTINGS
from core.logger import LOGGING
from db import redis_inj

if SETTINGS.SENTRY.SENTRY_ENABLED:
    sentry_sdk.init(
        dsn=SETTINGS.SENTRY.SENTRY_DSN)

redis_inj.redis_pool = aioredis.ConnectionPool(
    host=SETTINGS.REDIS.REDIS_HOST, port=SETTINGS.REDIS.REDIS_PORT, db=0, max_connections=200)

app = FastAPI(
    title=SETTINGS.PROJECT.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,

)

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
