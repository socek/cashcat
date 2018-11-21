export default (vue) => vue.$resource('wallets{/wallet_uid}', {}, {
  list: {method: 'GET'},
  create: {method: 'PUT'},
  update: {method: 'PATCH'},
  delete: {method: 'DELETE'}
})
