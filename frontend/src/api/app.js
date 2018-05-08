import Vue from 'vue'
import api from './index'
import router from '../router'
import store from '../store'

export default {
  config () {
    return {
      apiURL: Vue.config.app.API_URL,
      headers: {
        'Authorization': 'Token ' + store.getters.token
      }
    }
  },
  request (config, endpoint, params, headers = {}) {
    config.url = `${this.config().apiURL}${endpoint}/`
    config.params = params
    config.headers = Object.assign(api.config().headers, this.config().headers)
    config.headers = Object.assign(config.headers, headers)
    return api.request(config).then(response => {
      return response.data
    }).catch(error => {
      if (!error.response || [404, 500].indexOf(error.response.status) > -1) {
        router.push('error')
      } else {
        return Promise.reject(error)
      }
    })
  },
  getURL (url) {
    let config = {
      method: 'get',
      url: url,
      headers: Object.assign(api.config().headers, this.config().headers)
    }
    return api.request(config).then(response => {
      return response.data
    })
  },

  login (user, password) {
    let config = {
      method: 'post',
      url: `${this.config().apiURL}token-auth/`,
      data: { 'username': user, 'password': password }
    }

    return api.request(config)
  },

  // Events
  createEvent (data) {
    return this.request({ method: 'post', data: data }, `events`)
  },
  getEvents (params) {
    return this.request({ method: 'get' }, 'events', params)
  },
  getEvent (id) {
    return this.request({ method: 'get' }, `events/${id}`)
  },
  editEvent (id, data) {
    let headers = {}

    if ('attachment' in data) {
      headers = {'Content-Type': 'multipart/form-data'}
    }

    return this.request({method: 'patch', data: data}, `events/${id}`, null, headers)
  },
  getEventStatuses () {
    return this.request({ method: 'get' }, 'events-statuses')
  }
}
