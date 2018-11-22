// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

// External imports
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import VueResource from 'vue-resource'
import Icon from 'vue-awesome/components/Icon'
import datePicker from 'vue-bootstrap-datetimepicker'
import vSelect from 'vue-select'

// Local imports
import App from '@/App'
import router from '@/routing'
import store from '@/store'
import form from '@/forms/plugin'
import auth from '@/auth/plugin'

// Style imports
import 'vue-awesome/icons'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'pc-bootstrap4-datetimepicker/build/css/bootstrap-datetimepicker.css'
import '@/common/style.css'

// External plugins
Vue.component('icon', Icon)
Vue.use(BootstrapVue)
Vue.use(VueResource)
Vue.use(datePicker)
Vue.component('v-select', vSelect)

// Local plugins
Vue.use(form)
Vue.use(auth)

// Configuration
Vue.config.productionTip = true
Vue.http.options.root = '/api'

/* eslint-disable no-new */
export default new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})

