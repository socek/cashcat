<template>
  <div role="group" class="b-form-group form-group">
    <label :for="id" class="col-form-label pt-0">{{ label }}:</label>
    <date-picker :id="id" v-model="form.fields[name]" class="form-control" @input="onInput" :class="{'is-invalid': state == 'error'}" :config="options"></date-picker>
    <div class="invalid-feedback" style="display: block;" v-for="message in form.errors[name]">{{ message }}</div>
  </div>
</template>

<script>
  import base from '@/forms/base'
  export default {
    mixins: [base],
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
