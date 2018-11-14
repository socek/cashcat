<template>
  <dialogform
    title="Usuń portfel"

    ref="form"
    v-model="form"
    @success="$emit('success')"
    @submit="onSubmit">

    <template slot="anhor">
      <icon name="trash" />
    </template>

    <template slot="content">
      <p>Czy na pewno chcesz usunąć ten portfel?</p>
      <p>Nazwa: <strong>{{ wallet().name }}</strong></p>
    </template>
  </dialogform>
</template>

<script>
import walletResource from '@/wallets/resource'

export default {
  props: ['wallet_uid'],
  data () {
    return {
      form: {}
    }
  },
  methods: {
    wallet () {
      return this.$store.state.wallets.dict[this.wallet_uid]
    },
    onSubmit (form) {
      return walletResource(this).delete({wallet_uid: this.wallet_uid}, {}).then((response) => {
        this.$store.dispatch('wallets/fetchWallets')
        this.$refs.form.onSuccess()
      }).catch(this.$refs.form.parseErrorResponse)
    }
  }
}
</script>
