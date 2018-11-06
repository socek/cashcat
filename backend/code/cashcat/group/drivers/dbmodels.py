from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from cashcat.application.drivers.dbmodel import SqlDataModel
from cashcat.group.models import Group


class GroupData(SqlDataModel):
    __tablename__ = "groups"

    name = Column(String, nullable=True)
    wallet_uid = Column(UUID(as_uuid=True), ForeignKey("wallets.uid"), nullable=False)

    def to_model(self):
        return Group(
            uid=self.uid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            wallet_uid=self.wallet_uid,
        )

    def from_model(self, model):
        self.uid = model.uid
        self.created_at = model.created_at
        self.updated_at = model.updated_at
        self.name = model.name
        self.wallet_uid = model.wallet_uid
