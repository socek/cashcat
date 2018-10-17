def wallet_routing(routing):
    routing.add("cashcat.wallet.views.WalletsView", "wallets", "/wallets")
    routing.add("cashcat.wallet.views.WalletView", "wallet", "/wallets/{wallet_uid}")
