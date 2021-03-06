from jwt import decode
from jwt import encode

from sapp.decorators import WithContext

from cashcat import app


@WithContext(app, args=["settings"])
def encode_jwt_from_user(user, settings):
    payload = {"uid": user.uid}
    return encode(
        payload, settings["jwt:secret"], algorithm=settings["jwt:algorithm"]
    ).decode("utf8")


@WithContext(app, args=["settings"])
def decode_jwt(token, settings):
    return decode(token, settings["jwt:secret"], algorithms=[settings["jwt:algorithm"]])
