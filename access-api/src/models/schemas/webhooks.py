from typing import Any

from pydantic import BaseModel


# class StripeEventData(BaseModel):
#     object: dict[str, Any]
#     billing_address_collection: str
#     cancel_url: str
#     client_reference_id: str
#     consent: str


class StripeEvent(BaseModel):
    id: str
    object: str
    api_version: str
    created: str
    data: dict[str, Any]
    livemode: bool
    pending_webhooks: int
    request: dict[str, Any]
    type: str
