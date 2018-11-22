<template>
  <div>
    <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
      <h1 class="h2"><icon name="wallet" /> Portfele</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <new-dialog></new-dialog>
      </div>
    </div>
    <b-table ref="table" :busy.sync="isBusy" show-empty striped bordered hover :items="provider" :fields="fields">
    <template slot="name" slot-scope="data">
      <router-link class="nav-link active" :to="{ name: 'WalletDashboard', params: {wallet_uid: data.item.uid} }"><icon name="wallet" /> {{ data.item.name }}</router-link>
    </template>
      <template slot="actions" slot-scope="data">
        <editDialog :wallet_uid="data.item.uid"></editDialog>
        <deleteDialog :wallet_uid="data.item.uid"></deleteDialog>
      </template>
      <template slot="empty">
        Brak elementów do wyświetlenia.
      </template>
    </b-table>
  </div>
</template>

<script>
import walletResource from '@/wallets/resource'
import newDialog from '@/wallets/dialogs/new'
import editDialog from '@/wallets/dialogs/edit'
import deleteDialog from '@/wallets/dialogs/delete'

export default {
  data () {
    return {
      isBusy: false,
      fields: [ {key: 'name', label: 'Nazwa'}, {key: 'actions', label: 'Akcje'} ],
      items: [],
      resource: walletResource(this)
    }
  },
  computed: {
    provider (ctx) { return this.$store.state.wallets.wallets }
  },
  components: {
    editDialog,
    newDialog,
    deleteDialog
  }
}
</script>
