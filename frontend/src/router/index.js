import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/pages/Home'
import Calendar from '@/pages/Calendar'
import Event from '@/pages/Event'
import EventNew from '@/pages/EventNew'
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
      path: '/event-add/',
      name: 'event-add',
      component: EventNew,
      meta: { title: route => { return 'Crear Evento' } }
    },
    {
      path: '/event-detail/:id',
      name: 'event-detail',
      component: Event,
      meta: { title: route => { return 'Evento' + route.params.id } }
    },
    {
      path: '/calendar/',
      name: 'calendar',
      component: Calendar,
      meta: { title: route => { return 'Calendar' } }
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
