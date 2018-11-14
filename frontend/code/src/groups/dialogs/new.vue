<template>
  <dialogform
    title="Nowa grupa"

    ref="form"
    v-model="form"
    @success="$emit('success')"
    @submit="onSubmit">

    <template slot="anhor">
      <icon name="plus-circle" />
    </template>

    <template slot="content">
      <text-input v-model="form.name" label="Nazwa" placeholder="Grupa produktów"></text-input>
    </template>
  </dialogform>
</template>

<script>
import groupResource from '@/groups/resource'

export default {
  data () {
    return {
      form: {
        name: ''
      }
    }
  },
  methods: {
    onSubmit (form) {
      return groupResource(this).create({}, form).then((response) => {
        this.$store.dispatch('groups/fetchGroups')
        this.$refs.form.onSuccess()
      }).catch(this.$refs.form.parseErrorResponse)
    }
  }
}
</script>
