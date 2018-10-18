from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound as SANoResultFound

from cashcat.application.drivers import Query
from cashcat.application.drivers.query import NoResultFound

from .dbmodels import BillData


class BillQuery(Query):
    model = BillData

    def _get_active_by_uid(self, uid, wallet_uid=None):
        query = self._list_active().filter(self.model.uid == uid)
        if wallet_uid:
            query = query.filter(self.model.wallet_uid == wallet_uid)
        return query

    def get_active_by_uid(self, uid, wallet_uid=None):
        try:
            return self._get_active_by_uid(uid, wallet_uid).one().to_model()
        except (SANoResultFound, DataError):
            raise NoResultFound

    def _list_for_wallet_uid(self, wallet_uid):
        return self._list_active().filter(self.model.wallet_uid == wallet_uid)

    def list_for_wallet(self, wallet_uid):
        for obj in self._list_for_wallet_uid(wallet_uid).order_by(self.model.created_at):
            yield obj.to_model()
