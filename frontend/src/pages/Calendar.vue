<template>
<div>
  <v-subheader>Calendario de eventos</v-subheader>
  <v-container>
    <iframe src="https://calendar.google.com/calendar/embed?src=orestes.io_fj8ev1vakdnl8l8o6jeljhof1s%40group.calendar.google.com&ctz=Europe%2FMadrid" style="border: 0" width="100%" height="920" frameborder="0" scrolling="no"></iframe>
  </v-container>

</div>
</template>

<script>
  import api from '@/api/app'
  import { mapState } from 'vuex'
  import mutationsMixin from '@/mixins/mutationsMixin'

  export default {
    name: 'calendar',
    mixins: [mutationsMixin],
    mounted () {
      this.loading = true

      api.getEventClosets().then(response => {
        this.events = response
        this.loading = false
      })
    },
    data () {
      return {
        events: [],
        show: false
      }
    },
    computed: mapState({
      items: state => state.menu
    })
  }
</script>
