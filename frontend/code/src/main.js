// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import VueResource from 'vue-resource'
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'
import VueNativeSock from 'vue-native-websocket'
import datePicker from 'vue-bootstrap-datetimepicker'

import App from '@/App'
import router from '@/routing'
import store from '@/store'
import Context from '@/context'
import contexts from '@/contexts'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import '@/common/style.css'
import 'pc-bootstrap4-datetimepicker/build/css/bootstrap-datetimepicker.css'

Vue.config.productionTip = true
Vue.use(BootstrapVue)
Vue.use(VueResource)

Vue.http.options.root = '/api'

Vue.http.interceptors.push((request, next) => {
  if (store.state.auth.jwt) {
    request.headers.set('JWT', store.state.auth.jwt)
  }
  next()
})
Vue.component('icon', Icon)

import passwordInput from '@/forms/password'
import textInput from '@/forms/text'
import ccform from '@/forms/form'
import dialogform from '@/common/dialogForm'
import dateInput from '@/forms/date'
Vue.component('text-input', textInput)
Vue.component('ccform', ccform)
Vue.component('password-input', passwordInput)
Vue.component('dialogform', dialogform)
Vue.component('date-input', dateInput)

Vue.use(VueNativeSock, 'ws://' + window.location.hostname + '/wsapp', {
  connectManually: true
})

store.dispatch('auth/tryAutoLogin')

Vue.use(
  Context,
  {contexts}
)

Vue.use(datePicker)

/* eslint-disable no-new */
export default new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
