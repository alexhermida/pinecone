import Vue from 'vue'
import Vuex from 'vuex'

import router from '../router'

import { ACTION_SUCCESS, ACTION_ERROR, TO_ROUTE } from './mutations'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    menu: [
      { icon: 'assignment', iconClass: 'red white--text', title: 'Eventos', subtitle: 'Listado', route: 'events-list' },
      { icon: 'calendar_today', iconClass: 'red white--text', title: 'Calendario', subtitle: 'Calendario', route: 'calendar' }
    ],
    notify: {
      timeout: 5000,
      message: null,
      mode: null,
      textColor: null,
      backgroundColor: null,
      visible: false,
      position: 'bottom'
    },
    session: {}
  },
  actions: {
    logIn ({ state }, data) {
      state.session = { token: data.token, profile: data.profile }
      localStorage.setItem(Vue.config.app.sessionName, JSON.stringify(state.session))
      router.push({ name: 'home' })
    },
    logOut ({ state }) {
      state.session = {
        profile: {},
        token: null
      }
      localStorage.removeItem(Vue.config.app.sessionName)
      router.push({ name: 'login' })
    }
  },
  getters: {
    authenticated (state) {
      return state.session && state.session.token
    },
    profile (state) {
      return state.session.profile || {}
    },
    token (state) {
      return state.session.token || null
    }
  },
  mutations: {
    initialiseStore (state) {
      const sessionName = Vue.config.app.sessionName
      if (localStorage.getItem(sessionName)) {
        Object.assign(state.session, JSON.parse(localStorage.getItem(sessionName)))
      }
    },
    [ACTION_SUCCESS] (state, message) {
      Object.assign(state.notify, {
        message: message,
        backgroundColor: null,
        textColor: 'success',
        visible: true
      })
    },
    [ACTION_ERROR] (state, message) {
      Object.assign(state.notify, {
        message: message,
        backgroundColor: 'error',
        textColor: null,
        visible: true,
        position: 'top'
      })
    },
    [TO_ROUTE] (state, name) {
      if (name === 'logout') {
        this.logout()
      } else {
        router.push({ name: name })
      }
    }
  }
})
