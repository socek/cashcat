from sqlalchemy import DateTime
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound as SANoResultFound
from sqlalchemy.sql import and_
from sqlalchemy.sql import cast
from sqlalchemy.sql import func
from sqlalchemy.sql import or_

from cashcat.application.drivers import Query
from cashcat.application.drivers.query import NoResultFound
from cashcat.bill.drivers.dbmodels import BillData
from cashcat.bill.drivers.dbmodels import BillItemData
from cashcat.wallet.drivers.dbmodels import WalletData

from .dbmodels import GroupData


class GroupQuery(Query):
    model = GroupData

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

    def list_for_wallet(self, wallet):
        for obj in self._list_for_wallet_uid(wallet.uid).order_by(
            self.model.created_at
        ):
            yield obj.to_model()

    def summary_for_period(self, wallet_uid, start, end):
        """
        Get summary aggregation of groups from a provided period.
        """
        return (
            self.database.query(
                self.model.uid,
                self.model.name,
                func.sum(BillItemData.total).label('total'),
                func.count(BillItemData.uid).label('items'),
            )
            .join(BillItemData, full=True)
            .join(BillData, full=True)
            .filter(
                or_(
                    BillData.billed_at.is_(None),
                    and_(
                        cast(BillData.billed_at, DateTime) >= start,
                        cast(BillData.billed_at, DateTime) <= end
                    )
                )
            )
            .filter(self.model.is_active.is_(True))
            .filter(BillItemData.is_active.isnot(False))
            .filter(BillData.is_active.isnot(False))
            .filter(WalletData.is_active.is_(True))
            .group_by(self.model.uid)
        ).all()
