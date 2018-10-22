from marshmallow import Schema as BaseSchema
from marshmallow.fields import UUID
from marshmallow.validate import Length

not_blank = Length(min=1, error="Field cannot be blank")


class ModelSchema(BaseSchema):
    uid = UUID(required=True, allow_none=False)
