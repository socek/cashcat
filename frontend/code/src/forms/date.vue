<template>
  <div role="group" class="b-form-group form-group">
    <label class="col-form-label pt-0">{{ label }}:</label>
    <date-picker v-model="value.value" class="form-control" :class="{'is-invalid': state == 'error'}" :config="options"></date-picker>
    <div class="invalid-feedback" style="display: block;" v-for="message in value.errors">{{ message }}</div>
  </div>
</template>

<script>
  import base from '@/forms/base'
  export default {
    extends: base,
    data () {
      return {
        options: {
          format: 'YYYY-MM-DD',
          showTodayButton: true,
          useCurrent: true
        }
      }
    }
  }
</script>
