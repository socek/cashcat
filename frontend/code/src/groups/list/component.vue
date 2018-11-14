<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2"><icon name="layer-group" /> Grupy</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <new-dialog></new-dialog>
      </div>
    </div>
    <b-table ref="table" :busy.sync="isBusy" show-empty striped bordered hover :items="provider" :fields="fields">
      <template slot="actions" slot-scope="data">
        <edit-dialog :group_uid="data.item.uid"></edit-dialog>
      </template>
      <template slot="empty">
        Brak elementów do wyświetlenia.
      </template>
    </b-table>
  </div>
</template>

<script>
import groupResource from '@/groups/resource'
import newDialog from '@/groups/dialogs/new'
import editDialog from '@/groups/dialogs/edit'

export default {
  data () {
    this.$store.dispatch('groups/fetchGroups')
    return {
      isBusy: false,
      fields: [
        {key: 'name', label: 'Nazwa'},
        {key: 'actions', label: 'Akcje'} ],
      resource: groupResource(this)
    }
  },
  computed: {
    provider (ctx) {
      return this.$store.state.groups.groups
    }
  },
  components: {
    newDialog,
    editDialog
  }
}
</script>
