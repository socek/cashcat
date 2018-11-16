<template>
  <form @submit.prevent="onSubmit">
    <div class="invalid-feedback" style="display: block;" v-for="message in value._schema">{{ message }}</div>
    <slot></slot>

    <input type="submit" :value="okButtonLabel" class="btn btn-primary">
    <b-btn v-if="showCancel" variant="danger" @click="onCancel">Anuluj</b-btn>
  </form>
</template>

<script>
  import {resetForm, toFields, toFormObject, parseErrorResponse, setDefaults} from './tools'

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
      this.$emit('input', toFormObject(this.value))
      return {}
    },
    methods: {
      resetForm () {
        let form = resetForm(this.value)
        this.$emit('input', form)
        this.$emit('afterReset')
      },
      onSubmit () {
        let fields = toFields(this.value)
        this.$emit('submit', fields)
      },
      onCancel (event) {
        this.$emit('cancel', this.value)
      },

      parseErrorResponse (response) {
        let form = parseErrorResponse(this.value, response)
        if (form) {
          this.$emit('input', form)
        } else {
          console.log('something bad has happened', response)
        }
      },
      setDefaults (defaults) {
        let form = setDefaults(this.value, defaults)
        this.$emit('input', form)
      }
    }
  }
</script>
