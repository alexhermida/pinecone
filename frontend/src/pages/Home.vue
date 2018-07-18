<template>
<div>
  <v-container fluid justify-center>
    <v-layout justify-center align-center>
      <v-flex xs10 class="has-text-centered">
        <img src="/static/img/logo-vigotech-vertical-150px.png" />
      </v-flex>
    </v-layout>
  </v-container>
  <v-container
    fluid
    grid-list-md
  >
    <v-layout row wrap>
      <v-flex
        v-for="(card, index) in events"
        v-bind:class="{ xs12: index == 0 }"
        :key="card.id"
      >
        <v-card>
          <v-card-media
            :src=card.src
            height="100px"
          >
          </v-card-media>

          <v-card-title primary-title>
            <div>
              <div class="headline">{{ card.title }}</div>
              <span class="grey--text">{{ card.group }}</span>
            </div>
          </v-card-title>

          <v-card-actions>
            <v-btn flat>Review</v-btn>
            <v-spacer></v-spacer>
            <v-btn icon @click="show = !show">
              <v-icon>{{ show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
            </v-btn>
          </v-card-actions>

          <v-slide-y-transition>
            <v-card-text v-show="show">
              {{ card.description }}
            </v-card-text>
          </v-slide-y-transition>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
  <v-container>
    <iframe src="https://calendar.google.com/calendar/embed?src=orestes.io_fj8ev1vakdnl8l8o6jeljhof1s%40group.calendar.google.com&ctz=Europe%2FMadrid" style="border: 0" width="800" height="600" frameborder="0" scrolling="no"></iframe>
  </v-container>

</div>
</template>

<script>
  import api from '@/api/app'
  import { mapState } from 'vuex'
  import mutationsMixin from '@/mixins/mutationsMixin'

  export default {
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
