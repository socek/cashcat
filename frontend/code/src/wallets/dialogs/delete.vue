<template>
  <dialogform title="Usuń portfel" ref="dialog" v-model="form" @submit="onSubmit">
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
import form from '@/forms'

export default {
  props: ['wallet_uid'],
  data () {
    return {
      form: form({})
    }
  },
  methods: {
    wallet () {
      return this.$store.state.wallets.dict[this.wallet_uid]
    },
    onSubmit (form) {
      form.submit(
        () => walletResource(this).delete({wallet_uid: this.wallet_uid}, {}),
        (response) => {
          this.$store.dispatch('wallets/fetchWallets')
          this.$refs.dialog.hide()
        }
      )
    }
  }
}
</script>
