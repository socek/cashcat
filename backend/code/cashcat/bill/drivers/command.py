from cashcat.application.drivers import Command

from .dbmodels import BillData
from .dbmodels import BillItemData
from .query import BillQuery


class BillCommand(Command):
    model = BillData
    item_data_model = BillItemData
    _query = BillQuery

    def _item_query(self):
        return self.database.query(self.item_data_model)

    def create(self, bill):
        bill_data = self.model()
        bill_data.from_model(bill)
        self.database.add(bill_data)
        self.database.flush()
        subojects = []
        for item in bill.items:
            item_data = self.item_data_model()
            item_data.from_model(item)
            item_data.bill_uid = bill_data.uid
            self.database.add(item_data)
            subojects.append((item, item_data))

        self.database.commit()
        bill_data.update_model(bill)
        for item, item_data in subojects:
            item_data.update_model(item)

    def force_delete(self, uid):
        self._item_query().filter(self.item_data_model.bill_uid == uid).delete()
        self.database.query(self.model).filter(self.model.uid == uid).delete()
        self.database.commit()

    def patch_by_uid(
        self, uid, bill=None, create_items=None, remove_items=None, items_update=None
    ):
        if not (bill or create_items or remove_items or items_update):
            raise RuntimeError("Do not invoke command when nothing to do!")
        if bill:
            self._update_by_uid(uid, bill)
        if create_items:
            for item in create_items:
                item_data = self.item_data_model()
                item_data.from_model(item)
                item_data.bill_uid = uid
                self.database.add(item_data)
        if remove_items:
            for uid in remove_items:
                self._delete_item(uid)
        if items_update:
            for uid, item in items_update.items():
                self._update_item_by_uid(uid, item)
        self.database.commit()

    def _delete_item(self, uid):
        self._update_item_by_uid(uid, {"is_active": False})

    def _update_item_by_uid(self, uid, update):
        update_raw = {}
        for key, value in update.items():
            update_raw[getattr(self.item_data_model, key)] = value
        self._item_query().filter(self.item_data_model.uid == uid).update(update_raw)
