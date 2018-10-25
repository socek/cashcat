<template>
  <div class="col input-group">
    <input type="number" name="price" v-model="data" step="0.01"  @blur="formatDollars()" class="form-control currency" required/>
    <div class="input-group-append">
      <span class="input-group-text">zł</span>
    </div>
    <b-form-invalid-feedback v-for="error in errors" :key="error">
      {{ error }}
    </b-form-invalid-feedback>
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
      this.formatDollars()
    },
    methods: {
      stripTheGarbage (e) {
        if (e.keyCode < 48 && e.keyCode !== 46 || e.keyCode > 59) {
          e.preventDefault()
        }
      },
      formatDollars () {
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
          this.$emit('change', this.data)
        }
      }
    }
  }
</script>
