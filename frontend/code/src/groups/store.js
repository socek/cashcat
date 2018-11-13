import groupResource from '@/groups/resource'

export default {
  namespaced: true,
  state: {
    groups: []
  },
  getters: {
  },
  mutations: {
    setGroups (state, groups) {
      state.groups = groups
    }
  },
  actions: {
    fetchGroups: (state) => {
      let resource = groupResource(state.rootState.vue)
      resource.list({}).then((response) => {
        state.commit('setGroups', response.data)
      })
    }
  }
}
