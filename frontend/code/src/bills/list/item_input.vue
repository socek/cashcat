<template>
  <div class="form-row">
    <div role="group" class="form-group col-md-6">
      <input type="text" v-model="value.name.value" class="form-control" placeholder="Nazwa produktu" :class="{'is-invalid': state == 'error'}"  @input="onInput">
      <div class="invalid-feedback" style="display: block;" v-for="message in value.name.errors">{{ message }}</div>
    </div>
    <div role="group" class="form-group col-md-2">
      <input type="text" v-model="value.quantity.value" class="form-control" placeholder="1.00" :class="{'is-invalid': state == 'error'}"  @input="onInput">
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
      <b-btn v-if="index !== 0" size="sm" variant="outline-danger" @click="$emit('removeItem', index)" title="Usuń produkt">
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
        currency = Number(currency)

        var countDecimals = function (value) {
          if (Math.floor(value) === value) return 0
          return value.toString().split('.')[1].length || 0
        }

        var decimal = countDecimals(currency)

        if (decimal < 2) {
          currency = currency.toFixed(2)
        }

        if (decimal > 2) {
          currency = currency.toFixed(decimal)
        }
        form.value.value = currency
        this.$emit('input', form)
      }
    },
    onInput () {
      this.$emit('input', this.value)
    }
  }
}
</script>
