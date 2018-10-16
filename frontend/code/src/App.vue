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

    <div class="container-fluid" id="content_container">
      <register v-if="!isAuthenticated"></register>
      <div class="row">
        <nav class="col-md-2 d-none d-md-block bg-light sidebar">
          <div class="sidebar-sticky">
            <ul class="nav flex-column">
              <li class="nav-item">
                <a class="nav-link active" href="#">
                  <icon name="wallet" /> Portfele
                </a>
              </li>
            </ul>
          </div>
        </nav>
        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 pt-3 px-4">
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
