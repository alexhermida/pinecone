<template>
  <v-dialog v-model="dialog" persistent max-width="500px">
    <v-btn color="secondary" dark top right fixed fab slot="activator"><v-icon>add</v-icon></v-btn>
    <v-card>
      <v-card-title>
        <span class="headline">Nuevo Evento</span>
      </v-card-title>
      <v-card-text>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-flex xs12 sm12 md12>
              <v-form ref="form" v-model="valid">
                <v-select
                  v-model="event.status"
                  :items="masters.statuses"
                  :loading="loading"
                  :cache-items="true"
                  :rules="requiredRules"
                  label="Estado"
                  item-value="id"
                  item-text="name"
                  @change="fieldErrors.status = []"
                  :error-messages="fieldErrors.status"
                  required
                ></v-select>
                <v-text-field
                  v-model="event.description"
                  :rules="requiredRules"
                  label="Descripción"
                  multi-line
                  @input="fieldErrors.description = []"
                  :error-messages="fieldErrors.description"
                  required></v-text-field>
              </v-form>
            </v-flex>
          </v-layout>
        </v-container>
        <small>*campos obligatorios</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn flat @click.native="closeDialog()">Cancelar</v-btn>
          <v-btn primary
            @click="submit"
            :disabled="!valid"
            >
              Crear
          </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import api from '@/api/app'
import formMixin from '@/mixins/formMixin'
import mutationsMixin from '@/mixins/mutationsMixin'

export default {
  props: ['callback', 'process'],
  mixins: [formMixin, mutationsMixin],
  mounted () {
    this.loading = true

    // let p1 = api.getEventStatuses().then(response => {
    //   this.masters.statuses = response
    // })

    // Promise.all([p1]).then(() => {
    //   this.loading = false
    // })
  },
  data () {
    return {
      dialog: false,
      masters: {
        severities: [],
        statuses: []
      },
      event: {operator: null, severity: null, status: null, duration: null, description: null},
      requiredRules: [
        v => !!v || 'Campo obligatorio'
      ]
    }
  },
  methods: {
    onSubmit () {
      return api.createEvent(this.event)
    },
    onSuccess (response) {
      this.closeDialog()
      if (this.callback) {
        this.callback()
      } else {
        let route = {name: 'event-detail', params: {'id': response.id}}
        this.$router.push(route)
      }
      this.success('Evento creado con éxito')
    },
    closeDialog () {
      this.event = {severity: null, status: null, description: null}
      this.$refs.form.reset()
      this.dialog = false
    }
  }
}
</script>
