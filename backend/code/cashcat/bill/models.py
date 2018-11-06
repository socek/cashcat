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
        items=None,
    ):
        super().__init__(uid, created_at, updated_at)
        self.place = place
        self.billed_at = billed_at
        self.wallet_uid = wallet_uid
        self.items = items or []

    def add_item(
        self,
        uid,
        created_at=None,
        updated_at=None,
        name=None,
        quantity=None,
        value=None,
    ):
        """
        Add item to a bill.
        """
        item = BillItem(uid, created_at, updated_at, name, quantity, value, self.uid)
        self.items.append(item)
        return item


class BillItem(Model):
    def __init__(
        self,
        uid,
        created_at=None,
        updated_at=None,
        name=None,
        quantity=None,
        value=None,
        bill_uid=None,
    ):
        super().__init__(uid, created_at, updated_at)
        self.name = name
        self.quantity = quantity
        self.value = value
        self.bill_uid = bill_uid
