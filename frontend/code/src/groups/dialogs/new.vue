<template>
  <dialogform title="Nowa grupa" ref="dialog" v-model="form" @submit="onSubmit">

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
import form from '@/forms'

export default {
  data () {
    return {
      form: form({
        name: ''
      })
    }
  },
  methods: {
    onSubmit (form) {
      form.submit(
        () => groupResource(this).create({}, form.toData()),
        (response) => {
          this.$store.dispatch('groups/fetchGroups')
          this.$refs.dialog.hide()
        }
      )
    }
  }
}
</script>
