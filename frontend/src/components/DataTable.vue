<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :disable-initial-sort="true"
    class="elevation-2"
    rows-per-page-text="Por página"
    :rows-per-page-items='[10, 25, 50, {"text": "Todo", "value": -1}]'
    :loading="loading==true">
    <template slot="pageText" slot-scope="props">
      {{ props.pageStart }} - {{ props.pageStop }} de {{ props.itemsLength }}
    </template>
    <template slot="items" slot-scope="props">
      <tr @click="rowAction(props.item.id)">
        <slot name="row" :item="props.item" />
      </tr>
    </template>
    <template slot="no-data">
      <v-alert :value="true" color="warning" icon="warning">
        No hay datos para mostrar
      </v-alert>
    </template>
  </v-data-table>
</template>

<script>
export default {
  props: ['items', 'headers', 'loading', 'rowAction']
}
</script>

