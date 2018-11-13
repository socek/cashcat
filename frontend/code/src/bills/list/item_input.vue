<template>
  <div class="form-row">
    <div role="group" class="form-group col-md-4">
      <input type="text" v-model="value.name.value" class="form-control" placeholder="Nazwa produktu" :class="{'is-invalid': value.name.errors.length > 0}"  @input="onInput">
      <div class="invalid-feedback" style="display: block;" v-for="message in value.name.errors">{{ message }}</div>
    </div>

    <div role="group" class="form-group col-md-2">
      <dropdown v-model="value.group_uid" :options="groups" :class="{'is-invalid': value.group_uid.errors.length > 0}"></dropdown>
      <div class="invalid-feedback" style="display: block;" v-for="message in value.group_uid.errors">{{ message }}</div>
    </div>

    <div role="group" class="form-group col-md-2 is-valid">
      <input type="number" step="0.00001" v-model="value.quantity.value" class="form-control" placeholder="1.00" :class="{'is-invalid': value.quantity.errors.length > 0}"  @input="onInput">
      <div class="invalid-feedback" style="display: block;" v-for="message in value.quantity.errors">{{ message }}</div>
    </div>

    <div role="group" class="form-group col currency">
      <input type="number" v-model="value.value.value" step="0.01"  @blur="formatCurrency()" class="form-control" :class="{'is-invalid': value.value.errors.length > 0}" placeholder="-1,00" @input="onInput" />
      <div class="input-group-append">
        <span class="input-group-text">PLN</span>
      </div>
      <div class="invalid-feedback" style="display: block;" v-for="message in value.value.errors">{{ message }}</div>
    </div>
    <div role="group" class="form-group col currency">
      <b-btn v-if="isDeleteVisible()" size="sm" variant="outline-danger" @click="$emit('removeItem', value)" title="Usuń produkt">
        <icon name="plus-circle" />
      </b-btn>
    </div>
  </div>
</template>

<script>
import base from '@/forms/base'

export default {
  extends: base,
  props: {
    index: {
      type: Number,
      required: true
    }
  },
  data () {
    return {}
  },
  methods: {
    formatCurrency () {
      let form = this.value
      let currency = form.value.value
      if (currency !== '') {
        form.value.value = Number(currency).toFixed(2)
        this.$emit('input', form)
      }
    },
    onInput () {
      this.$emit('input', this.value)
    },
    isDeleteVisible () {
      let isLast = this.value._isLast
      return !isLast
    }
  },
  computed: {
    groups () {
      let data = [{value: '', text: '(wybierz)'}]
      for (let group of this.$store.state.groups.groups) {
        data.push({value: group.uid, text: group.name})
      }
      return data
    }
  }
}
</script>
