from marshmallow import post_load
from marshmallow import pre_dump
from marshmallow.fields import String
from marshmallow.fields import UUID

from cashcat.application.schemas import ModelSchema
from cashcat.application.schemas import not_blank
from cashcat.group.models import Group


class GroupSchema(ModelSchema):
    name = String(required=True, validate=not_blank)
    wallet_uid = UUID(required=True, allow_none=False)

    @pre_dump
    def make_dict(self, obj):
        return dict(uid=obj.uid, name=obj.name, wallet_uid=obj.wallet_uid)

    @post_load
    def make_model(self, data):
        return Group(
            uid=data.get("uid"),
            name=data.get("name"),
            wallet_uid=data.get("wallet_uid"),
        )
