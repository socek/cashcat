from uuid import uuid4

from pytest import fixture

from cashcat.auth.models import User


class TestUser(object):
    @fixture
    def user(self):
        return User(uuid4())

    def test_set_password(self, user):
        """
        .set_password should hash the password
        """
        user.set_password("password")

        assert user.password != "password"

    def test_do_password_match(self, user):
        """
        .do_password_match should validate only proper password
        """
        user.set_password("elo")

        assert user.do_password_match("elo")
        assert not user.do_password_match("no")

    def test_validate_empty_password(self, user):
        """
        .do_password_match should not validate empty password
        """
        assert not user.do_password_match(None)
