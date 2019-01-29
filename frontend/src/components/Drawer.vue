<template>
  <v-navigation-drawer v-if="authenticated" fixed :clipped="$vuetify.breakpoint.lgAndUp" app v-model="drawerState">
    <v-toolbar flat color="primary" dark class="transparent">
      <v-list dense>
        <v-list-tile avatar>
          <v-avatar>
            <img src="/static/img/logo-simbolo-vigotech.png" alt="VigoTech">
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
      <v-list-tile href="https://vigotech.org/" target="_blank">
        <v-list-tile-action>
          <v-icon>web</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>https://vigotech.org</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile @click="logout()">
        <v-list-tile-action>
          <v-icon>exit_to_app</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>Sair</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'

  export default {
    props: {
      value: {
        default: true
      }
    },
    actions: {
      logout () {
        this.$emit('logout')
      }
    },
    computed: {
      drawerState: {
        get () {
          return this.value
        },
        set (value) {
          this.$emit('input', value)
        }
      },
      ...mapState({
        navigation: state => state.menu
      }),
      ...mapGetters(['authenticated', 'profile'])
    }
  }
</script>