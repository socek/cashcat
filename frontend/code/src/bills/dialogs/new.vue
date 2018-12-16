<template>
  <dialogform
    title="Nowy rachunek"
    size="lg"

    ref="dialog"
    v-model="form"
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
import itemRow from '@/bills/dialogs/widgets/item_row'
import form from '@/forms'

export default {
  data () {
    return {
      form: form({
        place: '',
        billed_at: '', // paste here current date
        items: [{
          _index: 0,
          name: '',
          quantity: '',
          value: '',
          group_uid: ''
        }]
      }),
      resource: billResource(this),
      sum: 0
    }
  },
  methods: {
    onSubmit (form) {
      form.submit(
        () => this.resource.create({}, form.toData()),
        (response) => {
          this.$refs.dialog.hide()
          this.$emit('success')
        }
      )
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
    ensureEmptyItemAtEnd () {
      let items = this.form.items
      let len = items.length
      if (items.length === 0 || items[len - 1].name.value) {
        let field = form({
          _index: len,
          _isLast: true,
          name: '',
          quantity: '',
          value: '',
          group_uid: ''
        })
        if (len > 0) {
          this.form.items[len - 1]._isLast = false
        }
        this.form.items.push(field)
      }
    },
    onInput () {
      this.ensureEmptyItemAtEnd()
      this.countSum()
    },
    removeItem (item) {
      let index = item._index
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
