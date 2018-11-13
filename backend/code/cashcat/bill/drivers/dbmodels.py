from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from cashcat.application.drivers.dbmodel import SqlDataModel
from cashcat.bill.models import Bill
from cashcat.bill.models import BillItem


class BillData(SqlDataModel):
    __tablename__ = "bills"

    place = Column(String, nullable=True)
    billed_at = Column(String, nullable=False)
    wallet_uid = Column(UUID(as_uuid=True), ForeignKey("wallets.uid"), nullable=False)

    def to_model(self):
        return Bill(
            uid=self.uid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            place=self.place,
            billed_at=self.billed_at,
            wallet_uid=self.wallet_uid,
        )

    def from_model(self, model):
        self.uid = model.uid
        self.created_at = model.created_at
        self.updated_at = model.updated_at
        self.place = model.place
        self.billed_at = model.billed_at
        self.wallet_uid = model.wallet_uid


class BillItemData(SqlDataModel):
    __tablename__ = "bill_items"

    name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    value = Column(Float, nullable=False)
    bill_uid = Column(UUID(as_uuid=True), ForeignKey("bills.uid"), nullable=False)
    group_uid = Column(UUID(as_uuid=True), ForeignKey("groups.uid"), nullable=False)

    def to_model(self):
        return BillItem(
            uid=self.uid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            quantity=self.quantity,
            value=self.value,
            bill_uid=self.bill_uid,
            group_uid=self.group_uid,
        )

    def from_model(self, model):
        self.uid = model.uid
        self.created_at = model.created_at
        self.updated_at = model.updated_at
        self.name = model.name
        self.quantity = model.quantity
        self.value = model.value
        self.bill_uid = model.bill_uid
        self.group_uid = model.group_uid
