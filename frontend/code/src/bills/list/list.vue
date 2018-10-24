<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2"><icon name="wallet" /> Portfele</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
          <new-dialog></new-dialog>
      </div>
    </div>
    <b-table ref="table" id="wallet-list-table" :busy.sync="isBusy" show-empty striped bordered hover :items="provider" :fields="fields">
      <template slot="empty">
        Brak elementów do wyświetlenia.
      </template>
    </b-table>
  </div>
</template>

<script>
import billResource from '@/bills/resource'
import newDialog from '@/bills/list/new_dialog'

export default {
  data () {
    return {
      isBusy: false,
      fields: [ {key: 'place', label: 'Miejsce'}, {key: 'billed_at', label: 'Dzień'} ],
      items: [],
      resource: billResource(this)
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
    newDialog
  }
}
</script>
