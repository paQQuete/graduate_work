import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import sentry_sdk

from api.v1 import bookmarks
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
    kafka.producer = aiokafka.AIOKafkaProducer(bootstrap_servers=config.Settings().KAFKA_SERVER)
    await kafka.producer.start()


@app.on_event('shutdown')
async def shutdown():
    await kafka.producer.stop()


app.include_router(views.router, prefix='/api/v1/views', tags=['views'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])
app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(reviews.router, prefix='/api/v1/reviews', tags=['reviews'])

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
