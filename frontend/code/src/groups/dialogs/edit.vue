<template>
  <dialogform title="Edytuj grupę" :fetchContent="fetchContent" ref="dialog" v-model="form" @submit="onSubmit">

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
import form from '@/forms'

export default {
  props: ['group_uid'],

  data () {
    return {
      form: form({
        name: ''
      }),
      resource: groupResource(this)
    }
  },
  methods: {
    fetchContent () {
      return this.resource.get({group_uid: this.group_uid})
    },
    onSubmit (form) {
      form.submit(
        () => groupResource(this).update({group_uid: this.group_uid}, form.toData()),
        (response) => {
          this.$store.dispatch('groups/fetchGroups')
          this.$refs.dialog.hide()
        }
      )
    }
  }
}
</script>
