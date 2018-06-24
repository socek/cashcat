from json.decoder import JSONDecodeError

from marshmallow.exceptions import ValidationError
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotAcceptable
from sapp.decorators import WithContext
from sapp.plugins.pyramid.views import RestfulView as BaseRestfulView

from PROJECT import app


class RestfulView(BaseRestfulView):
    @property
    @WithContext(app, args=['dbsession'])
    def dbsession(self, dbsession):
        return dbsession  # pragma: no cover

    def get_validated_fields(self, schema):
        try:
            return schema.load(self.request.json_body)
        except JSONDecodeError:
            raise HTTPNotAcceptable()
        except ValidationError as error:
            raise HTTPBadRequest(json=error.messages)

    def validate(self):
        pass

    def __call__(self):
        self.validate()
        method = self.methods[self.request.method]
        return method()

    def _object_validation(self, message):
        return HTTPBadRequest(json=[message])
