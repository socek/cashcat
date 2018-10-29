<template>
  <div>
    <b-btn size="sm" :variant="variant" @click="showModal" v-b-tooltip.hover :title="title">
      <slot name="anhor"></slot>
    </b-btn>

    <b-modal ref="modal" :size="size" :title="title" hide-footer>
      <ccform ref="form" v-model="value" @submit="onSubmit" @cancel="$refs.modal.hide()" v-show="!isBusy">
        <slot name="content"></slot>
      </ccform>
      <div v-show="isBusy" class="modal-spiner">
        <icon name="sync" scale="2" spin></icon>
      </div>
    </b-modal>
  </div>
</template>

<script>
  export default {
    props: {
      title: String,
      variant: {
        type: String,
        default: 'outline-primary'
      },
      fetchContent: {
        default: false
      },
      size: {
        default: 'md'
      },
      value: {
        type: Object,
        required: true
      }
    },
    data () {
      return {
        isBusy: true,
        withLoading: this.fetchContent && true
      }
    },
    methods: {
      showModal (modal) {
        this.isBusy = this.withLoading
        this.$refs.modal.show()
        if (this.fetchContent) {
          this.fetchContent().then((response) => {
            this.$refs.form.setDefaults(response.body)
            this.isBusy = false
          })
        } else {
          this.$refs.form.resetForm()
        }
      },
      onSubmit (fields) {
        this.$emit('submit', fields)
      },
      onSuccess () {
        this.$refs.modal.hide()
        this.$emit('success')
      },
      parseErrorResponse (response) {
        return this.$refs.form.parseErrorResponse(response)
      }
    }
  }
</script>

<style scoped>
  .modal-spiner {
    text-align: center;
  }
  .save {
    float: left;
  }
  .cancel {
    float: right;
  }
</style>
