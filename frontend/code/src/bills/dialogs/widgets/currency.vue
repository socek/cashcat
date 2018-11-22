<template>
  <div role="group" class="form-group col currency">
    <input
      type="number"
      step="0.01"
      placeholder="-1,00"

      v-model="value.value"
      :class="getClass()"
      @blur="formatCurrency()"
      @input="sendUpdate()">
    <div class="input-group-append">
      <span class="input-group-text">PLN</span>
    </div>
    <div class="invalid-feedback" style="display: block;" v-for="message in value.errors">{{ message }}</div>
  </div>
</template>

<script>
  import base from './base'

  export default {
    extends: base,
    mounted () { this.formatCurrency() },
    methods: {
      formatCurrency () {
        let currency = this.value.value
        if (currency !== '') {
          this.value.value = Number(currency).toFixed(2)
          this.sendUpdate()
        }
      }
    }
  }
</script>
