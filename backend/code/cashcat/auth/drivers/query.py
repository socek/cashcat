from cashcat.application.drivers import Query

from .dbmodels import UserData


class UserQuery(Query):
    model = UserData

    def _get_by_email(self, email):
        return self._query().filter(self.model.email == email)

    def find_by_email(self, email):
        data = self._get_by_email(email).first()
        return data.to_model() if data else None
