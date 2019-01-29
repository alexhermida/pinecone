<template>
  <div id="app" :class="`page ${currentRouteName}-page`">
    <v-app>

      <drawer @logout="logOut" v-model="drawer"/>

      <v-toolbar v-if="authenticated" color="primary" dark :clipped-left="$vuetify.breakpoint.lgAndUp" fixed app>
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <v-spacer></v-spacer>
        <v-toolbar-title>{{ $route.meta.title($route) }}</v-toolbar-title>
      </v-toolbar>

      <v-content>
        <div class="container page">
          <router-view :class="`page ${$route.name}-page`" />
        </div>
      </v-content>

      <snackbar/>
    </v-app>
  </div>

</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex'
import mutationsMixin from '@/mixins/mutationsMixin'
import Snackbar from '@/components/Snackbar'
import Drawer from '@/components/Drawer'

export default {
  name: 'app',
  components: {
    Drawer,
    Snackbar
  },
  mixins: [mutationsMixin],
  beforeCreate () {
    this.$store.commit('initialiseStore')
  },
  data () {
    return {
      drawer: true,
      snackbar: false,
      mainContent: true
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

<style lang="scss">
  @import './assets/scss/pinecone.scss';
</style>
