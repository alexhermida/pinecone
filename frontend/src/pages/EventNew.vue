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
                  v-model="event.group"
                  label="Grupo"
                  required
                  @input="fieldErrors.group = []"
                  :error-messages="fieldErrors.group"
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
  computed: {
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
      ]
    }
  },
  methods: {
    onSubmit () {
      return api.createEvent(this.event)
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
