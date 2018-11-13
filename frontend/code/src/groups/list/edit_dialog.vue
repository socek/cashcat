<template>
  <dialogform
    title="Edytuj grupę"

    :fetchContent="fetchContent"
    ref="form"
    v-model="form"
    @success="$emit('success')"
    @submit="onSubmit">

      <template slot="anhor">
        <icon name="edit"></icon>
      </template>

      <template slot="content">
        <text-input v-model="form.name" placeholder="Grupa produktów" label="Nazwa"></text-input>
      </template>
  </dialogform>


</template>

<script>
import groupResource from '@/groups/resource'

export default {
  props: ['group_uid'],

  data () {
    return {
      form: {
        name: ''
      },
      resource: groupResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({group_uid: this.group_uid})
    },
    onSubmit (form) {
      groupResource(this).update({group_uid: this.group_uid}, form).then((response) => {
        this.$refs.form.onSuccess()
      }).catch(this.$refs.form.parseErrorResponse)
    }
  }
}
</script>
