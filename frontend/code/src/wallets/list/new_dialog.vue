<template>
  <dialogform
    title="Nowy portfel"
    :saveCall="saveCall"
    @success="$emit('success')">

    <template slot="anhor">
      <icon name="plus-circle" />
    </template>

    <template slot="content">
      <text-input name="name" label="Nazwa" placeholder="prywatny"></text-input>
    </template>
  </dialogform>
</template>

<script>
import walletResource from '@/wallets/resource'

export default {
  methods: {
    saveCall (form) {
      return walletResource(this).create({}, form.fields)
    }
  }
}
</script>
