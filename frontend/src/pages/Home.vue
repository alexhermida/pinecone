<template>
<div>
  <v-container fluid justify-center>
    <v-layout justify-center align-center>
      <v-flex xs10 class="has-text-centered">
        <img src="/static/img/logo-vigotech-vertical-150px.png" />
      </v-flex>
    </v-layout>
  </v-container>
  <v-subheader>Próximos eventos</v-subheader>
  <v-container
    fluid
    grid-list-md
  >
    <v-layout row wrap>
      <v-flex
        v-for="(card, index) in events"
        xs12 sm6
        :key="card.id"
      >
        <v-card>
          <v-card-title primary-title>
            <v-avatar
                v-if="card.group && card.group.logo != ''"
                size="40"
                :tile="true"
            >
              <img :src="card.group.logo" :alt="card.group.name">
            </v-avatar>
            <div>
              <div class="headline mb-0">
                {{ card.title }}
              </div>
              <div>{{ card.start |format-date-time }}</div>
            </div>
          </v-card-title>
          <v-card-actions>
            <v-btn icon @click="show = !show">
              <v-icon>{{ !show ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
                :to="{name: 'event-detail', params: {'id': card.id}}"
                color="primary"
            >
              Ver
            </v-btn>
          </v-card-actions>

          <v-slide-y-transition>
            <v-card-text v-show="show">
              <p>
                {{ card.description }}
              </p>

              <v-chip v-if="card.location">
                <v-icon>location_on</v-icon> {{ card.location }}
              </v-chip>
              <v-chip v-if="card.link">
                <v-icon>link</v-icon> {{ card.link }}
              </v-chip>
              <v-chip>
                <v-icon>calendar_today</v-icon> gCalendar: {{ card.google_calendar_published ? 'Si' : 'Non' }}
              </v-chip>
              <v-chip>
                <v-icon>public</v-icon> {{ card.status }}
              </v-chip>
            </v-card-text>
          </v-slide-y-transition>
        </v-card>
      </v-flex>
    </v-layout>
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
