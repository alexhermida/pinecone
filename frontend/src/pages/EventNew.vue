<template>
  <v-card>
    <v-card-text>
      <v-container grid-list-lg fill-height>
        <v-form ref="form" enctype="multipart/form-data" novalidate v-model="valid">
          <v-layout wrap>
              <v-flex xs12>
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
              <v-flex xs12 md3>
                <v-text-field
                  v-model="event.group"
                  label="Grupo"
                  required
                  @input="fieldErrors.group = []"
                  :error-messages="fieldErrors.group"
                ></v-text-field>
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
                <v-text-field
                  v-model="event.description"
                  label="Descripción"
                  multi-line
                  :rules="descriptionRules" class="textarea" required
                  @input="fieldErrors.description = []"
                  :error-messages="fieldErrors.description"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="event.link"
                  label="Enlace"
                  @input="fieldErrors.link = []"
                  :error-messages="fieldErrors.link"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  v-model="event.location"
                  label="Localización"
                  @input="fieldErrors.location = []"
                  :error-messages="fieldErrors.location"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 sm6>
                <date-picker
                    :date.sync="startDate"
                    label="Fecha comienzo"
                    @change="fieldErrors.start = []"
                    :error-messages="fieldErrors.start"/>
              </v-flex>
              <v-flex xs12 sm6>
                <time-picker
                  :time.sync="startTime"
                  @change="fieldErrors.start = []"
                  label="Hora comienzo"/>
              </v-flex>
              <v-flex xs12 sm6>
                <date-picker
                  :date.sync="endDate"
                  label="Fecha fin"
                  @change="fieldErrors.end = []"
                  :error-messages="fieldErrors.end"/>
              </v-flex>
              <v-flex xs12 sm6>
                <time-picker
                  :time.sync="endTime"
                  @change="fieldErrors.end = []"
                  label="Hora fin"/>
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
          Crear
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<script>
import api from '@/api/app'
import formMixin from '@/mixins/formMixin'
import mutationsMixin from '@/mixins/mutationsMixin'

export default {
  props: ['isValid', 'showCancel', 'title', 'actionName'],
  mixins: [formMixin, mutationsMixin],
  mounted () {
    this.loading = true

    let p1 = api.getEventStatuses().then(response => {
      this.masters.statuses = response
    })

    Promise.all([p1]).then(() => {
      this.loading = false
    })
  },
  data () {
    return {
      masters: {},
      event: {},
      descriptionRules: [
        v => !!v || 'Descripción es obligatoria'
      ],
      startDate: null,
      startTime: null,
      endDate: null,
      endTime: null
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
      const endDateTime = this.$options.filters.splitDateTime(this.event.end)
      if (endDateTime) {
        this.endDate = endDateTime.date
        this.endTime = endDateTime.time
      }
    },
    startDate () {
      this.event.startDate = this.startDate
      this.$emit('update:event', this.event)
    },
    startTime () {
      this.event.startTime = this.startTime
      this.$emit('update:event', this.event)
    },
    endDate () {
      this.event.endDate = this.endDate
      this.$emit('update:event', this.event)
    },
    endTime () {
      this.event.endTime = this.endTime
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
        end: this.$options.filters.joinDateTime(this.event.endDate, this.event.endTime),
        google_calendar_published: this.event.google_calendar_published
      }
    },
    onSubmit () {
      return api.createEvent(this.submitData())
    },
    onSuccess (response) {
      if (this.callback) {
        this.callback()
      } else {
        let route = {name: 'event-detail', params: {'id': response.id}}
        this.$router.push(route)
      }
      this.success('Evento creado con éxito')
    }
  }
}
</script>
