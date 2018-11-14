<template>
  <div>
    <groups ref="groups"></groups>
    <bills  ref="bills"></bills>
  </div>
</template>

<script>
  import bills from '@/bills/list/list'
  import groups from '@/groups/list/component'

  export default {
    watch: {
      '$route': 'fetchData'
    },
    methods: {
      fetchData () {
        this.$refs.bills.fetchData()
        this.$store.dispatch('groups/fetchGroups')
      }
    },
    components: {
      bills,
      groups
    }
  }
</script>
