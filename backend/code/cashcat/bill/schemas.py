from marshmallow import post_load
from marshmallow import pre_dump
from marshmallow.fields import Date
from marshmallow.fields import Decimal
from marshmallow.fields import Nested
from marshmallow.fields import String
from marshmallow.fields import UUID

from cashcat.application.schemas import ModelSchema
from cashcat.application.schemas import not_blank
from cashcat.bill.models import Bill
from cashcat.bill.models import BillItem


def data_to_bill_item(data):
    return BillItem(
        uid=data.get("uid"),
        name=data.get("name"),
        quantity=data.get("quantity"),
        value=data.get("value"),
        bill_uid=data.get("bill_uid"),
    )


class BillItemSchema(ModelSchema):
    name = String(required=True, validate=not_blank)
    quantity = Decimal(required=True, places=2, allow_none=False)
    value = Decimal(required=True, places=2, allow_none=False)
    bill_uid = UUID(required=True, allow_none=False)

    @pre_dump
    def make_dict(self, obj):
        return dict(
            uid=obj.uid,
            name=obj.name,
            quantity=obj.quantity,
            value=obj.value,
            bill_uid=obj.bill_uid,
        )

    @post_load
    def make_model(self, data):
        return data_to_bill_item(data)


class BillSchema(ModelSchema):
    place = String(required=True, validate=not_blank)
    billed_at = Date(required=True)
    wallet_uid = UUID(required=True, allow_none=False)
    items = Nested(BillItemSchema, many=True, only=("uid", "name", "quantity", "value"))

    @pre_dump
    def make_dict(self, obj):
        return dict(
            uid=obj.uid,
            place=obj.place,
            billed_at=obj.billed_at,
            wallet_uid=obj.wallet_uid,
            items=[item for item in obj.items],
        )

    @post_load
    def make_model(self, data):
        print("hej")
        return Bill(
            uid=data.get("uid"),
            place=data.get("place"),
            billed_at=data.get("billed_at"),
            wallet_uid=data.get("wallet_uid"),
            items=[item for item in data.get("items", [])],
        )
