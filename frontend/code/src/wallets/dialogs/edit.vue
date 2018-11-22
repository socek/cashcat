<template>
  <dialogform
    title="Edytuj portfel"

    :fetchContent="fetchContent"
    ref="dialog"
    v-model="form"
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
import form from '@/forms'

export default {
  props: ['wallet_uid'],

  data () {
    return {
      form: form({
        name: ''
      }),
      resource: walletResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({wallet_uid: this.wallet_uid})
    },
    onSubmit (form) {
      form.submit(
        () => walletResource(this).update(
          {wallet_uid: this.wallet_uid},
          form.toData()),
        (response) => {
          this.$store.dispatch('wallets/fetchWallets')
          this.$refs.dialog.hide()
        }
      )
    }
  }
}
</script>
