<script>
import _ from 'lodash'

import DatePicker from '@/components/DatePicker'
import TimePicker from '@/components/TimePicker'

export default {
  name: 'formMixin',
  components: {DatePicker, TimePicker},
  data () {
    return {
      fieldErrors: {},
      valid: false,
      loading: false
    }
  },
  computed: {
    nonFieldErrors () {
      return this.fieldErrors['non_field_errors']
    },
    hasNonFieldErrors () {
      return this.fieldErrors['non_field_errors'] && this.fieldErrors['non_field_errors'].length > 0
    }
  },
  methods: {
    submit (event) {
      if (!this.valid) { return }
      this.loading = true
      this.fieldErrors = {}
      this.onSubmit().then(response => {
        this.loading = false
        if (this.onSuccess) {
          this.onSuccess(response)
        }
      }).catch((error) => {
        this.loading = false
        this.fieldErrors = error.response.data
        if (this.onError) {
          this.onError(error.response)
        }
      })
    },
    debounceSubmit: _.debounce(function () { this.submit() }, 1000)
  }
}
</script>
