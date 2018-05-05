// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'babel-polyfill'

import Vue from 'vue'

import router from './router'
import Vuetify from 'vuetify'

import store from './store'
import App from './App'

Vue.config.productionTip = false
Vue.use(Vuetify)

Vue.config.productionTip = false
Vue.config.app = process.env
Vue.config.app.sessionName = Vue.config.app.APP_NAME + 'Session'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})
