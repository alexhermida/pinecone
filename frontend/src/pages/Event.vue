<template>
  <v-card>
    <v-card-text>
      <v-container grid-list-lg fill-height>
        <v-form ref="form" enctype="multipart/form-data" novalidate v-model="valid">
          <v-layout wrap>
            <v-flex xs6 sm4>
                <v-text-field
                  v-model="created"
                  label="Creado"
                  disabled
                ></v-text-field>
              </v-flex>
              <v-flex xs6 sm4>
                <v-text-field
                  v-model="modified"
                  label="Modificado"
                  disabled
                ></v-text-field>
              </v-flex>
              <v-flex xs6 sm4>
                <v-select
                  :items="masters.statuses"
                  v-model="event.status"
                  :loading="loading"
                  :cache-items="true"
                  label="Estado"
                  item-value="id"
                  item-text="name"
                  @change="fieldErrors.status = []"
                  :error-messages="fieldErrors.status"
                  required
                ></v-select>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="event.title"
                  label="Título"
                  required
                  @input="fieldErrors.title = []"
                  :error-messages="fieldErrors.title"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="event.description"
                  label="Descripción"
                  multi-line
                  :rules="descriptionRules" class="textarea" required
                  @input="fieldErrors.description = []"
                  :error-messages="fieldErrors.description"
                ></v-text-field>
              </v-flex>
              <v-flex xs6 sm4>
                <v-text-field
                  v-model="event.group"
                  label="Grupo"
                  required
                  @input="fieldErrors.group = []"
                  :error-messages="fieldErrors.group"
                ></v-text-field>
              </v-flex>
              <v-flex xs6 sm4>
                <v-text-field
                  v-model="event.link"
                  label="Enlace"
                  @input="fieldErrors.link = []"
                  :error-messages="fieldErrors.link"
                ></v-text-field>
              </v-flex>
              <v-flex xs6 sm4>
                <v-text-field
                  v-model="event.location"
                  label="Localización"
                  @input="fieldErrors.location = []"
                  :error-messages="fieldErrors.location"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-switch
                  v-model="event.google_calendar_published"
                  label="Publicar Google Calendar"
                  @input="fieldErrors.google_calendar_published = []"
                  :error-messages="fieldErrors.google_calendar_published"
                ></v-switch>
              </v-flex>
          </v-layout>
        </v-form>
      </v-container>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        @click="submit"
        :disabled="!valid"
        :loading="loading"
        >
          Guardar
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<script>
import api from '@/api/app'
import formMixin from '@/mixins/formMixin'
import mutationsMixin from '@/mixins/mutationsMixin'

export default {
  mixins: [formMixin, mutationsMixin],
  mounted () {
    this.loading = true

    let p1 = api.getEvent(this.$route.params.id).then(response => {
      this.event = response
    })

    let p2 = api.getEventStatuses().then(response => {
      this.masters.statuses = response
    })

    Promise.all([p1, p2]).then(() => {
      this.loading = false
    })
  },
  computed: {
    created () {
      return this.$options.filters.formatDateTime(this.event.created)
    },
    modified () {
      return this.$options.filters.formatDateTime(this.event.modified)
    },
    submitData () {
      return {
        status: this.event.status,
        description: this.event.description
      }
    }
  },
  data () {
    return {
      masters: {},
      event: {},
      descriptionRules: [
        v => !!v || 'Descripción es obligatoria'
      ],
      server: {
        url: api.config().apiURL,
        process: {
          url: './events/' + this.$route.params.id + '/',
          method: 'PATCH',
          withCredentials: false,
          headers: api.config().headers,
          timeout: 7000
        }
      }
    }
  },
  methods: {
    onSubmit () {
      return api.editEvent(this.event.id, this.submitData)
    },
    onSuccess () {
      this.success('Evento actualizada con éxito')
    }
  }
}
</script>
