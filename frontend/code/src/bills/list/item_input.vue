<template>
  <div class="form-row">
    <div class="col">
      <b-form-input id="billItemField"
                    type="text"
                    placeholder="produkt"
                    v-model.trim="item.name"
                    @change="onChange"
                    :state="errors.name.length == 0 ? null : false">
      </b-form-input>
      <b-form-invalid-feedback v-for="error in errors.name" :key="error">
        {{ error }}
      </b-form-invalid-feedback>
    </div>
    <div class="col">
      <b-form-input id="billItemField"
                    type="number"
                    step="0.01"
                    placeholder="ilość"
                    v-model.number="item.quantity"
                    @change="onChange"
                    :state="errors.quantity.length == 0 ? null : false">
      </b-form-input>
      <b-form-invalid-feedback v-for="error in errors.quantity" :key="error">
        {{ error }}
      </b-form-invalid-feedback>
    </div>
    <currency :value="item.value" @change="onChangeCurrency" />
  </div>
</template>

<script>
import currency from '@/bills/list/currency'
export default {
  props: ['item'],
  data () {
    return {
      errors: {
        name: [],
        quantity: [],
        value: []
      }
    }
  },
  methods: {
    onChange () {
      this.$emit('change')
    },
    onChangeCurrency (value) {
      this.item.value = value
      console.log('changed value!', value)
      this.$emit('change')
    }
  },
  components: {
    currency
  }
}
</script>
