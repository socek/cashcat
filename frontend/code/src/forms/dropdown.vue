<template>
  <v-select
    class="form-control"
    :class="inputClass()"
    label="text"
    v-model="selected"
    :options="options"
    @input="onInputSelect"></v-select>
</template>

<script>
  import base from '@/forms/base'

  export default {
    extends: base,
    props: {
      options: {
        required: true
      }
    },
    data () {
      return {
        selected: this.getOptionByValue(this.value.value)
      }
    },
    updated () {
      this.selected = this.getOptionByValue(this.value.value)
    },
    methods: {
      getOptionByValue (value) {
        for (let option of this.options) {
          if (option.value === value) {
            return option
          }
        }
      },
      onInputSelect (element) {
        let value = this.value
        value.value = element ? element.value : null
        this.$emit('input', value)
      }
    }
  }
</script>
