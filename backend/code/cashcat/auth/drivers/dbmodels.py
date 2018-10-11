from sqlalchemy import Binary
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String

from cashcat.application.drivers.dbmodel import SqlDataModel
from cashcat.auth.models import User


class UserData(SqlDataModel):
    __tablename__ = "users"

    name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    password = Column(Binary(100), nullable=True)

    def to_model(self):
        return User(
            uid=self.uid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            email=self.email,
            is_admin=self.is_admin,
            password=self.password)

    def from_model(self, model):
        self.uid = model.uid
        self.created_at = model.created_at
        self.updated_at = model.updated_at
        self.name = model.name
        self.email = model.email
        self.is_admin = model.is_admin
        self.password = model.password

    def update_model(self, model):
        model.uid = self.uid
        model.created_at = self.created_at
        model.updated_at = self.updated_at
