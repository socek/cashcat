<template>
  <form @submit.prevent="onSubmit">
    <div class="invalid-feedback" style="display: block;" v-for="message in value._schema">{{ message }}</div>
    <slot></slot>

    <input type="submit" :value="okButtonLabel" class="btn btn-primary">
    <b-btn v-if="showCancel" variant="danger" @click="onCancel">Anuluj</b-btn>
  </form>
</template>

<script>
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
      this.$emit('input', this.toFormObject(this.value))
      return {}
    },
    methods: {
      toFormField (value) {
        return {
          value: value,
          errors: [],
          default: value
        }
      },
      toFormObject (obj) {
        obj._schema = []
        for (let index in obj) {
          let value = obj[index]
          if (index === '_schema') {
            // do nothing. _schema is a special field
          } else if (typeof (value) === 'object') {
            obj[index] = this.toFormObject(value)
          } else {
            obj[index] = this.toFormField(value)
          }
        }
        return obj
      },
      resetFields (field) {
        for (let index in field) {
          let value = field[index]
          if (value.default !== undefined) {
            field[index].value = value.default
          } else {
            field[index] = this.resetFields(value)
          }
        }
        return field
      },
      resetForm () {
        this.$emit('input', this.resetFields(this.value))
      },
      toFields (form) {
        let fields = {}
        for (let index in form) {
          let value = form[index]
          if (index === '_schema') {
            // do nothing
          } else if (value.value !== undefined) {
            fields[index] = value.value
          } else {
            fields[index] = this.toFields(value)
          }
        }
        return fields
      },
      onSubmit () {
        let fields = this.toFields(this.value)
        this.$emit('submit', fields)
      },
      onCancel (event) {
        this.$emit('cancel', this.value)
      },

      resetErrors (field) {
        for (let index in field) {
          let value = field[index]
          if (index === 'errors') {
            field[index] = []
          } else if (value.default !== undefined) {
            field[index].errors = []
          } else {
            field[index] = this.resetErrors(value)
          }
        }
        return field
      },

      setErrors (form, errors) {
        for (let index in errors) {
          if (index === '_schema') {
            form._schema = errors[index]
          } else if (typeof (errors[index][0]) === 'string') {
            form[index].errors = errors[index]
          } else {
            form[index] = this.setErrors(form[index], errors[index])
          }
        }
        return form
      },
      parseErrorResponse (response) {
        let form = this.value
        form = this.resetErrors(form)
        form = this.setErrors(form, response.body)
        this.$emit('input', form)
      }
    }
  }
</script>
