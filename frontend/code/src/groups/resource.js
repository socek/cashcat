export default (vue) => {
  return vue.$resource(
    'wallets{/wallet_uid}/groups{/group_uid}',
    {
      wallet_uid: vue.$route.params.wallet_uid
    },
    {
      list: {method: 'GET'},
      create: {method: 'PUT'},
      update: {method: 'PATCH'}
    }
  )
}
