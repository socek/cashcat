<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2"><icon name="money-bill-wave" /> Rachunki</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
          <new-dialog @success="fetchData"></new-dialog>
      </div>
    </div>
    <b-table ref="table" :busy.sync="isBusy" show-empty striped bordered hover :items="provider" :fields="fields">
      <template slot="actions" slot-scope="data">
        <edit-dialog :bill_uid="data.item.uid" @success="fetchData"></edit-dialog>
      </template>
      <template slot="empty">
        Brak elementów do wyświetlenia.
      </template>
    </b-table>
  </div>
</template>

<script>
import billResource from '@/bills/resource'
import newDialog from '@/bills/dialogs/new'
import editDialog from '@/bills/dialogs/edit'

export default {
  data () {
    return {
      isBusy: false,
      fields: [
        {key: 'place', label: 'Miejsce'},
        {key: 'billed_at', label: 'Dzień'},
        {key: 'total', label: 'Suma'},
        {key: 'actions', label: 'Akcje'} ],
      items: [],
      resource: billResource(this)
    }
  },
  methods: {
    provider (ctx) {
      return this.resource.list({wallet_uid: this.$route.params.wallet_uid}, this.fields).then((response) => {
        return response.data
      })
    },
    fetchData () {
      this.$refs.table.refresh()
    }
  },
  components: {
    newDialog,
    editDialog
  }
}
</script>
