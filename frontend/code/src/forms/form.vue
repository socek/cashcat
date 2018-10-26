<template>
  <form @submit.prevent="onSubmit">
    <div class="invalid-feedback" style="display: block;" v-for="message in form.errors._schema">{{ message }}</div>
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
      }
    },
    data () {
      return {
        form: {
          fields: {},
          defaults: {},
          inputs: [],
          errors: {
            _schema: []
          }
        }
      }
    },
    mounted () {
      for (let child of this.$children) {
        if (child.$on) {
          child.$on('input', this.onInput)
        }
        if (child.setForm) {
          child.setForm(this.form)
        }
      }
    },
    methods: {
      onSubmit (event, data) {
        this.$emit('submit', event, this.form)
      },
      onCancel (event, data) {
        this.$emit('cancel', event, this.form)
      },
      onInput () {
        this.$emit('input', this.form)
      },
      catchError (response) {
        for (let item in this.form.errors) {
          this.form.errors[item] = []
        }
        for (let item in response.body) {
          this.form.errors[item] = response.body[item]
        }
        for (let input of this.form.inputs) {
          input.updateForm(this.form)
        }
      },
      updateForm (form) {
        this.form = form
        for (let input of this.form.inputs) {
          input.updateForm(form)
        }
      },
      reset () {
        for (let input of this.form.inputs) {
          input.resetInput()
        }
      }
    }
  }
</script>
