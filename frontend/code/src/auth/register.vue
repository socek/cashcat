<template>
  <dialogform
    title="Zarejestruj się"

    v-if="!isAuthenticated"
    variant="danger"
    ref="dialog"
    v-model="form"
    @submit="onSubmit">

    <template slot="anhor">
      Zarejestruj
    </template>

    <template slot="content">
      <text-input v-model="form.name" label="Imię" placeholder="Nick"></text-input>
      <text-input v-model="form.email" label="Email" placeholder="sample@email.com"></text-input>
      <password-input v-model="form.password" label="Hasło"></password-input>
      <password-input v-model="form.confirmPassword" label="Powtórz hasło"></password-input>

    </template>
  </dialogform>
</template>

<script>
import authResource from '@/auth/resource'
import form from '@/forms'

export default {
  data () {
    return {
      form: form({
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
      }),
      resource: authResource(this)
    }
  },
  methods: {
    onSubmit (form) {
      form.submit(
        () => this.resource.signUp({}, form.toData()),
        (response) => {
          this.$store.commit('auth/logIn', response.body.jwt)
          this.$router.push({name: 'WalletList'})
        }
      )
    }
  },
  computed: {
    isAuthenticated () {
      return this.$store.getters['auth/isAuthenticated']
    }
  }
}
</script>
