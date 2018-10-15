from cashcat.application.drivers import Query

from .dbmodels import WalletData


class WalletQuery(Query):
    model = WalletData

    def _list_for_owner(self, owner):
        return self._list_active().filter(self.model.owner_uid == owner.uid)

    def list_for_owner(self, owner):
        for obj in self._list_for_owner(owner):
            yield obj.to_model()
