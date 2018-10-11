from uuid import uuid4

from pytest import fixture
from pytest import raises

from cashcat.application.drivers.query import NoResultFound
from cashcat.application.testing import IntegrationFixture
from cashcat.auth.drivers import UserCommand
from cashcat.auth.drivers import UserQuery
from cashcat.auth.models import User


class TestUserDriver(IntegrationFixture):
    user_data = dict(
        name="user2", email="user2@my.pl", is_admin=False, password=b"mypassword"
    )

    @fixture
    def query(self, app):
        return UserQuery(app.dbsession)

    @fixture
    def command(self, app):
        return UserCommand(app.dbsession)

    @fixture
    def user(self, command):
        uid = uuid4()
        user = User(uid, **self.user_data)
        command.create(user)
        yield user
        command.force_delete(uid)

    def test_find_by_email(self, query, user):
        assert query.find_by_email(self.user_data["email"]).uid == user.uid

    def test_find_by_email_with_no_user(self, query):
        assert query.find_by_email(self.user_data["email"]) is None

    def test_create(self, user):
        assert user.uid
        assert user.created_at
        assert user.updated_at
        assert user.name == self.user_data["name"]
        assert user.email == self.user_data["email"]
        assert user.is_admin == self.user_data["is_admin"]
        assert user.password == self.user_data["password"]

    def test_get_by_uid(self, query, user):
        model = query.get_by_uid(user.uid)
        assert model.uid == user.uid
        assert model.created_at == user.created_at
        assert model.updated_at == user.updated_at
        assert model.name == user.name
        assert model.email == user.email
        assert model.is_admin == user.is_admin
        assert model.password == user.password

    def test_delete(self, command, query, user):
        command.delete(user.uid)

        with raises(NoResultFound):
            query.get_by_uid(user.uid)

        assert list(query.list_active()) == []
        assert len(list(query.list_all())) == 1

    def test_list_active(self, query, user):
        data = list(query.list_active())
        assert len(data) == 1
        assert data[0].uid == user.uid
        assert data[0].created_at == user.created_at
        assert data[0].updated_at == user.updated_at
        assert data[0].name == user.name
        assert data[0].email == user.email
        assert data[0].is_admin == user.is_admin
        assert data[0].password == user.password
