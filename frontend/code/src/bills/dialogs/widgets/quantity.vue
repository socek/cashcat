<template>
  <div role="group" class="form-group col-md-2 is-valid">
    <input
      ref="input"
      type="number"
      step="0.00001"
      placeholder="1.00"

      v-model="value.value"
      :class="getClass()"
      @input="sendUpdate()">
    <div class="invalid-feedback" style="display: block;" v-for="message in value.errors">{{ message }}</div>
  </div>
</template>

<script>
  import base from './base'

  export default {
    extends: base,
    methods: {
      focus () {
        this.$refs.input.focus()
      }
    }
  }
</script>
