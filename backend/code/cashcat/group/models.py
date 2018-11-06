from cashcat.application.model import Model


class Group(Model):

    def __init__(
        self,
        uid,
        created_at=None,
        updated_at=None,
        name=None,
        wallet_uid=None,
    ):
        super().__init__(uid, created_at, updated_at)
        self.name = name
        self.wallet_uid = wallet_uid

