import datetime
import uuid

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseSchemaModel(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps



