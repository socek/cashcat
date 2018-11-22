<template>
  <div class="form-row">
    <name v-model="value.name" @input="onInput" />
    <group v-model="value.group_uid" @input="onSelectInput" />
    <quantity v-model="value.quantity" @input="onInput" ref="quantity" />
    <currency v-model="value.value" @input="onInput" />

    <div role="group" class="form-group col currency">
      <b-btn
        v-if="isDeleteVisible()"
        size="sm"
        variant="outline-danger"
        title="Usuń produkt"
        @click="$emit('removeItem', value)">
        <icon name="plus-circle" />
      </b-btn>
    </div>
  </div>
</template>

<script>
import base from '@/forms/base'

import currency from './currency'
import name from './name'
import group from './group'
import quantity from './quantity'

export default {
  extends: base,
  methods: {
    onSelectInput () {
      this.onInput()
      this.$refs.quantity.focus()
    },
    onInput () {
      this.$emit('input', this.value)
    },
    isDeleteVisible () {
      let isLast = this.value._isLast
      return !isLast
    }
  },
  components: {
    name,
    group,
    quantity,
    currency
  }
}
</script>
