from cashcat.application.model import Model


class Wallet(Model):
    types = {"private": "private", "vat": "vat"}

    def __init__(
        self,
        uid,
        created_at=None,
        updated_at=None,
        name=None,
        type=None,
        owner_uid=None,
    ):
        super().__init__(uid, created_at, updated_at)
        self.name = name
        self.type = type
        self.owner_uid = owner_uid
        if self.type and self.type not in self.types:
            raise RuntimeError("Wrong wallet type: {}".format(self.type))

    def is_accessible_by(self, user):
        """
        User has access only if he/she is owner of this wallet.
        """
        return self.owner_uid == user.uid
