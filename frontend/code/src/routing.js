import Vue from 'vue'
import Router from 'vue-router'

import store from '@/store'

import NotLoggedIn from '@/auth/not-logged-in'
import WalletList from '@/wallets/list/list'
import BillList from '@/bills/list/list'

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
      path: '/login',
      name: 'NotLoggedIn',
      component: NotLoggedIn,
      beforeEnter: onlyNotLoggedIn
    },
    {
      path: '/',
      name: 'WalletList',
      component: WalletList,
      beforeEnter: requireAuth
    },
    {
      path: '/wallets/:wallet_uid',
      name: 'BillList',
      component: BillList,
      beforeEnter: requireAuth
    }
  ]
})

export default router
