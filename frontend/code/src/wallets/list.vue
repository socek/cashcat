<template>
  <div>List
  </div>
</template>

<script>
import walletResource from '@/wallets/resource'

export default {
  data () {
    return {
      resource: walletResource(this)
    }
  },
  mounted () {
    this.resource.list({}, this.fields).then((response) => {
      console.log(response)
    })
  }
}
</script>
