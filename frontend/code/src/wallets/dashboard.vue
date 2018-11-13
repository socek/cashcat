<template>
  <div>
    <groups></groups>
    <bills></bills>
  </div>
</template>

<script>
  import bills from '@/bills/list/list'
  import groups from '@/groups/list/list'

  export default {
    components: {
      bills,
      groups
    }
  }
</script>
