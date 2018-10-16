from marshmallow.validate import Length

not_blank = Length(min=1, error="Field cannot be blank")
