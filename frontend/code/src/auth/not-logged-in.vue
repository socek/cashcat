<template>
  <div class="row justify-content-md-center">
    <div class="col-lg-4">
      <h1>Please log in</h1>
      <ccform ref="form" v-model="form" @submit="onSubmit" :showCancel="false" okButtonLabel="Zaloguj">
        <text-input v-model="form.email" label="Email" placeholder="email@email.com"></text-input>
        <password-input v-model="form.password" label="Hasło"></password-input>
      </ccform>
    </div>
  </div>
</template>

<script>
import authResource from '@/auth/resource'
import form from '@/forms'

export default {
  data () {
    return {
      form: form({
        email: '',
        password: ''
      }),
      resource: authResource(this)
    }
  },
  methods: {
    onSubmit (form) {
      this.resource.login({}, form).then((response) => {
        this.$store.commit('auth/logIn', response.body.jwt)
        this.$router.push({name: 'WalletList'})
      }).catch(this.$refs.form.parseErrorResponse)
    }
  }
}
</script>
