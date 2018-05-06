<template>
<div>
  <v-container fluid justify-center>
    <v-layout justify-center align-center>
      <v-flex xs10 class="has-text-centered">
        <img src="/static/img/logo-vigotech-vertical-150px.png" />
      </v-flex>
    </v-layout>
  </v-container>

  <v-jumbotron>
      <v-layout>
        <v-flex>
          <v-list two-line subheader>
            <v-list-tile v-for="item in items" :key="item.title" avatar @click="toRoute(item.route)">
              <v-list-tile-avatar>
                <v-icon :class="[item.iconClass]">{{ item.icon }}</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-flex>
      </v-layout>
  </v-jumbotron>
</div>
</template>

<script>
  import { mapState } from 'vuex'
  import mutationsMixin from '@/mixins/mutationsMixin'

  export default {
    computed: mapState({
      items: state => state.menu
    }),
    mixins: [mutationsMixin]
  }
</script>
