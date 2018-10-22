from cashcat.application.drivers import Command

from .dbmodels import BillData
from .dbmodels import BillItemData
from .query import BillQuery


class BillCommand(Command):
    model = BillData
    item_data_model = BillItemData
    _query = BillQuery

    def create(self, bill):
        bill_data = self.model()
        bill_data.from_model(bill)
        self.database.add(bill_data)
        self.database.flush()
        subojects = []
        for item in bill.items:
            item_data = self.item_data_model()
            item_data.from_model(item)
            self.database.add(item_data)
            subojects.append((item, item_data))

        self.database.commit()
        bill_data.update_model(bill)
        for item, item_data in subojects:
            item_data.update_model(item)

    def force_delete(self, uid):
        self.database.query(self.item_data_model).filter(
            self.item_data_model.bill_uid == uid
        ).delete()
        self.database.query(self.model).filter(self.model.uid == uid).delete()
        self.database.commit()
