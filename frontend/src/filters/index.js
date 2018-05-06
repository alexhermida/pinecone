import moment from 'moment'
import Vue from 'vue'

Vue.filter('formatDateTime', function (value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY HH:mm')
  }
})

Vue.filter('formatDate', function (value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY')
  }
})

Vue.filter('joinDateTime', function (date, time) {
  if (date || time) {
    if (!date) {
      date = moment.format('DD/MM/YYYY')
    }
    if (!time) {
      time = '00:00'
    }
    return moment(`${date} ${time}`).toDate()
  }
})

Vue.filter('splitDateTime', function (datetime) {
  if (datetime) {
    return {
      date: moment(datetime).format('YYYY-MM-DD'),
      time: moment(datetime).format('HH:mm')
    }
  }
})
