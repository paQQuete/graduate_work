import datetime
import uuid as builtin_uuid

from models.schemas.base import BaseSchemaModel, BaseFullModelMixin


class GrantedAccessBase(BaseSchemaModel):
    user_uuid: builtin_uuid.UUID
    subscription_id: builtin_uuid.UUID
    granted_at: datetime.datetime
    available_until: datetime.datetime


class GrantedAccessCreate(GrantedAccessBase):
    pass

class GrantedFilm(BaseFullModelMixin):
    uuid: builtin_uuid.UUID
    granted_at: datetime.datetime
    grant_uuid: builtin_uuid.UUID

    class Config:
        orm_mode = True



class GrantedAccess(GrantedAccessBase, BaseFullModelMixin):
    uuid: builtin_uuid.UUID
    films: list[GrantedFilm]

    class Config:
        orm_mode = True
