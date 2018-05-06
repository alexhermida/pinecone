<template>
<div>
  <event-modal/>
  <data-table :items="events" :headers="headers" :loading="loading" :row-action="toDetailRoute">
    <template slot="row" slot-scope="row" >
      <td>{{ row.item.group }}</td>
      <td>{{ row.item.location }}</td>
      <td>{{ row.item.description }}</td>
      <td>{{ row.item.status }}</td>
      <td>{{ row.item.created|format-date-time }}</td>
      <td>{{ row.item.modified|format-date-time }}</td>
    </template>
  </data-table>
</div>
</template>


<script>
import api from '@/api/app'
import DataTable from '@/components/DataTable'
import EventModal from '@/partials/EventModal'
import formMixin from '@/mixins/formMixin'
import mutationsMixin from '@/mixins/mutationsMixin'

export default {
  components: {DataTable, EventModal},
  mixins: [formMixin, mutationsMixin],
  mounted () {
    this.loading = true

    api.getEvents({page_size: 10}).then(response => {
      this.events = response
      this.loading = false
    })
  },
  data () {
    return {
      headers: [
        {
          text: 'Grupo',
          align: 'left',
          sortable: true,
          value: 'group'
        },
        {
          text: 'Ubicación',
          align: 'left',
          sortable: true,
          value: 'location'
        },
        {
          text: 'Descripción',
          align: 'left',
          sortable: true,
          value: 'description'
        },
        {
          text: 'Estado',
          align: 'left',
          sortable: true,
          value: 'status'
        },
        {
          text: 'Creado',
          align: 'left',
          sortable: true,
          value: 'created'
        },
        {
          text: 'Modificado',
          align: 'left',
          sortable: true,
          value: 'modified'
        }
      ],
      events: [],
      requiredRules: [
        v => !!v || 'Campo obligatorio'
      ]
    }
  },
  methods: {
    toDetailRoute (id) {
      this.$router.push({name: 'event-detail', params: {'id': id}})
    }
  }
}
</script>
