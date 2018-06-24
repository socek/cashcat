export let _Vue

export default function install (Vue, options) {
  if (install.installed && _Vue === Vue) return
  install.installed = true

  _Vue = Vue

  const isDef = v => v !== undefined

  let checkPath = (vm, to) => {
    options.contexts.forEach((element) => {
      const shouldExists = element.check(vm, to)
      const isExisting = element._existing === true
      if (!(shouldExists && isExisting)) {
        if (shouldExists) {
          element.success(vm, to)
          element._existing = true
        } else {
          element.fail(vm, to)
          element._existing = false
        }
      }
    })
  }

  Vue.prototype._init_context = function () {
    this.$router.beforeEach((to, from, next) => {
      checkPath(this, to)
      next()
    })
    checkPath(this, this.$route)
  }

  Vue.mixin({
    mounted () {
      if (!isDef(this.$parent)) {
        this._init_context()
      }
    }
  })
}
