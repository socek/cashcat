<template>
  <dialogform
    title="Edytuj portfel"

    :fetchContent="fetchContent"
    ref="form"
    v-model="form"
    @success="$emit('success')"
    @submit="onSubmit">

      <template slot="anhor">
        <icon name="edit"></icon>
      </template>

      <template slot="content">
        <text-input v-model="form.name" placeholder="Prywatny" label="Nazwa"></text-input>
      </template>
  </dialogform>


</template>

<script>
import walletResource from '@/wallets/resource'

export default {
  props: ['wallet_uid'],

  data () {
    return {
      form: {
        name: ''
      },
      resource: walletResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({wallet_uid: this.wallet_uid})
    },
    onSubmit (form) {
      walletResource(this).update({wallet_uid: this.wallet_uid}, form).then((response) => {
        this.$store.dispatch('wallets/fetchWallets')
        this.$refs.form.onSuccess()
      }).catch(this.$refs.form.parseErrorResponse)
    }
  }
}
</script>
