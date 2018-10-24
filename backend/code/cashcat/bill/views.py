from uuid import uuid4

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotFound

from cashcat.application.cache import cache_per_request
from cashcat.application.drivers import driver
from cashcat.application.drivers.query import NoResultFound
from cashcat.bill.drivers import BillCommand
from cashcat.bill.drivers import BillQuery
from cashcat.bill.patcher import BillPatcher
from cashcat.bill.patcher import PatchError
from cashcat.bill.schemas import BillSchema
from cashcat.bill.schemas import PatchSchema
from cashcat.wallet.views import BaseWalletView


class BaseView(BaseWalletView):
    bill_query = driver(BillQuery)
    bill_command = driver(BillCommand)


class BillsView(BaseView):
    def get(self):
        """
        Get list of bills.
        """
        wallet = self._get_wallet()
        bills = self.bill_query().list_for_wallet(wallet.uid)
        schema = BillSchema(many=True)
        return schema.dump(bills)

    def put(self):
        """
        Create new bill for logged in user.
        """
        schema = BillSchema()
        bill = self.get_validated_fields(schema, partial=("uid", "wallet_uid"))
        bill.uid = uuid4()
        bill.wallet_uid = self._get_wallet().uid
        self.bill_command().create(bill)
        return schema.dump(bill)


class BillView(BaseView):
    def validate(self):
        super().validate()
        self._get_bill()

    def get(self):
        """
        Get bill data.
        """
        return BillSchema().dump(self._get_bill())

    def patch(self):
        """
        Update bill data.
        """
        patches = self.get_validated_fields(PatchSchema(many=True))
        patcher = BillPatcher(patches)
        try:
            result = patcher.make()
        except PatchError as error:
            raise HTTPBadRequest(json={"message": error.message, "patch": error.patch})

        self.bill_command().patch_by_uid(
            self.request.matchdict["bill_uid"],
            *result,
        )

    @cache_per_request("bill")
    def _get_bill(self):
        try:
            return self.bill_query().get_active_by_uid(
                self.request.matchdict["bill_uid"], self.get_user().uid
            )
        except NoResultFound:
            raise HTTPNotFound()
