import walletResource from '@/wallets/resource'

export default {
  namespaced: true,
  state: {
    wallets: []
  },
  getters: {
  },
  mutations: {
    setWallets (state, wallets) {
      state.wallets = wallets
    }
  },
  actions: {
    fetchWallets: (state) => {
      let resource = walletResource(state.rootState.vue)
      resource.list({}).then((response) => {
        state.commit('setWallets', response.data)
      })
    }
  }
}
