<template>
  <div>
    <b-navbar v-if="isAuthenticated" toggleable="md" type="dark" variant="dark">
      <b-navbar-brand href="#">Cashcat Admin Panel</b-navbar-brand>
      <b-collapse is-nav id="nav_collapse">

        <b-navbar-nav>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <login></login>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <div class="container" id="content_container">
      <register v-if="!isAuthenticated"></register>
      <router-view></router-view>
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
