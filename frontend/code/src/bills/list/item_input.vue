<template>
  <div class="form-row">
    <div role="group" class="form-group col-md-6">
      <input type="text" v-model="value.name.value" class="form-control" placeholder="Nazwa produktu" :class="{'is-invalid': state == 'error'}"  @input="onInput">
      <div class="invalid-feedback" style="display: block;" v-for="message in value.name.errors">{{ message }}</div>
    </div>
    <div role="group" class="form-group col-md-2">
      <input type="number" step="0.00001" v-model="value.quantity.value" class="form-control" placeholder="1.00" :class="{'is-invalid': state == 'error'}"  @input="onInput">
      <div class="invalid-feedback" style="display: block;" v-for="message in value.quantity.errors">{{ message }}</div>
    </div>

    <div role="group" class="form-group col currency">
      <input type="number" v-model="value.value.value" step="0.01"  @blur="formatCurrency()" class="form-control" placeholder="-1,00" @input="onInput" />
      <div class="input-group-append">
        <span class="input-group-text">PLN</span>
      </div>
      <div class="invalid-feedback" style="display: block;" v-for="message in value.value.errors">{{ message }}</div>
    </div>
    <div role="group" class="form-group col currency">
      <b-btn v-if="isDeleteVisible()" size="sm" variant="outline-danger" @click="$emit('removeItem', value._index)" title="Usuń produkt">
        <icon name="plus-circle" />
      </b-btn>
    </div>
  </div>
</template>

<script>
import base from '@/forms/base'

export default {
  extends: base,
  props: {
    index: {
      type: Number,
      required: true
    }
  },
  methods: {
    formatCurrency () {
      let form = this.value
      let currency = form.value.value
      if (currency !== '') {
        form.value.value = Number(currency).toFixed(2)
        this.$emit('input', form)
      }
    },
    onInput () {
      this.$emit('input', this.value)
    },
    isDeleteVisible () {
      let index = this.value._index
      let isLast = this.value._isLast
      return index !== 0 && !isLast
    }
  }
}
</script>
