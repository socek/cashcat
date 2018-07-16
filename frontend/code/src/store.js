import Vue from 'vue'
import Vuex from 'vuex'

import auth from '@/auth/store'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    vue: null
  },
  getters: {
    vue (state) {
      return state.vue
    },
    $route (state) {
      return state.vue.$route
    }
  },
  mutations: {
    init: (state, vue) => {
      state.vue = vue
    }
  },
  modules: {
    auth
  }
})
