<template>
  <div class="row justify-content-md-center">
    <div class="col-lg-4">
      <h1>Please log in</h1>
      <ccform ref="form" @submit="onSubmit" :showCancel="false" okButtonLabel="Zaloguj">
        <text-input name="email" label="Email" placeholder="email@email.com"></text-input>
        <password-input name="password" label="Hasło"></password-input>
      </ccform>
    </div>
  </div>
</template>

<script>
import textInput from '@/forms/text'
import passwordInput from '@/forms/password'
import ccform from '@/forms/form'
import authResource from '@/auth/resource'

export default {
  data () {
    return {
      resource: authResource(this)
    }
  },
  methods: {
    onSubmit (event, form) {
      this.resource.login({}, form.fields).then((response) => {
        this.$store.commit('auth/logIn', response.body.jwt)
        this.$router.push({name: 'WalletList'})
      }).catch(this.$refs.form.catchError)
    }
  },
  components: {
    textInput,
    passwordInput,
    ccform
  }
}
</script>
