from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from cashcat.application.drivers.dbmodel import SqlDataModel
from cashcat.wallet.models import Wallet


class WalletData(SqlDataModel):
    __tablename__ = "wallets"

    name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    owner_uid = Column(UUID(as_uuid=True), ForeignKey("users.uid"), nullable=False)

    def to_model(self):
        return Wallet(
            uid=self.uid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            type=self.type,
            owner_uid=self.owner_uid,
        )

    def from_model(self, model):
        self.uid = model.uid
        self.created_at = model.created_at
        self.updated_at = model.updated_at
        self.name = model.name
        self.type = model.type
        self.owner_uid = model.owner_uid
