import axios from 'axios'
import Qs from 'qs'

export default {
  config () {
    return {
      mode: 'no-cors',
      responseType: 'json',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      'paramsSerializer': function (params) {
        return Qs.stringify(params, { arrayFormat: 'repeat' })
      }
    }
  },
  request (config) {
    config = Object.assign(this.config(), config)
    return axios(config)
  }
}
