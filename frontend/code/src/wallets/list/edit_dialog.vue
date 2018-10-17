<template>
  <dialogform
    title="Edytuj portfel"
    variant="outline-primary"
    :form="form"
    :fetchContent="fetchContent"
    @onSave="onSave"
    @onRefresh="refreshForm"
    ref="dialog">

      <template slot="anhor">
        <icon name="edit"></icon>
      </template>

      <template slot="content">
        <b-form-group id="nameFieldGroup"
                            label="Nazwa:"
                            label-for="nameField">
          <b-form-input id="nameField"
                        v-model.trim="form.fields.name"
                        type="text"
                        :state="form.errors.name.length == 0 ? null : false"
                        placeholder="Nazwa"></b-form-input>
          <b-form-invalid-feedback  v-for="error in form.errors.name"
                                    class="modal-invalid-feedback"
                                    :key="error">
            {{ error }}
          </b-form-invalid-feedback>
        </b-form-group>
      </template>

  </dialogform>


</template>

<script>
import walletResource from '@/wallets/resource'
import baseForm from '@/forms'
import dialogform from '@/common/dialogForm'

export default {
  props: ['wallet_uid'],
  extends: baseForm,
  data () {
    return {
      isBusy: true,
      form: this.prepareForm({
        name: ''
      }),
      resource: walletResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({wallet_uid: this.wallet_uid})
    },
    saveCall () {
      return this.resource.update({wallet_uid: this.wallet_uid}, this.form.fields)
    }
  },
  components: {
    dialogform
  }
}
</script>
