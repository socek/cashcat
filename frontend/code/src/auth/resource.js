export default (vue) => vue.$resource('auth', {}, {
  login: {method: 'POST', url: 'auth/login'},
  signUp: {method: 'POST', url: 'auth/signup'}
})
