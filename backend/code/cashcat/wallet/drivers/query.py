from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound as SANoResultFound

from cashcat.application.drivers import Query
from cashcat.application.drivers.query import NoResultFound

from .dbmodels import WalletData


class WalletQuery(Query):
    model = WalletData

    def _get_active_by_uid(self, uid, owner_uid=None):
        query = self._list_active().filter(self.model.uid == uid)
        if owner_uid:
            query = query.filter(self.model.owner_uid == owner_uid)
        return query

    def get_active_by_uid(self, uid, owner_uid=None):
        try:
            return self._get_active_by_uid(uid, owner_uid).one().to_model()
        except (SANoResultFound, DataError):
            raise NoResultFound

    def _list_for_owner_uid(self, owner_uid):
        return self._list_active().filter(self.model.owner_uid == owner_uid)

    def list_for_owner(self, owner):
        for obj in self._list_for_owner_uid(owner.uid).order_by(self.model.created_at):
            yield obj.to_model()
