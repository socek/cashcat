from pytest import raises

from cashcat.application.drivers.query import NoResultFound
from cashcat.application.testing import IntegrationFixture


class TestUserDriver(IntegrationFixture):
    def test_find_by_email(self, user_query, user):
        assert user_query.find_by_email(self.user_data["email"]).uid == user.uid

    def test_find_by_email_with_no_user(self, user_query):
        assert user_query.find_by_email(self.user_data["email"]) is None

    def test_create(self, user):
        assert user.uid
        assert user.created_at
        assert user.updated_at
        assert user.name == self.user_data["name"]
        assert user.email == self.user_data["email"]
        assert user.is_admin == self.user_data["is_admin"]
        assert user.password != self.user_data["password"]
        assert type(user.password) == bytes

    def test_get_by_uid(self, user_query, user):
        model = user_query.get_by_uid(user.uid)
        assert model.uid == user.uid
        assert model.created_at == user.created_at
        assert model.updated_at == user.updated_at
        assert model.name == user.name
        assert model.email == user.email
        assert model.is_admin == user.is_admin
        assert model.password == user.password

    def test_get_by_uid_with_bad_uid(self, user_query):
        """
        .get_by_uid should raise NoResultFound when uuid is malformed
        """
        with raises(NoResultFound):
            user_query.get_by_uid("x")

    def test_delete(self, user_command, user_query, user):
        user_command.delete(user.uid)

        with raises(NoResultFound):
            user_query.get_by_uid(user.uid)

        assert list(user_query.list_active()) == []
        assert len(list(user_query.list_all())) == 1

    def test_list_active(self, user_query, user):
        data = list(user_query.list_active())
        assert len(data) == 1
        assert data[0].uid == user.uid
        assert data[0].created_at == user.created_at
        assert data[0].updated_at == user.updated_at
        assert data[0].name == user.name
        assert data[0].email == user.email
        assert data[0].is_admin == user.is_admin
        assert data[0].password == user.password
