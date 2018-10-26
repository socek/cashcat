<template>
  <dialogform
    title="Edytuj portfel"
    :fetchContent="fetchContent"
    :saveCall="saveCall"
    @success="$emit('success')">

      <template slot="anhor">
        <icon name="edit"></icon>
      </template>

      <template slot="content">
        <text-input name="name" placeholder="Prywatny" label="Nazwa"></text-input>
      </template>
  </dialogform>


</template>

<script>
import walletResource from '@/wallets/resource'

export default {
  props: ['wallet_uid'],
  data () {
    return {
      resource: walletResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({wallet_uid: this.wallet_uid})
    },
    saveCall (form) {
      return this.resource.update({wallet_uid: this.wallet_uid}, form.fields)
    }
  }
}
</script>
