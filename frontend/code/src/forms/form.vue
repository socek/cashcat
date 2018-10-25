<template>
  <form @submit.prevent="onSubmit">
    <slot></slot>

    <input type="submit" value="Zapisz" class="btn btn-primary">
    <b-btn variant="danger" @click="onCancel">Anuluj</b-btn>
  </form>
</template>

<script>
  export default {
    props: ['id'],
    data () {
      return {
        form: {
          fields: {},
          defaults: {},
          inputs: [],
          errors: {
            _schema: []
          },
          id: this.id ? this.id : ''
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
