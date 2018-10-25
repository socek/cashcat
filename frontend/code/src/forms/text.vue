<template>
  <div role="group" class="b-form-group form-group">
    <label :for="id" class="col-form-label pt-0">{{ label }}:</label>
    <div>
      <input :id="id" type="text" v-model="form.fields[name]" v-bind="options" class="form-control" @input="onInput">
    </div>
  </div>
</template>

<script>
  export default {
    props: ['name', 'default', 'placeholder', 'label'],
    data () {
      let form = {
        fields: {},
        errors: {}
      }
      form.fields[this.name] = ''
      form.errors[this.name] = []
      let options = {}
      if (this.placeholder) {
        options.placeholder = this.placeholder
      }
      return {
        form: form,
        options: options,
        id: ''
      }
    },
    methods: {
      setForm (form) {
        form.fields[this.name] = ''
        form.errors[this.name] = []
        form.defaults[this.name] = this.default ? this.default : ''
        form.inputs.push(this)
        this.id = form.id + '_' + this.name
        this.form = form
      },
      updateForm (form) {
        this.form = form
      },
      onInput () {
        this.$emit('input', this.form)
      },
      resetInput () {
        this.form.fields[this.name] = this.default ? this.default : ''
        this.form.errors[this.name] = []
        this.form = Object.assign({}, this.form)
        this.onInput()
      }
    }
  }
</script>
