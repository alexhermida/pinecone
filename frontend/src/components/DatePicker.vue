<template>
  <v-dialog
    ref="dialog"
    persistent
    v-model="modal"
    lazy
    full-width
    width="290px"
    :date.sync="selectedDate"
  >
    <v-text-field
      slot="activator"
      :label="label"
      v-model="displayDate"
      prepend-icon="event"
      :error-messages="errors"
      readonly
    ></v-text-field>
    <v-date-picker v-model="selectedDate" scrollable
      :first-day-of-week="1"
      locale="es-es"
      >
      <v-spacer></v-spacer>
      <v-btn flat color="primary" @click="modal = false">Cancelar</v-btn>
      <v-btn flat color="primary" @click="accept()">Aceptar</v-btn>
    </v-date-picker>
  </v-dialog>
</template>

<script>
export default {
  props: ['date', 'label', 'errors'],
  data () {
    return {
      selectedDate: this.date,
      modal: false
    }
  },
  methods: {
    accept () {
      this.$emit('update:date', this.selectedDate)
      this.modal = false
    }
  },
  computed: {
    displayDate () {
      return this.$options.filters.formatDate(this.date)
    }
  }
}
</script>

