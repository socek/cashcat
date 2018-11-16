<template>
  <div>

   <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
     <a class="navbar-brand col-sm-3 col-md-1 mr-0" href="#/">Cashcat</a>
     <ul class="navbar-nav px-3">
       <login v-if="isAuthenticated"></login>
       <register v-if="!isAuthenticated"></register>
     </ul>
   </nav>

    <div class="container-fluid">
      <nav class="col-md-1 d-none d-md-block bg-light sidebar" v-if="isAuthenticated">
        <div class="sidebar-sticky">
          <ul class="nav flex-column">
            <walletsList></walletsList>
          </ul>
        </div>
      </nav>

      <main role="main" class="col-md-10 ml-sm-auto" :class="{'col-lg-11': isAuthenticated, 'col-lg-12': !isAuthenticated}">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script>
  import login from '@/auth/login'
  import register from '@/auth/register'
  import walletsList from '@/wallets/list/sidebar'

  export default {
    computed: {
      isAuthenticated () {
        return this.$store.getters['auth/isAuthenticated']
      }
    },
    created () {
      this.$store.commit('init', this)
    },
    name: 'app',
    components: {
      login,
      register,
      walletsList
    }
  }
</script>
