<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2"><icon name="layer-group" /> Grupy</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <new-dialog @success="onSuccess"></new-dialog>
      </div>
    </div>
    <b-table ref="table" :busy.sync="isBusy" show-empty striped bordered hover :items="provider" :fields="fields">
      <template slot="actions" slot-scope="data">
        <edit-dialog :group_uid="data.item.uid" @success="onSuccess"></edit-dialog>
      </template>
      <template slot="empty">
        Brak elementów do wyświetlenia.
      </template>
    </b-table>
  </div>
</template>

<script>
import groupResource from '@/groups/resource'
import newDialog from '@/groups/list/new_dialog'
import editDialog from '@/groups/list/edit_dialog'

export default {
  data () {
    return {
      isBusy: false,
      fields: [
        {key: 'name', label: 'Nazwa'},
        {key: 'actions', label: 'Akcje'} ],
      resource: groupResource(this)
    }
  },
  methods: {
    provider (ctx) {
      return this.resource.list({}, this.fields).then((response) => {
        return response.data
      })
    },
    onSuccess () {
      this.$refs.table.refresh()
    }
  },
  components: {
    newDialog,
    editDialog
  }
}
</script>
