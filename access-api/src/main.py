import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import sentry_sdk

from api.v1 import transactions, balance
from core import config
from core.logger import LOGGING

sentry_sdk.init(
    dsn="https://d7b229275c864cb9aa5d7a3b7f2ac257@o4504634582302720.ingest.sentry.io/4504662476390400")

app = FastAPI(
    title=config.Settings().PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    pass


@app.on_event('shutdown')
async def shutdown():
    pass


app.include_router(transactions.router, prefix='/api/v1/transactions', tags=['transactions'])
app.include_router(balance.router, prefix='/api/v1/balance', tags=['balance'])

if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=9000,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
