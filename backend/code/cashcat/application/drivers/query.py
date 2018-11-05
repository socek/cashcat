from uuid import UUID

from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound as SANoResultFound

from sapp.plugins.sqlalchemy.driver import Query as BaseQuery


class NoResultFound(Exception):
    pass


class Query(BaseQuery):
    """
    You need to set up:
    - model
    """

    def get_by_uid(self, uid):
        try:
            isinstance(uid, UUID) or UUID(uid)
        except (ValueError, AttributeError):
            raise NoResultFound

        try:
            return self._get_by_uid(uid).one().to_model()
        except (SANoResultFound, DataError):
            raise NoResultFound

    def list_all(self):
        for obj in self._query():
            yield obj.to_model()

    def _list_active(self):
        return self._query().filter(self.model.is_active.is_(True))

    def _get_by_uid(self, uid):
        return self._list_active().filter(self.model.uid == uid)

    def list_active(self):
        for obj in self._list_active().order_by(self.model.created_at):
            yield obj.to_model()
