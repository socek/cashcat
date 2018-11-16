import store from '@/store'

export default {
  install (Vue, options) {
    Vue.http.interceptors.push((request, next) => {
      if (store.state.auth.jwt) {
        request.headers.set('JWT', store.state.auth.jwt)
      }
      next()
    })

    store.dispatch('auth/tryAutoLogin')
  }
}
