import groupResource from '@/groups/resource'

export default {
  namespaced: true,
  state: {
    groups: [],
    dict: {}
  },
  getters: {
  },
  mutations: {
    setGroups (state, groups) {
      state.groups = groups
      state.dict = {}
      for (let group of groups) {
        state.dict[group.uid] = group
      }
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
