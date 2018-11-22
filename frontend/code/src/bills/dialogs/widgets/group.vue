<template>
  <div role="group" class="form-group col-md-3">
    <dropdown v-model="value" :options="groups" @input="sendUpdate()"></dropdown>
    <div class="invalid-feedback" style="display: block;" v-for="message in value.errors">{{ message }}</div>
  </div>
</template>

<script>
  import base from './base'

  export default {
    extends: base,
    computed: {
      groups () {
        let data = []
        for (let group of this.$store.state.groups.groups) {
          data.push({value: group.uid, text: group.name})
        }
        return data
      }
    }
  }
</script>
