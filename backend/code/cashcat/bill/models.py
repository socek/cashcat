from cashcat.application.model import Model


class Bill(Model):

    def __init__(
        self,
        uid,
        created_at=None,
        updated_at=None,
        place=None,
        billed_at=None,
        wallet_uid=None,
    ):
        super().__init__(uid, created_at, updated_at)
        self.place = place
        self.billed_at = billed_at
        self.wallet_uid = wallet_uid
