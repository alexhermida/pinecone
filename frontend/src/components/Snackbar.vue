<template>
  <v-snackbar
    :timeout="options.timeout"
    :color="options.backgroundColor"
    :multi-line="options.mode === 'multi-line'"
    :vertical="options.mode === 'vertical'"
    :top="options.position === 'top'"
    :bottom="options.position === 'bottom'"
    :right="options.position === 'right'"
    :left="options.position === 'left'"
    v-model="options.visible"
  >
    {{ options.message }}
    <v-btn flat :color="options.textColor" @click.native="options.visible = false">Cerrar</v-btn>
  </v-snackbar>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: mapState({
    options: state => state.notify
  })
}
</script>