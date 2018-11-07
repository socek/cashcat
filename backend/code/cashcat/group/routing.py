def group_routing(routing):
    routing.add(
        "cashcat.group.views.GroupsView", "groups", "/wallets/{wallet_uid}/groups"
    )
    routing.add(
        "cashcat.group.views.GroupView",
        "group",
        "/wallets/{wallet_uid}/groups/{group_uid}",
    )
