<template>
  <div>
    <b-navbar toggleable="md" type="dark">
      <b-navbar-brand href="#">CROJECT Admin Panel</b-navbar-brand>
      <b-collapse is-nav id="nav_collapse">

        <b-navbar-nav>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <login></login>
          <register v-if="!isAuthenticated"></register>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <breadcrumb v-if="isNavbar"></breadcrumb>

    <div class="container" id="content_container">
      <router-view></router-view>
    </div>

  </div>
</template>

<script>
  import login from '@/auth/login'
  import register from '@/auth/register'
  import breadcrumb from '@/breadcrumb/component'

  export default {
    computed: {
      isAuthenticated () {
        return this.$store.getters['auth/isAuthenticated']
    },
    created () {
      this.$store.commit('init', this)
    },
    name: 'app',
    components: {
      login,
      register,
      breadcrumb
    }
  }
</script>
