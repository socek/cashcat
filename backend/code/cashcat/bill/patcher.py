from collections import defaultdict

from cashcat.bill.models import BillItem


class PatchError(Exception):
    def __init__(self, patch, message):
        self.message = message
        self.patch = patch


class BillPatcher(object):
    def __init__(self, patches):
        self.patches = patches
        self.bill_update = {}
        self.items_update = defaultdict(lambda: {})
        self.create_items = []
        self.remove_items = []

    def make(self):
        for patch in self.patches:
            if patch["op"] == "replace":
                self._replace(patch)
            elif patch["op"] == "add":
                self._create_item(patch)
            elif patch["op"] == "remove":
                self._remove_item(patch)
            else:
                self._parse_error(
                    patch, "This json patch implementation does not support operant"
                )
        return (
            self.bill_update,
            self.create_items,
            self.remove_items,
            dict(self.items_update),
        )

    def _replace(self, patch):
        key = patch["path"].split("/", 1)[1]
        if key in ["place", "billed_at"]:
            self._replace_bill(key, patch)
        elif key.startswith("items/"):
            self._replace_item(patch)
        else:
            self._parse_error(
                patch, "Only allow to replace: /place, /billed_at or /items/{uid}/{key}"
            )

    def _replace_bill(self, key, patch):
        self.bill_update[key] = patch["value"]

    def _replace_item(self, patch):
        try:
            _, _, uid, key = patch["path"].split("/")
        except ValueError:
            self._parse_error(
                patch, "Only allow to replace: /place, /billed_at or /items/{uid}/{key}"
            )
        if key in ["name", "quantity", "value"]:
            self.items_update[uid][key] = patch["value"]
        else:
            self._parse_error(
                patch, "Only allow to replace: /place, /billed_at or /items/{uid}/{key}"
            )

    def _create_item(self, patch):
        return self.create_items.append(BillItem(None, **patch["value"]))

    def _remove_item(self, patch):
        return self.remove_items.append(patch["value"])

    def _parse_error(self, patch, message):
        raise PatchError(patch, message)
