<template>
  <div>
    <b-navbar v-if="!isAuthenticated" toggleable="md" type="light" variant="light">
      <b-navbar-brand href="#">Cashcat</b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <register v-if="!isAuthenticated"></register>
      </b-navbar-nav>
    </b-navbar>

   <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow" v-if="isAuthenticated">
     <a class="navbar-brand col-sm-3 col-md-1 mr-0" href="#/">Cashcat</a>
     <ul class="navbar-nav px-3">
       <login></login>
     </ul>
   </nav>

    <div class="container-fluid">
      <router-view v-if="!isAuthenticated"></router-view>
      <nav class="col-md-1 d-none d-md-block bg-light sidebar" v-if="isAuthenticated">
        <div class="sidebar-sticky">
          <ul class="nav flex-column">
            <walletsList></walletsList>
          </ul>
        </div>
      </nav>

      <main id="main" role="main" class="col-md-10 ml-sm-auto col-lg-11">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script>
  import login from '@/auth/login'
  import register from '@/auth/register'
  import walletsList from '@/wallets/navbar_list'

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
