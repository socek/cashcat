from uuid import uuid4

from pyramid.httpexceptions import HTTPBadRequest
from sapp.decorators import WithContext
from sqlalchemy.exc import IntegrityError

from cashcat import app
from cashcat.application.views import RestfulView
from cashcat.auth.drivers import UserCommand
from cashcat.auth.drivers import UserQuery
from cashcat.auth.jwt import encode_jwt_from_user
from cashcat.auth.models import User
from cashcat.auth.schemas import LoginSchema
from cashcat.auth.schemas import SignUpSchema


class LoginView(RestfulView):
    @property
    @WithContext(app, args=["dbsession"])
    def query(self, dbsession):
        return UserQuery(dbsession)

    def post(self):
        fields = self.get_validated_fields(LoginSchema())
        user = self.get_authenticated_user(fields)
        if user:
            return {"jwt": encode_jwt_from_user(user)}
        else:
            raise HTTPBadRequest(
                json={"_schema": ["Username and/or password do not match."]})

    def get_authenticated_user(self, fields):
        user = self.query.find_by_email(fields["email"])
        if user and user.do_password_match(fields["password"]):
            return user


class SignUpView(RestfulView):
    @property
    @WithContext(app, args=["dbsession"])
    def command(self, dbsession):
        return UserCommand(dbsession)

    def post(self):
        fields = self.get_validated_fields(SignUpSchema())
        try:
            user = self.create_user(fields)
            return {"jwt": encode_jwt_from_user(user)}
        except IntegrityError:
            raise HTTPBadRequest(
                json={"_schema": ["User with that email already exists"]})

    def create_user(self, fields):
        user = User(
            uuid4(),
            name=fields['name'],
            email=fields['email'],
            is_admin=False)
        user.set_password(fields['password'])
        self.command.create(user)
        return user
