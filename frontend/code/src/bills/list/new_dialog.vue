<template>
  <div class="row justify-content-md-end">
    <b-btn @click="showModal" variant="outline-success" size="sm" v-b-tooltip.hover title="Stwórz nowy rachunek">
      <icon name="plus-circle" />
    </b-btn>

    <b-modal id="newBillDialog" ref="newBillDialog" title="Nowy Rachunek" hide-footer>
      <cc-form ref="form" @submit="onSubmit" @cancel="hideModal">
        <text-input name="place" label="Miejsce:" placeholder="nazwa sklepu"></text-input>
        <text-input name="billed_at" label="Kiedy:" placeholder="dzień zakupu"></text-input>
      </cc-form>
    </b-modal>
  </div>
</template>

<script>
import billResource from '@/bills/resource'
import itemInput from '@/bills/list/item_input'
import textInput from '@/forms/text'
import ccForm from '@/forms/form'

export default {
  data () {
    return {
      resource: billResource(this),
      datepicker_options: {
        format: 'YYYY-MM-DD',
        useCurrent: true
      },
      sum: 0
    }
  },
  methods: {
    refresh () {
      for (let input of this.form.inputs) {
        if (input) {
          input.resetInput()
        }
      }
    },
    showModal () {
      this.$refs.form.reset()
      this.$refs.newBillDialog.show()
    },
    hideModal () {
      this.$refs.newBillDialog.hide()
    },
    onSubmit (event, form) {
      this.resource.create({}, this.fields).then((response) => {
        this.hideModal()
        this.$root.$emit('bv::refresh::table', 'bill-list-table')
      }).catch((response) => {
        for (let item in this.errors) {
          form.errors[item] = []
        }
        for (let item in response.body) {
          form.errors[item] = response.body[item]
        }
        this.$refs.form.updateForm(form)
      })
    },
    createEmptyItem () {
      this.fields.items.push({
        index: this.fields.items.length,
        name: '',
        quantity: 1.0,
        value: -1.0
      })
      this.fields = Object.assign({}, this.fields) // refresh the whole object for vue
    },
    countSum () {
      this.sum = 0
      for (let index in this.fields.items) {
        let item = this.fields.items[index]
        if (item.name) {
          this.sum += item.quantity * item.value
        }
      }
    },
    onChange () {
      let items = this.fields.items
      let value = items[items.length - 1].name
      if (value) {
        this.createEmptyItem()
      }
      this.countSum()
    }
  },
  components: {
    itemInput,
    textInput,
    ccForm
  }
}
</script>
