<template>
  <div>
    <div class="d-flex align-items-center justify-content-center">
      <monthly-picker @selected="onChangeMonth" :value="month"></monthly-picker>
    </div>
    <groups ref="groups"></groups>
    <bills  ref="bills"></bills>
  </div>
</template>

<script>
  import bills from '@/bills/list/list'
  import groups from '@/groups/list/component'
  import monthlyPicker from 'vue-monthly-picker'

  export default {
    watch: {
      '$route': 'fetchData'
    },
    methods: {
      fetchData () {
        this.$refs.bills.fetchData()
        this.$store.dispatch('groups/fetchGroups')
      },
      onChangeMonth (value) {
        this.$store.commit('month/setMonth', value)
        this.$store.dispatch('groups/fetchGroups')
        this.$refs.bills.fetchData()
      }
    },
    components: {
      bills,
      groups,
      monthlyPicker
    },
    computed: {
      month () {
        return this.$store.state.month.month
      }
    }
  }
</script>
