<template>
  <form @submit.prevent="$emit('submit', value)">
    <div class="invalid-feedback" style="display: block;" v-for="message in value._schema">{{ message }}</div>
    <slot></slot>

    <input type="submit" :value="okButtonLabel" class="btn btn-primary">
    <b-btn v-if="showCancel" variant="danger" @click="$emit('cancel', value)">Anuluj</b-btn>
  </form>
</template>

<script>
  export default {
    props: {
      id: {
        type: String,
        default: ''
      },
      showCancel: {
        type: Boolean,
        default: true
      },
      okButtonLabel: {
        type: String,
        default: 'Zapisz'
      },
      value: {
        type: Object,
        required: true
      }
    }
  }
</script>
