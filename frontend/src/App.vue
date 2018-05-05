<template>
  <div id="app" :class="`page ${currentRouteName}-page`">
    <v-app>
      <v-navigation-drawer v-if="authenticated" fixed :clipped="$vuetify.breakpoint.lgAndUp" app v-model="drawer">
        <v-toolbar flat color="red" dark class="transparent">
          <v-list dense>
            <v-list-tile avatar>
              <v-avatar size="24">
                <img src="/static/img/logo-vigotech-vertical-150px.png" alt="VigoTech">
              </v-avatar>
              <v-list-tile-content>
                <v-list-tile-title class="ml-1">
                  {{ profile.fullname }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
          </v-toolbar>
        <v-divider></v-divider>
        <v-list dense class="pt-0">
          <v-list-tile :to="{name: 'home'}">
            <v-list-tile-action>
              <v-icon>home</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Inicio</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile v-for="item in navigation" :key="item.title" :to="{ name: item.route}">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile @click="logOut()">
            <v-list-tile-action>
              <v-icon>exit_to_app</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Salir</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-navigation-drawer>

      <v-toolbar v-if="authenticated" color="red" dark :clipped-left="$vuetify.breakpoint.lgAndUp" fixed app>
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <v-toolbar-title>{{ $route.meta.title($route) }}</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>

      <v-content>
        <router-view :class="`page ${$route.name}-page`" />
      </v-content>

      <snackbar/>
    </v-app>
  </div>

</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex'
import mutationsMixin from '@/mixins/mutationsMixin'
import Snackbar from '@/components/Snackbar'

export default {
  name: 'app',
  components: {Snackbar},
  mixins: [mutationsMixin],
  beforeCreate () {
    this.$store.commit('initialiseStore')
  },
  data () {
    return {
      drawer: null,
      snackbar: false
    }
  },
  methods: {
    ...mapActions(['logOut'])
  },
  computed: {
    currentRouteName () {
      return this.$route.name
    },
    ...mapState({
      navigation: state => state.menu
    }),
    ...mapGetters(['authenticated', 'profile'])
  }
}
</script>

<style lang="stylus">
@import url('https://fonts.googleapis.com/css?family=Roboto:300,400,500,700');
@import './assets/stylus/app.styl';
</style>
