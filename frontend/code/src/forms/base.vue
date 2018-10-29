<script>
  export default {
    props: {
      value: {
        required: true
      },
      placeholder: String,
      label: {
        type: [String, Boolean],
        default: false
      }
    },
    data () {
      return {
        state: 'normal'
      }
    },
    methods: {
      resetInput () {
        let obj = this.value
        obj.value = obj.default
        this.$emit('input', obj)
      }
    }
  }
</script>
