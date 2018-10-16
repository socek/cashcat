<template>
  <div class="row justify-content-md-end">
    <b-btn @click="showModal" variant="outline-primary" size="sm">
      Nowy Portfel
    </b-btn>

    <b-modal id="newWalletDialog" ref="newWalletDialog" title="Nowy Portfel" hide-footer>
      <form @submit.prevent="onSubmit">
        <b-form-invalid-feedback  :force-show="true"
                                  v-for="error in errors._schema"
                                  :key="error">
          {{ error }}
        </b-form-invalid-feedback>

        <b-form-group id="walletNameFieldGroup"
                      label="Nazwa:"
                      label-for="walletNameField">
          <b-form-input id="walletNameField"
                        type="text"
                        placeholder="nazwa"
                        v-model.trim="fields.name"
                        :state="errors.name.length == 0 ? null : false">
          </b-form-input>
          <b-form-invalid-feedback v-for="error in errors.name" :key="error">
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
import walletResource from '@/wallets/resource'

export default {
  data () {
    return {
      fields: {
        name: ''
      },
      errors: {
        _schema: [],
        name: []
      },
      resource: walletResource(this)
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
      this.$refs.newWalletDialog.show()
    },
    hideModal () {
      this.$refs.newWalletDialog.hide()
    },
    onSubmit () {
      this.resource.create({}, this.fields).then((response) => {
        this.hideModal()
        this.$root.$emit('bv::refresh::table', 'wallet-list-table')
      })
    }
  }
}
</script>
