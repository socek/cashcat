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
    query = driver(WalletQuery)
    command = driver(WalletCommand)


class WalletsView(BaseView):
    def get(self):
        """
        Get list of wallets.
        """
        owner = self.get_user()
        wallets = self.query().list_for_owner(owner)
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
        self.command().create(wallet)
        return schema.dump(wallet)


class WalletView(BaseView):
    def validate(self):
        super().validate()
        user = self.get_user()
        wallet = self._get_wallet()
        if not wallet.is_accessible_by(user):
            raise HTTPNotFound()

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
        self.command().update_by_uid(
            self.request.matchdict["wallet_uid"], {"name": wallet.name}
        )

    @cache_per_request("wallet")
    def _get_wallet(self):
        try:
            return self.query().get_by_uid(self.request.matchdict["wallet_uid"])
        except NoResultFound:
            raise HTTPNotFound()
