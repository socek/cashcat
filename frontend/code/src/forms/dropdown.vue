<template>
  <select class="form-control" v-model="value.value">
    <option v-for="option in options" v-bind:value="option.value">
      {{ option.text }}
    </option>
  </select>
</template>

<script>
  import base from '@/forms/base'

  export default {
    extends: base,
    props: {
      options: {
        required: true
      }
    }
  }
</script>
