<template>
  <dialogform
    title="Nowy rachunek"
    size="lg"
    :saveCall="saveCall"
    @success="$emit('success')">

    <template slot="anhor">
      <icon name="plus-circle" />
    </template>
    <template slot="content">
      <text-input name="place" label="Miejsce" placeholder="nazwa sklepu"></text-input>
      <date-input name="billed_at" label="Kiedy"></date-input>
      <item-row ref="items" name="items" :default="items"  @input="onInput"></item-row>
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
      items: [{name: '', quantity: '', value: ''}],
      resource: billResource(this),
      sum: 0
    }
  },
  methods: {
    saveCall (form) {
      let fields = Object.assign({}, form.fields)
      fields.items = []
      for (let item of form.fields.items) {
        if (item.name || item.quantity || item.value) {
          fields.items.push(item)
        }
      }
      return this.resource.create({}, fields)
    },
    countSum (form) {
      this.sum = 0
      for (let item of form.fields.items) {
        if (item.name) {
          this.sum += item.quantity * item.value
        }
      }
      this.sum = this.formatCurrency(this.sum)
    },
    formatCurrency (value) {
      let num = Number(value)

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
      return num
    },
    onInput (form) {
      let items = form.fields.items
      let value = items[items.length - 1].name
      if (value) {
        this.$refs.items.appendChild()
      }
      this.countSum(form)
    }
  },
  components: {
    itemRow
  }
}
</script>
