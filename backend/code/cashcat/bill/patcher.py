class BillPatcher(object):
    _bill_keys = ["place", "billed_at"]
    _item_keys = ["name", "quantity", "value", "group_uid"]

    def __init__(self, old_object, new_object):
        self.old_object = old_object
        self.new_object = new_object
        self.new_object.billed_at = self.new_object.billed_at.isoformat()

    def make(self):
        return (
            self._create_bill_diff(),
            self._create_new_items_list(),
            self._create_removed_items_list(),
            self._create_items_diff(),
        )

    def _create_bill_diff(self):
        diff = {}
        for key in self._bill_keys:
            old_value = getattr(self.old_object, key)
            new_value = getattr(self.new_object, key)
            if old_value != new_value:
                diff[key] = new_value
        return diff

    def _create_new_items_list(self):
        return [item for item in self.new_object.items if not item.uid]

    def _create_removed_items_list(self):
        old_uids = [item.uid for item in self.old_object.items if item.uid]
        new_uids = [item.uid for item in self.new_object.items if item.uid]
        return [uid for uid in old_uids if uid not in new_uids]

    def _create_items_diff(self):
        diff = {}
        new_items = {item.uid: item for item in self.new_object.items if item.uid}
        for old_item in self.old_object.items:
            new_item = new_items.get(old_item.uid)
            if not new_item:
                continue
            item_diff = self._create_bill_item_diff(old_item, new_item)
            if item_diff:
                diff[old_item.uid] = item_diff
        return diff

    def _create_bill_item_diff(self, old_item, new_item):
        diff = {}
        for key in self._item_keys:
            old_value = getattr(old_item, key)
            new_value = getattr(new_item, key)
            if old_value != new_value:
                diff[key] = new_value
        return diff
