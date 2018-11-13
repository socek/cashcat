<template>
  <div role="group" class="form-group">
    <label v-if="label" class="col-form-label">{{ label }}:</label>
    <input type="password" v-model="value.value" class="form-control" :class="inputClass()">
    <div class="invalid-feedback" style="display: block;" v-for="message in value.errors">{{ message }}</div>
  </div>
</template>

<script>
  import base from '@/forms/base'
  export default {extends: base}
</script>
