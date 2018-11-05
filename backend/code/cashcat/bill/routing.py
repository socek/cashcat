def bill_routing(routing):
    routing.add("cashcat.bill.views.BillsView", "bills", "/wallets/{wallet_uid}/bills")
    routing.add(
        "cashcat.bill.views.BillView", "bill", "/wallets/{wallet_uid}/bills/{bill_uid}"
    )
