<template>
  <div>
    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted nooutline">
      <router-link class="nav-link" :to="{ name: 'WalletList'}" :class="{active: isWalletListActive()}">
        Portfele
      </router-link>
      <new-dialog></new-dialog>
    </h6>

    <li class="nav-item" v-for="wallet in wallets" :key="wallet.uid">
      <router-link class="nav-link" :class="{active: isWalletActive(wallet)}" :to="{ name: 'WalletDashboard', params: {wallet_uid: wallet.uid} }">
        <icon name="wallet" /> {{ wallet.name }} <span v-if="isWalletActive(wallet)" class="sr-only">(current)</span>
      </router-link>
    </li>
  </div>
</template>

<script>
  import newDialog from '@/wallets/dialogs/new'

  export default {
    methods: {
      isWalletActive (wallet) {
        return this.$route.name === 'WalletDashboard' && this.$route.params.wallet_uid === wallet.uid
      },
      isWalletListActive () {
        return this.$route.name === 'WalletList'
      }
    },
    computed: {
      wallets () {
        return this.$store.state.wallets.wallets
      }
    },
    created () {
      this.$store.dispatch('wallets/fetchWallets')
    },
    components: {
      newDialog
    }
  }
</script>
