from sqlalchemy import Binary
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String

from cashcat.application.drivers.dbmodel import DbModel
from cashcat.auth.models import User


class UserData(DbModel):
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

    def from_model(self, obj):
        self.uid = obj.uid
        self.created_at = obj.created_at
        self.updated_at = obj.updated_at
        self.name = obj.name
        self.email = obj.email
        self.is_admin = obj.is_admin
        self.password = obj.password

    def update_model(self, model):
        model.uid = self.uid
        model.created_at = self.created_at
        model.updated_at = self.updated_at
