import Vue from 'vue'
import Router from 'vue-router'

import store from '@/store'

import NotLoggedIn from '@/auth/not-logged-in'

Vue.use(Router)

export function requireAuth (to, from, next) {
  if (!store.getters['auth/isAuthenticated']) {
    next({
      name: 'NotLoggedIn',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
}

function onlyNotLoggedIn (to, from, next) {
  if (store.getters['auth/isAuthenticated']) {
    next({
      name: 'NotLoggedIn' // TODO: fix this
    })
  } else {
    next()
  }
}

let router = new Router({
  routes: [
    {
      path: '/',
      name: 'NotLoggedIn',
      component: NotLoggedIn,
      beforeEnter: onlyNotLoggedIn
    }
  ]
})

export default router
