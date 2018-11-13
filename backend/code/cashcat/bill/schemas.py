from datetime import date

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


class BillItemSchema(ModelSchema):
    _decimal_error_messages = {"invalid": "Wymagana jest liczba"}
    uid = UUID(required=False, allow_none=True)
    name = String(required=True, validate=not_blank)
    quantity = Decimal(
        as_string=True,
        required=True,
        places=2,
        allow_none=False,
        error_messages=_decimal_error_messages,
    )
    value = Decimal(
        as_string=True,
        required=True,
        places=2,
        allow_none=False,
        error_messages=_decimal_error_messages,
    )
    bill_uid = UUID(required=True, allow_none=False)
    group_uid = UUID(
        required=True,
        allow_none=False,
        error_messages={"invalid_uuid": "Wybierz grupę"},
    )

    @pre_dump
    def make_dict(self, obj):
        return dict(
            uid=obj.uid,
            name=obj.name,
            quantity=obj.quantity,
            value=obj.value,
            bill_uid=obj.bill_uid,
            group_uid=obj.group_uid,
        )

    @post_load
    def make_model(self, data):
        return BillItem(
            uid=data.get("uid"),
            name=data.get("name"),
            quantity=data.get("quantity"),
            value=data.get("value"),
            bill_uid=data.get("bill_uid"),
            group_uid=data.get("group_uid"),
        )


class BillSchema(ModelSchema):
    place = String(required=True, validate=not_blank)
    billed_at = Date(required=True)
    wallet_uid = UUID(required=True, allow_none=False)
    items = Nested(
        BillItemSchema,
        many=True,
        only=("uid", "name", "quantity", "value", "group_uid"),
    )

    @pre_dump
    def make_dict(self, obj):
        return dict(
            uid=obj.uid,
            place=obj.place,
            billed_at=self._to_date(obj.billed_at),
            wallet_uid=obj.wallet_uid,
            items=[item for item in obj.items],
        )

    def _to_date(self, obj):
        if isinstance(obj, str):
            return date.fromisoformat(obj)
        return obj

    @post_load
    def make_model(self, data):
        return Bill(
            uid=data.get("uid"),
            place=data.get("place"),
            billed_at=data.get("billed_at"),
            wallet_uid=data.get("wallet_uid"),
            items=[item for item in data.get("items", [])],
        )
