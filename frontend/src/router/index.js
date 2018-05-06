import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/pages/Home'
// import Event from '@/pages/Event'
import EventList from '@/pages/EventList'
import Login from '@/pages/Login'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/home/',
      name: 'home',
      component: Home,
      meta: { title: route => { return 'Inicio' } }
    },
    {
      path: '/events-list/',
      name: 'events-list',
      component: EventList,
      meta: { title: route => { return 'Eventos' } }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { title: route => { return 'Login' } }
    },
    { path: '*', redirect: { name: 'home' } }
  ]
})

router.beforeEach((to, from, next) => {
  const session = JSON.parse(localStorage.getItem(Vue.config.app.sessionName))
  if (to['name'] !== 'login' && (!session || !session.token)) {
    return next({ name: 'login' })
  }

  if (to.meta.title) {
    document.title = to.meta.title(to)
  }
  return next()
})

export default router
