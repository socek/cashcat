from calendar import monthrange
from datetime import datetime
from uuid import uuid4

from pyramid.httpexceptions import HTTPNotFound

from cashcat.application.cache import cache_per_request
from cashcat.application.drivers import driver
from cashcat.application.drivers.query import NoResultFound
from cashcat.group.drivers import GroupCommand
from cashcat.group.drivers import GroupQuery
from cashcat.group.schemas import GroupAggregationSchema
from cashcat.group.schemas import GroupSchema
from cashcat.wallet.views import BaseWalletView


class BaseView(BaseWalletView):
    group_query = driver(GroupQuery)
    group_command = driver(GroupCommand)


class GroupsView(BaseView):
    def get(self):
        """
        Get list of groups.
        """
        wallet = self._get_wallet()
        start, end = self._get_start_and_end()
        groups = self.group_query().summary_for_period(wallet.uid, start, end)
        schema = GroupAggregationSchema(many=True)
        return schema.dump(groups)

    def _get_start_and_end(self):
        month_string = self.request.GET.get("month")
        if month_string:
            date = datetime.strptime(month_string, "%Y-%m")
        else:
            date = datetime.utcnow()
        year = date.year
        month = date.month
        first_day, last_day = monthrange(year, month)
        return (datetime(year=year, month=month, day=first_day),
                datetime(year=year, month=month, day=last_day))

    def put(self):
        """
        Create new group for logged in user.
        """
        schema = GroupSchema()
        group = self.get_validated_fields(
            schema, partial=("uid", "wallet_uid"))
        group.uid = uuid4()
        group.wallet_uid = self._get_wallet().uid
        self.group_command().create(group)
        return schema.dump(group)


class GroupView(BaseView):
    def validate(self):
        super().validate()
        self._get_group()

    def get(self):
        """
        Get group data.
        """
        return GroupSchema().dump(self._get_group())

    def patch(self):
        """
        Update group data.
        """
        schema = GroupSchema(partial=("uid", "wallet_uid"))
        group = self.get_validated_fields(schema)
        self.group_command().update_by_uid(self.request.matchdict["group_uid"],
                                           {"name": group.name})

    @cache_per_request("group")
    def _get_group(self):
        try:
            return self.group_query().get_active_by_uid(
                self.request.matchdict["group_uid"],
                self.request.matchdict["wallet_uid"],
            )
        except NoResultFound:
            raise HTTPNotFound()
