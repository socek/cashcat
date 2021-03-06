from unittest.mock import MagicMock
from uuid import uuid4

from pytest import fixture
from undecorated import undecorated

from cashcat.auth.jwt import decode_jwt
from cashcat.auth.jwt import encode_jwt_from_user


class TestJwt(object):
    @fixture
    def muser(self):
        return MagicMock()

    @fixture
    def settings(self):
        return {"jwt:secret": "mysupersecret", "jwt:algorithm": "HS256"}

    @fixture
    def encode(self):
        return undecorated(encode_jwt_from_user)

    @fixture
    def decode(self):
        return undecorated(decode_jwt)

    def test_jwt_from_user(self, encode, decode, muser, settings):
        """
        encode_jwt_from_user should create proper jwt which decode_jwt should
        decode properly. "payload" should contains user id.
        """
        muser.uid = uuid4()
        jwt = encode(muser, settings)
        payload = decode(jwt, settings)
        assert payload == {"uid": muser.uid.hex}
