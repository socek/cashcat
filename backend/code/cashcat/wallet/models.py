from cashcat.application.model import Model


class Wallet(Model):
    def __init__(
        self,
        uid,
        created_at=None,
        updated_at=None,
        name=None,
        type=None,
        owner_uid=None
    ):
        super().__init__(uid, created_at, updated_at)
        self.name = name
        self.type = type
        self.owner_uid = owner_uid

