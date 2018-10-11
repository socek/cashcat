from sapp.plugins.sqlalchemy.driver import Command as BaseCommand


class Command(BaseCommand):
    """
    You need to set up:
    - model
    - _query
    """

    @property
    def query(self):
        return self._query(self.database)

    def create(self, model):
        obj = self.model()
        obj.from_model(model)
        self.database.add(obj)
        self.database.commit()
        obj.update_model(model)

    def update_by_uid(self, uid, update):
        update_raw = {}
        for key, value in update.items():
            update_raw[getattr(self.model, key)] = value
        self.query._get_by_uid(uid).update(update_raw)
        self.database.commit()

    def delete(self, uid):
        self.update_by_uid(uid, {"is_active": False})
        self.database.commit()

    def force_delete(self, uid):
        self.database.query(self.model).filter(self.model.uid == uid).delete()
        self.database.commit()
