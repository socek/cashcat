<script>
  export default {
    props: ['value'],
    methods: {
      getClass () {
        return {
          'form-control': true,
          'is-invalid': this.value.errors.length > 0
        }
      },
      sendUpdate () {
        this.$emit('input', this.value)
      }
    }
  }
</script>
