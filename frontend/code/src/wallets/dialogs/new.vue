<template>
  <dialogform
    title="Nowy portfel"

    ref="dialog"
    v-model="form"
    @submit="onSubmit">

    <template slot="anhor">
      <icon name="plus-circle" />
    </template>

    <template slot="content">
      <text-input v-model="form.name" label="Nazwa" placeholder="prywatny"></text-input>
    </template>
  </dialogform>
</template>

<script>
import walletResource from '@/wallets/resource'
import form from '@/forms'

export default {
  data () {
    return {
      form: form({
        name: ''
      })
    }
  },
  methods: {
    onSubmit (form) {
      form.submit(
        () => walletResource(this).create({}, form.toData()),
        (response) => {
          this.$store.dispatch('wallets/fetchWallets')
          this.$refs.dialog.hide()
        }
      )
    }
  }
}
</script>
