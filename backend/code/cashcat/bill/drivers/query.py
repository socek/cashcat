from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound as SANoResultFound
from sqlalchemy.sql import func

from cashcat.application.drivers import Query
from cashcat.application.drivers.query import NoResultFound

from .dbmodels import BillData
from .dbmodels import BillItemData


class BillQuery(Query):
    model = BillData
    item_data_model = BillItemData

    def _get_active_by_uid(self, uid, wallet_uid=None):
        query = self._list_active().filter(self.model.uid == uid)
        if wallet_uid:
            query = query.filter(self.model.wallet_uid == wallet_uid)
        return query

    def get_active_by_uid(self, uid, wallet_uid=None, with_items=False):
        try:
            bill = self._get_active_by_uid(uid, wallet_uid).one().to_model()
            if with_items:
                bill.items = [obj.to_model() for obj in self._get_active_items(uid)]
            return bill
        except (SANoResultFound, DataError):
            raise NoResultFound

    def _list_for_wallet_uid(self, wallet_uid):
        return (
            self.database.query(
                self.model.uid,
                self.model.place,
                self.model.billed_at,
                self.model.wallet_uid,
                func.sum(self.item_data_model.total).label("total"),
            )
            .outerjoin(self.item_data_model)
            .filter(self.model.is_active.is_(True))
            .filter(self.model.wallet_uid == wallet_uid)
            .group_by(self.model.uid)
        )

    def list_for_wallet(self, wallet_uid):
        return self._list_for_wallet_uid(wallet_uid).order_by(self.model.created_at)

    def _get_active_items(self, bill_uid):
        return self.database.query(self.item_data_model).filter(
            self.item_data_model.bill_uid == bill_uid,
            self.item_data_model.is_active.is_(True),
        )
