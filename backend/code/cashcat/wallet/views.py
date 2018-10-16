from sapp.decorators import WithContext

from cashcat import app
from cashcat.auth.view_mixins import AuthenticatedView
from cashcat.wallet.drivers import WalletQuery
from cashcat.wallet.schemas import WalletSchema


class WalletView(AuthenticatedView):
    @WithContext(app, args=["dbsession"])
    def query(self, dbsession):
        return WalletQuery(dbsession)

    def get(self):
        owner = self.get_user()
        wallets = self.query().list_for_user(owner)
        schema = WalletSchema(many=True)
        return schema.dump(wallets)
