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
              <v-flex xs12 sm4>
                <date-picker
                    :date.sync="startDate"
                    label="Fecha comienzo"
                    @change="fieldErrors.start = []"/>
              </v-flex>
              <v-flex xs12 sm4>
                <time-picker
                  :time.sync="startTime"
                  @change="fieldErrors.start = []"
                  label="Hora comienzo"/>
              </v-flex>
              <v-flex xs12 sm4>
                <v-text-field
                  label="Duración"
                  suffix="minutos"
                  type="number"
                  v-model="event.duration"
                  @input="fieldErrors.duration = []"
                  :error-messages="fieldErrors.duration"
                  />
              </v-flex>
              <v-flex xs12 sm6>
                <v-switch
                  v-model="event.google_calendar_published"
                  label="Publicar Google Calendar"
                  @input="fieldErrors.google_calendar_published = []"
                  :error-messages="fieldErrors.google_calendar_published"
                ></v-switch>
              </v-flex>
              <v-flex xs12 sm6>
                <v-btn :disabled="disableCalendarBtn()" round color="primary" :href="event.google_event_htmllink" target="_blank">Abrir no calendario</v-btn>
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
  props: ['errors'],
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
        group: this.event.group,
        status: this.event.status,
        title: this.event.title,
        description: this.event.description,
        link: this.event.link,
        location: this.event.location,
        start: this.$options.filters.joinDateTime(this.event.startDate, this.event.startTime),
        duration: this.event.duration,
        google_calendar_published: this.event.google_calendar_published
      }
    },
    onSubmit () {
      return api.editEvent(this.event.id, this.submitData())
    },
    onSuccess () {
      this.success('Evento actualizada con éxito')
    },
    onError () {
      if (this.nonFieldErrors) {
        this.error(this.nonFieldErrors.join(' '))
      }
    },
    disableCalendarBtn () {
      this.disableCalendarButton = !this.event.google_event_htmllink
      return this.disableCalendarButton
    }
  }
}
</script>
