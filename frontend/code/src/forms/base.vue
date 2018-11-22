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
    methods: {
      inputClass () {
        let errors = this.value.errors
        return {'is-invalid': errors && errors.length > 0}
      }
    }
  }
</script>
