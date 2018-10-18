from marshmallow import Schema

from marshmallow import post_load
from marshmallow import pre_dump
from marshmallow.fields import Date
from marshmallow.fields import String
from marshmallow.fields import UUID

from cashcat.application.schemas import not_blank
from cashcat.bill.models import Bill


class WalletSchema(Schema):
    uid = UUID(required=True, allow_none=False)
    place = String(required=True, validate=not_blank)
    billed_at = Date(required=True, validate=not_blank)
    wallet_uid = UUID(required=True, allow_none=False)

    @pre_dump
    def make_dict(self, obj):
        return dict(uid=obj.uid, name=obj.name, type=obj.type, owner_uid=obj.owner_uid)

    @post_load
    def make_model(self, data):
        return Bill(
            uid=data.get("uid"),
            name=data.get("name"),
            type=data.get("type"),
            owner_uid=data.get("owner_uid"),
        )
