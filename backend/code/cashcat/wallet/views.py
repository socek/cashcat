from uuid import uuid4

from cashcat.application.drivers import driver
from cashcat.auth.view_mixins import AuthenticatedView
from cashcat.wallet.drivers import WalletCommand
from cashcat.wallet.drivers import WalletQuery
from cashcat.wallet.schemas import WalletSchema


class WalletView(AuthenticatedView):
    query = driver(WalletQuery)
    command = driver(WalletCommand)

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
