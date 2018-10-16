from marshmallow import Schema

from marshmallow import pre_dump
from marshmallow.fields import String
from marshmallow.fields import UUID

# from cashcat.wallet.models import Wallet


class WalletSchema(Schema):
    uid = UUID(required=True, allow_none=False)
    name = String(required=True, allow_none=False)
    type = String(required=True, allow_none=False)
    owner_uid = UUID(required=True, allow_none=False)

    @pre_dump
    def make_model(self, obj):
        return dict(
            uid=obj.uid,
            name=obj.name,
            type=obj.type,
            owner_uid=obj.owner_uid)
