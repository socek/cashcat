from uuid import uuid4

from pyramid.httpexceptions import HTTPNotFound

from cashcat.application.cache import cache_per_request
from cashcat.application.drivers import driver
from cashcat.application.drivers.query import NoResultFound
from cashcat.auth.view_mixins import AuthenticatedView
from cashcat.wallet.drivers import WalletCommand
from cashcat.wallet.drivers import WalletQuery
from cashcat.wallet.schemas import WalletSchema


class BaseView(AuthenticatedView):
    wallet_query = driver(WalletQuery)
    wallet_command = driver(WalletCommand)


class BaseWalletView(BaseView):
    def validate(self):
        super().validate()
        self._get_wallet()

    @cache_per_request("wallet")
    def _get_wallet(self):
        try:
            return self.wallet_query().get_active_by_uid(
                self.request.matchdict["wallet_uid"], self.get_user().uid
            )
        except NoResultFound:
            raise HTTPNotFound()


class WalletsView(BaseView):
    def get(self):
        """
        Get list of wallets.
        """
        owner = self.get_user()
        wallets = self.wallet_query().list_for_owner(owner)
        schema = WalletSchema(many=True)
        return schema.dump(wallets)

    def put(self):
        """
        Create new wallet for logged in user.
        """
        schema = WalletSchema()
        wallet = self.get_validated_fields(schema, partial=("uid", "type", "owner_uid"))
        wallet.uid = uuid4()
        wallet.type = "private"
        wallet.owner_uid = self.get_user().uid
        self.wallet_command().create(wallet)
        return schema.dump(wallet)


class WalletView(BaseWalletView):
    def get(self):
        """
        Get wallet data.
        """
        return WalletSchema().dump(self._get_wallet())

    def patch(self):
        """
        Update wallet data.
        """
        schema = WalletSchema(partial=("uid", "type", "owner_uid"))
        wallet = self.get_validated_fields(schema)
        self.wallet_command().update_by_uid(
            self.request.matchdict["wallet_uid"], {"name": wallet.name}
        )

    def delete(self):
        """
        Soft delete wallet.
        """
        self.wallet_command().delete(self.request.matchdict["wallet_uid"])
