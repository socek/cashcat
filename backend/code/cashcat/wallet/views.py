from sapp.decorators import WithContext

from cashcat import app
from cashcat.auth.view_mixins import AuthenticatedView
from cashcat.wallet.drivers import WalletQuery


class WalletView(AuthenticatedView):
    @property
    @WithContext(app, args=["dbsession"])
    def query(self, dbsession):
        return WalletQuery(dbsession)

    def get(self):
        return self.query.list_for_user()
