from marshmallow import post_load
from marshmallow import pre_dump
from marshmallow.fields import String
from marshmallow.fields import UUID

from cashcat.application.schemas import ModelSchema
from cashcat.application.schemas import not_blank
from cashcat.wallet.models import Wallet


class WalletSchema(ModelSchema):
    name = String(required=True, validate=not_blank)
    type = String(required=True, validate=not_blank)
    owner_uid = UUID(required=True, allow_none=False)

    @pre_dump
    def make_dict(self, obj):
        return dict(uid=obj.uid, name=obj.name, type=obj.type, owner_uid=obj.owner_uid)

    @post_load
    def make_model(self, data):
        return Wallet(
            uid=data.get("uid"),
            name=data.get("name"),
            type=data.get("type"),
            owner_uid=data.get("owner_uid"),
        )
