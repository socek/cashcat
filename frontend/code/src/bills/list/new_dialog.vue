<template>
  <dialogform
    title="Nowy rachunek"
    size="lg"

    ref="form"
    v-model="form"
    @success="$emit('success')"
    @submit="onSubmit">

    <template slot="anhor">
      <icon name="plus-circle" />
    </template>
    <template slot="content">
      <text-input v-model="form.place" label="Miejsce" placeholder="nazwa sklepu"></text-input>
      <date-input v-model="form.billed_at" label="Kiedy"></date-input>
      <item-row
        v-for="(item, index) in form.items"
        v-model="form.items[index]"
        :index="item._index"
        :key="item._index"
        @input="onInput"
        @removeItem="removeItem"></item-row>

      <div class="form-row">
        <div role="group" class="form-group col-md-8">
          &nbsp;
        </div>
        <div role="group" class="form-group col">
          Suma:
        </div>
        <div role="group" class="form-group col">
          {{sum}} PLN
        </div>
      </div>
    </template>
  </dialogform>

</template>

<script>
import billResource from '@/bills/resource'
import itemRow from '@/bills/list/item_input'

export default {
  data () {
    return {
      form: {
        place: '',
        billed_at: '', // paste here current date
        items: [{
          _index: 0,
          name: '',
          quantity: '',
          value: ''
        }]
      },
      resource: billResource(this),
      sum: 0
    }
  },
  methods: {
    onSubmit (form) {
      this.resource.create({}, form).then((response) => {
        this.$refs.form.onSuccess()
      }).catch(this.$refs.form.parseErrorResponse)
    },
    countSum () {
      this.sum = 0
      for (let item of this.form.items) {
        let price = item.value.value
        let quantity = item.quantity.value
        if (price && quantity) {
          this.sum += quantity * price
        }
      }
      this.sum = this.formatCurrency(this.sum)
    },
    formatCurrency (value) {
      return Number(value).toFixed(2)
    },
    createEmptyItem () {
      let len = this.form.items.length
      let field = this.$refs.form.$refs.form.toFormObject({
        _index: len,
        _isLast: true,
        name: '',
        quantity: '',
        value: ''
      })
      this.form.items[len - 1]._isLast = false
      this.form.items.push(field)
    },
    onInput () {
      let items = this.form.items
      let value = items[items.length - 1].name.value
      if (value) {
        this.createEmptyItem()
      }
      this.countSum()
    },
    removeItem (index) {
      this.form.items.splice(index, 1)
      for (let loop = index; loop < this.form.items.length; loop++) {
        this.form.items[loop]._index = loop
      }
      this.countSum()
    }
  },
  components: {
    itemRow
  }
}
</script>
