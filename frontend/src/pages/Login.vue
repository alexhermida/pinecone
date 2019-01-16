<template>
  <div>
    <v-app id="inspire">
      <v-content>
        <v-container fluid fill-height>
          <v-layout align-center justify-center>
            <v-flex xs12 sm8 md4>
              <v-form ref="form" v-on:submit.prevent="submit" v-model="valid">

                <v-flex xs12 class="logo-wrapper mb-4">
                  <v-layout align-center justify-center>
                    <img src="/static/img/vigotech-white-horizontal.png" alt="VigoTech">
                  </v-layout>
                </v-flex>

                <v-card class="login-box-wrapper elevation-12">
                  <v-card-text>
                      <v-text-field
                        @keyup.enter.native="logIn"
                        prepend-icon="person"
                        v-model="username"
                        name="login"
                        label="Login"
                        type="text"
                        @change="fieldErrors.username = []"
                        :error-messages="fieldErrors.username"
                        :error="hasNonFieldErrors"
                        ></v-text-field>
                      <v-text-field
                        @keyup.enter.native="logIn"
                        prepend-icon="lock"
                        v-model="password"
                        name="password"
                        label="Password"
                        id="password"
                        type="password"
                        @change="fieldErrors.password = []"
                        :error-messages="fieldErrors.password"
                        :error="hasNonFieldErrors"
                        ></v-text-field>
                  </v-card-text>
                  <v-card-actions>
                    <v-btn type="submit" block color="primary" dark>Acceder</v-btn>
                  </v-card-actions>
                </v-card>
              </v-form>
            </v-flex>
          </v-layout>
        </v-container>
      </v-content>
  </v-app>
</div>
</template>

<script>
import api from '@/api/app'
import formMixin from '@/mixins/formMixin'
import mutationsMixin from '@/mixins/mutationsMixin'
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'login',
  mixins: [formMixin, mutationsMixin],
  mounted () {
    if (this.authenticated) {
      this.$router.push({name: 'home'})
    }
  },
  data () {
    return {
      drawer: null,
      showLegalInfo: false,
      loading: false,
      username: '',
      password: ''
    }
  },
  computed: { ...mapGetters(['authenticated']) },
  methods: {
    ...mapActions(['logIn']),
    onSubmit () {
      return api.login(this.username, this.password)
    },
    onSuccess (response) {
      return this.logIn(response.data)
    },
    onError () {
      if (this.nonFieldErrors) {
        this.error(this.nonFieldErrors.join(' '))
      }
    }
  },
  props: {
    source: String
  }
}
</script>
