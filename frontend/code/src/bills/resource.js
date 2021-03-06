export default (vue) => vue.$resource(
  'wallets{/wallet_uid}/bills{/bill_uid}',
  {
    wallet_uid: vue.$route.params.wallet_uid
  },
  {
    list: {method: 'GET'},
    create: {method: 'PUT'},
    update: {method: 'PATCH'}
  }
)
