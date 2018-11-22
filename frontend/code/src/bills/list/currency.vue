<template>
  <div role="group" class="form-group col currency">
    <input
      type="number"
      name="value"
      v-model="data"
      step="0.01"
      @blur="formatCurrency()"
      class="form-control"
      placeholder="-1,00"
      @input="$emit('input', data)">
    <div class="input-group-append">
      <span class="input-group-text">PLN</span>
    </div>
  </div>
</template>

<script>
  export default {
    props: ['value'],
    data () {
      return {
        data: this.value,
        errors: []
      }
    },
    mounted () {
      this.formatCurrency()
    },
    methods: {
      formatCurrency () {
        if (this.data !== '') {
          var num = this.data

          num = Number(num)

          var countDecimals = function (value) {
            if (Math.floor(value) === value) return 0
            return value.toString().split('.')[1].length || 0
          }

          var decimal = countDecimals(num)

          if (decimal < 2) {
            num = num.toFixed(2)
          }

          if (decimal > 2) {
            num = num.toFixed(decimal)
          }
          this.data = num
        }
      }
    }
  }
</script>
