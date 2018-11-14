<template>
  <li class="nav-item text-nowrap">
    <a class="nav-link" @click="logout" href="#">Logout</a>
  </li>
</template>

<script>
  export default {
    methods: {
      logout (event) {
        this.$store.commit('auth/logOut')
        this.$router.push({name: 'NotLoggedIn'})
        event.preventDefault()
      }
    }
  }
</script>
