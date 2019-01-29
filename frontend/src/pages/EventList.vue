<template>
  <div>
    <data-table
        :items="events"
        :headers="headers"
        :loading="loading"
        :row-action="toDetailRoute"
        hide-actions>
      <template slot="row" slot-scope="row">
        <td>
          <v-avatar
            v-if="row.item.group && row.item.group.logo != ''"
            size="40"
            :tile="true"
          >
            <img :src="row.item.group.logo" :alt="row.item.group.name">
          </v-avatar>

          {{ row.item.group ? row.item.group.name : "" }}
        </td>
        <td>
          {{ row.item.title }}
        </td>
        <td>{{ row.item.start|format-date-time }}</td>
        <td>{{ row.item.location }}</td>
        <td>{{ row.item.status }}</td>
        <td align="center">{{ row.item.google_calendar_published ? "Si" : "No" }}</td>

      </template>
    </data-table>

    <v-btn
        color="primary"
        dark
        bottom
        right
        fab
        fixed
        to="/event-add/"
    >
      <v-icon>add</v-icon>
    </v-btn>
  </div>
</template>


<script>
  import api from '@/api/app'
  import DataTable from '@/components/DataTable'
  import formMixin from '@/mixins/formMixin'
  import mutationsMixin from '@/mixins/mutationsMixin'

  export default {
    name: 'eventsList',
    components: {DataTable},
    pagination: {'sortBy': 'start', 'descending': false},
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
            text: 'Título',
            align: 'left',
            sortable: true,
            value: 'title'
          },
          {
            text: 'Data',
            align: 'left',
            sortable: true,
            value: 'start'
          },
          {
            text: 'Localización',
            align: 'left',
            sortable: true,
            value: 'location'
          },
          {
            text: 'Estado',
            align: 'left',
            sortable: true,
            value: 'status'
          },
          {
            text: 'Google calendar',
            align: 'center',
            sortable: true,
            value: 'google_calendar_published'
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
