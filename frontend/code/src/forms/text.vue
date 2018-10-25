<template>
  <div role="group" class="b-form-group form-group">
    <label :for="id" class="col-form-label pt-0">{{ label }}:</label>
    <div>
      <input :id="id" type="text" v-model="form.fields[name]" v-bind="options" class="form-control" @input="onInput">
    </div>
  </div>
</template>

<script>
  import base from '@/forms/base'
  export default {extends: base}
</script>
