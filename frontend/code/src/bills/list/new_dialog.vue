<template>
  <div class="row justify-content-md-end">
    <b-btn @click="showModal" variant="outline-success" size="sm" v-b-tooltip.hover title="Stwórz nowy rachunek">
      <icon name="plus-circle" />
    </b-btn>

    <b-modal id="newBillDialog" ref="newBillDialog" title="Nowy Rachunek" hide-footer>
      <form @submit.prevent="onSubmit">
        <b-form-invalid-feedback  :force-show="true"
                                  v-for="error in errors._schema"
                                  :key="error">
          {{ error }}
        </b-form-invalid-feedback>

        <b-form-group id="billPlaceFieldGroup"
                      label="Miejsce:"
                      label-for="billPlaceField">
          <b-form-input id="billPlaceField"
                        type="text"
                        placeholder="sklep"
                        v-model.trim="fields.place"
                        :state="errors.place.length == 0 ? null : false">
          </b-form-input>
          <b-form-invalid-feedback v-for="error in errors.place" :key="error">
            {{ error }}
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group id="billBilledAtFieldGroup"
                      label="Dzień:"
                      label-for="billBilledAtField">
          <date-picker v-bind:class="{'is-invalid': errors.billed_at.length == 0 ? null : true}" v-model="fields.billed_at" :config="datepicker_options"></date-picker>
          <b-form-invalid-feedback v-for="error in errors.billed_at" :key="error">
            {{ error }}
          </b-form-invalid-feedback>
        </b-form-group>

        <input type="submit" value="Zapisz" class="btn btn-primary">
        <b-btn variant="danger" @click="hideModal">Anuluj</b-btn>
      </form>
    </b-modal>
  </div>
</template>

<script>
import billResource from '@/bills/resource'

export default {
  data () {
    return {
      fields: {
        place: '',
        billed_at: ''
      },
      errors: {
        _schema: [],
        place: [],
        billed_at: []
      },
      resource: billResource(this),
      datepicker_options: {
        format: 'YYYY-MM-DD',
        useCurrent: true
      }
    }
  },
  methods: {
    refresh () {
      for (let name in this.fields) {
        this.fields[name] = ''
        this.errors[name] = ''
      }
      this.errors._schema = ''
    },
    showModal () {
      this.refresh()
      this.$refs.newBillDialog.show()
    },
    hideModal () {
      this.$refs.newBillDialog.hide()
    },
    onSubmit () {
      this.resource.create({}, this.fields).then((response) => {
        this.hideModal()
        this.$root.$emit('bv::refresh::table', 'bill-list-table')
      }).catch((response) => {
        for (let item in this.errors) {
          this.errors[item] = []
        }
        for (let item in response.body) {
          console.log(item, response.body[item])
          this.errors[item] = response.body[item]
        }
        console.log(this.errors)
      })
    }
  }
}
</script>
