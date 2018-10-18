from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from cashcat.application.drivers.dbmodel import SqlDataModel
from cashcat.bill.models import Bill


class BillData(SqlDataModel):
    __tablename__ = "bills"

    place = Column(String, nullable=True)
    billed_at = Column(String, nullable=True)
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
