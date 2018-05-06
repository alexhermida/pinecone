<script>
import { mapMutations } from 'vuex'

export default {
  name: 'storeMixin',
  methods: {
    ...mapMutations(['success', 'error', 'toRoute'])
  }
}
</script>