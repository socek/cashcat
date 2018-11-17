<template>
  <form @submit.prevent="onSubmit">
    <div class="invalid-feedback" style="display: block;" v-for="message in value._schema">{{ message }}</div>
    <slot></slot>

    <input type="submit" :value="okButtonLabel" class="btn btn-primary">
    <b-btn v-if="showCancel" variant="danger" @click="onCancel">Anuluj</b-btn>
  </form>
</template>

<script>
  import {formActions, convertToData, convertToForm} from './tools'

  export default {
    props: {
      id: {
        type: String,
        default: ''
      },
      showCancel: {
        type: Boolean,
        default: true
      },
      okButtonLabel: {
        type: String,
        default: 'Zapisz'
      },
      value: {
        type: Object,
        required: true
      }
    },
    data () {
      this.$emit('input', convertToForm(this.value))
      return {}
    },
    methods: {
      resetForm () {
        let form = formActions.reset(this.value)
        this.$emit('input', form)
        this.$emit('afterReset')
      },
      onSubmit () {
        let fields = convertToData(this.value)
        this.$emit('submit', fields)
      },
      onCancel (event) {
        this.$emit('cancel', this.value)
      },

      parseErrorResponse (response) {
        if (response.status === 400) {
          let form = formActions.resetErrors(this.value)
          form = formActions.setErrors(form, response.body)
          this.$emit('input', form)
        } else {
          console.log('something bad has happened', response)
        }
      },
      setDefaults (defaults) {
        let form = formActions.setDefaults(this.value, defaults)
        this.$emit('input', form)
      }
    }
  }
</script>
