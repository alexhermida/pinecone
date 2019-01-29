<template>
  <v-dialog
    ref="dialog"
    persistent
    v-model="modal"
    lazy
    full-width
    width="290px"
    :time.sync="selectedTime"
  >
    <v-text-field
      slot="activator"
      :label="label"
      v-model="time"
      prepend-icon="access_time"
      :error-messages="errors"
      readonly
    ></v-text-field>
    <v-time-picker
        v-model="selectedTime"
        format="24hr"
        scrollable
    >
      <v-spacer></v-spacer>
      <v-btn flat color="primary" @click="modal = false">Cancelar</v-btn>
      <v-btn flat color="primary" @click="accept()">Aceptar</v-btn>
    </v-time-picker>
  </v-dialog>
</template>

<script>
export default {
  props: ['time', 'label', 'errors'],
  data () {
    return {
      selectedTime: this.time,
      modal: false
    }
  },
  methods: {
    accept () {
      this.$emit('update:time', this.selectedTime)
      this.modal = false
    }
  }
}
</script>

