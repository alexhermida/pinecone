<template>
  <v-card>
    <v-card-text>
      <v-container grid-list-lg fill-height>
        <v-form ref="form" enctype="multipart/form-data" novalidate v-model="valid">
          <v-layout wrap>
            <v-flex v-if="!isNew" xs6 sm4>
                <v-text-field
                  v-model="created"
                  label="Creado"
                  disabled
                ></v-text-field>
              </v-flex>
              <v-flex v-if="!isNew" xs6 sm4>
                <v-text-field
                  v-model="modified"
                  label="Modificado"
                  disabled
                ></v-text-field>
              </v-flex>
              <v-flex v-if="!isNew" xs6 sm4>
                <v-text-field
                  v-model="event.status"
                  label="Estado"
                  disabled
                ></v-text-field>
              </v-flex>
              <v-flex xs12 md3 d-flex>
                <v-select
                  :items="masters.groups"
                  item-text="name"
                  item-value="id"
                  label="Grupo"
                  v-model="event.group"
                  @input="fieldErrors.group = []"
                  :error-messages="fieldErrors.group"
                ></v-select>
              </v-flex>
              <v-flex xs12 md9>
                <v-text-field
                  v-model="event.title"
                  label="Título"
                  required
                  @input="fieldErrors.title = []"
                  :error-messages="fieldErrors.title"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-textarea
                  v-model="event.description"
                  label="Descripción"
                  :rules="descriptionRules" class="textarea" required
                  @input="fieldErrors.description = []"
                  :error-messages="fieldErrors.description"

                ></v-textarea>
              </v-flex>
              <v-flex xs6 sm4>
                <v-text-field
                  v-model="event.link"
                  label="Ligazón"
                  @input="fieldErrors.link = []"
                  :error-messages="fieldErrors.link"
                  prepend-icon="link"
                ></v-text-field>
              </v-flex>
              <v-flex xs6 sm4>
                <v-text-field
                  v-model="event.location"
                  label="Localización"
                  @input="fieldErrors.location = []"
                  :error-messages="fieldErrors.location"
                  prepend-icon="place"
                ></v-text-field>
              </v-flex>
          </v-layout>
          <v-layout wrap>
              <v-flex xs12 sm4>
                <date-picker
                  :date.sync="startDate"
                  label="Data comenzo"
                  @change="fieldErrors.start = []"/>
              </v-flex>
              <v-flex xs12 sm4>
                <time-picker
                  :time.sync="startTime"
                  @change="fieldErrors.start = []"
                  label="Hora comenzo"/>
              </v-flex>
              <v-flex xs12 sm4>
                <v-text-field
                  label="Duración"
                  suffix="minutos"
                  type="number"
                  v-model="event.duration"
                  @input="fieldErrors.duration = []"
                  :error-messages="fieldErrors.duration"
                  prepend-icon="keyboard_tab"
                  />
              </v-flex>
          </v-layout>
          <v-layout>
              <v-flex xs12 sm6>
                <v-switch
                  v-model="event.google_calendar_published"
                  label="Publicado en Google Calendar"
                  color="primary"
                  @input="fieldErrors.google_calendar_published = []"
                  :error-messages="fieldErrors.google_calendar_published"
                ></v-switch>
              </v-flex>
              <v-flex v-if="!isNew" xs12 sm6>
                <v-btn
                  :disabled="!event.google_event_htmllink"
                  round
                  color="primary"
                  :href="event.google_event_htmllink"
                  target="_blank"
                >
                  Abrir no calendario
                </v-btn>
              </v-flex>
          </v-layout>
        </v-form>
      </v-container>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
          @click="$router.push('/events-list')"
          :loading="loading"
          color="primary"
          flat
          large
      >
        Cancelar
      </v-btn>

      <v-btn
        @click="submit"
        :disabled="!valid"
        :loading="loading"
        color="primary"
        large
        >
          Gardar
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<script>
import api from '@/api/app'
import formMixin from '@/mixins/formMixin'
import mutationsMixin from '@/mixins/mutationsMixin'

export default {
  name: 'eventDetail',
  props: ['errors'],
  mixins: [formMixin, mutationsMixin],
  mounted () {
    this.loading = true

    let p1
    if (!this.isNew) {
      p1 = api.getEvent(this.$route.params.id).then(response => {
        this.event = response
      })
    }

    let p2 = api.getEventStatuses().then(response => {
      this.masters.statuses = response
    })

    let p3 = api.getGroups().then(response => {
      this.masters.groups = response
    })

    Promise.all([p1, p2, p3]).then(() => {
      this.loading = false
    })
  },
  computed: {
    isNew () {
      return !this.$route.params.id
    },
    created () {
      return this.$options.filters.formatDateTime(this.event.created)
    },
    modified () {
      return this.$options.filters.formatDateTime(this.event.modified)
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
        event: {
          url: './events/' + this.$route.params.id + '/',
          method: 'PATCH',
          withCredentials: false,
          headers: api.config().headers,
          timeout: 7000
        }
      },
      startDate: null,
      startTime: null,
      disableCalendarButton: true
    }
  },
  watch: {
    valid () {
      this.$emit('update:isValid', this.valid)
    },
    event () {
      const startDateTime = this.$options.filters.splitDateTime(this.event.start)
      if (startDateTime) {
        this.startDate = startDateTime.date
        this.startTime = startDateTime.time
      }
    },
    startDate () {
      this.event.startDate = this.startDate
      this.$emit('update:event', this.event)
    },
    startTime () {
      this.event.startTime = this.startTime
      this.$emit('update:event', this.event)
    }
  },
  methods: {
    submitData () {
      return {
        group: this.event.group.id ? this.event.group.id : this.event.group,
        status: this.event.status,
        title: this.event.title,
        description: this.event.description,
        link: this.event.link,
        location: this.event.location,
        start: this.$options.filters.joinDateTime(this.startDate, this.startTime),
        duration: this.event.duration,
        google_calendar_published: this.event.google_calendar_published
      }
    },
    onSubmit () {
      if (this.isNew) {
        return api.createEvent(this.submitData())
      } else {
        return api.editEvent(this.event.id, this.submitData()).then(response => {
          this.event = response
        })
      }
    },
    onSuccess () {
      this.success('Evento actualizado con éxito')
      this.$router.push('/events-list')
    },
    onError () {
      if (this.nonFieldErrors) {
        this.error(this.nonFieldErrors.join(' '))
      }
    }
  }
}
</script>
