<template>
  <div role="group" class="b-form-group form-group">
    <label :for="id" class="col-form-label pt-0">{{ label }}:</label>
    <input :id="id" type="password" v-model="form.fields[name]" v-bind="options" class="form-control" @input="onInput" :class="{'is-invalid': state == 'error'}">
    <div class="invalid-feedback" style="display: block;" v-for="message in form.errors[name]">{{ message }}</div>
  </div>
</template>

<script>
  import base from '@/forms/base'
  export default {extends: base}
</script>
