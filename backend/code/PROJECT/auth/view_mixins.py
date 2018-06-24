from pyramid.httpexceptions import HTTPUnauthorized
from sapp.decorators import WithContext
from sqlalchemy.orm.exc import NoResultFound

from PROJECT import app
from PROJECT.application.cache import cache_per_request
from PROJECT.application.views import RestfulView
from PROJECT.auth.drivers import UserQuery
from PROJECT.auth.jwt import decode_jwt


class AuthMixin(object):
    @cache_per_request('user')
    @WithContext(app, args=['dbsession'])
    def get_user(self, dbsession):
        # TODO: think about caching this per request or context?
        user_rd = UserQuery(dbsession)

        payload = self.decoded_jwt()
        return user_rd.get_by_id(payload['id'])

    def is_authenticated(self):
        return self.request.headers.get('JWT') is not None

    def get_user_id(self):
        return self.decoded_jwt()['id']

    def decoded_jwt(self):
        jwt = self.request.headers.get('JWT')
        if jwt:
            return decode_jwt(jwt)
        else:
            raise HTTPUnauthorized()


class AuthenticatedView(RestfulView, AuthMixin):
    def validate(self):
        try:
            self.get_user()
        except NoResultFound:
            raise HTTPUnauthorized()
