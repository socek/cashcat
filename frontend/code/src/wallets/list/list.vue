<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2"><icon name="wallet" /> Portfele</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <new-dialog></new-dialog>
      </div>
    </div>
    <b-table id="wallet-list-table" :busy.sync="isBusy" show-empty striped bordered hover :items="myProvider" :fields="fields">
      <template slot="empty">
        Brak elementów do wyświetlenia.
      </template>
    </b-table>
  </div>
</template>

<script>
import walletResource from '@/wallets/resource'
import newDialog from '@/wallets/list/new_dialog'

export default {
  data () {
    return {
      isBusy: false,
      fields: [ {key: 'name', label: 'Nazwa'} ],
      items: [],
      resource: walletResource(this)
    }
  },
  methods: {
    myProvider (ctx) {
      return this.resource.list({}, this.fields).then((response) => {
        return response.data
      })
    }
  },
  components: {
    newDialog
  }
}
</script>
