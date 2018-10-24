<template>
  <div>
    <b-navbar v-if="!isAuthenticated" toggleable="md" type="light" variant="light">
      <b-navbar-brand href="#">Cashcat - Portfelowy Kot</b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <register v-if="!isAuthenticated"></register>
      </b-navbar-nav>
    </b-navbar>

    <b-navbar v-if="isAuthenticated" toggleable="md" type="dark" variant="dark">
      <b-navbar-brand href="#">Cashcat - Portfelowy Kot</b-navbar-brand>
      <b-collapse is-nav id="nav_collapse">

        <b-navbar-nav>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <login></login>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <div class="container-fluid" id="content_container">
      <router-view v-if="!isAuthenticated"></router-view>
      <div class="row" v-if="isAuthenticated">
        <nav class="col-md-1 d-none d-md-block bg-light sidebar">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
              <li class="nav-item">
                <router-link class="nav-link active" :to="{ name: 'WalletList' }">
                  <icon name="wallet" /> Portfele
                </router-link>
              </li>
            </ul>
          </div>
        </nav>
        <main role="main" class="col-md-10 ml-sm-auto col-lg-11 pt-3 px-4">
          <router-view></router-view>
        </main>
      </div>
    </div>

  </div>
</template>

<script>
  import login from '@/auth/login'
  import register from '@/auth/register'

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
      register
    }
  }
</script>
