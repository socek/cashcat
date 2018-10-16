export default (vue) => {
  return vue.$resource('wallet', {}, {
    list: {method: 'GET', url: 'wallets'},
    create: {method: 'PUT', url: 'wallets'}
  })
}
