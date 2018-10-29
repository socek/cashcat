<template>
  <dialogform
    title="Nowy portfel"

    ref="form"
    v-model="form"
    @success="$emit('success')"
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

export default {
  data () {
    return {
      form: {
        name: ''
      }
    }
  },
  methods: {
    onSubmit (form) {
      return walletResource(this).create({}, form).then((response) => {
        this.$refs.form.onSuccess()
      }).catch(this.$refs.form.parseErrorResponse)
    }
  }
}
</script>
