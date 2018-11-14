import walletResource from '@/wallets/resource'

export default {
  namespaced: true,
  state: {
    wallets: [],
    dict: {}
  },
  getters: {
  },
  mutations: {
    setWallets (state, wallets) {
      state.wallets = wallets
      state.dict = {}
      for (let wallet of wallets) {
        state.dict[wallet.uid] = wallet
      }
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
