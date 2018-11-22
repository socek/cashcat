<template>
  <div role="group" class="form-group col-md-3">
    <input
      type="text"
      placeholder="Nazwa produktu"

      v-model="value.value"
      :class="getClass()"
      @input="sendUpdate()">
    <div class="invalid-feedback" style="display: block;" v-for="message in value.errors">{{ message }}</div>
  </div>
</template>

<script>
  import base from './base'

  export default {extends: base}
</script>
