import passwordInput from './password'
import textInput from './text'
import ccform from './form'
import dialogform from '@/common/dialogForm'
import dateInput from './date'
import dropdown from './dropdown'

export default {
  install (Vue, options) {
    Vue.component('text-input', textInput)
    Vue.component('ccform', ccform)
    Vue.component('password-input', passwordInput)
    Vue.component('dialogform', dialogform)
    Vue.component('date-input', dateInput)
    Vue.component('dropdown', dropdown)
  }
}
