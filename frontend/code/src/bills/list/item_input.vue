<template>
  <div>
    <div class="form-row" v-for="item in form.fields[name]">
      <div role="group" class="form-group col-md-6">
        <input type="text" v-model="item.name" class="form-control" @input="onInput" placeholder="nazwa produktu">
      </div>
      <div role="group" class="form-group col-md-2">
        <input type="text" v-model="item.quantity" class="form-control" @input="onInput" placeholder="1.00">
      </div>
      <currency v-model="item.value" @input="onInput"></currency>
    </div>
  </div>
</template>

<script>
import currency from '@/bills/list/currency'
import base from '@/forms/base'

export default {
  extends: base,
  methods: {
    resetInput () {
      this.form.fields[this.name] = []
      for (let item of this.form.defaults[this.name]) {
        this.form.fields[this.name].push(Object.assign({}, item))
      }
      this.form.errors[this.name] = []
      this.form = Object.assign({}, this.form)
      this.state = 'normal'
      this.onInput()
    },
    appendChild () {
      this.form.fields.items.push({
        name: '',
        quantity: '',
        value: ''
      })
      this.form = Object.assign({}, this.form)
    }
  },
  components: {
    currency
  }
}
</script>
