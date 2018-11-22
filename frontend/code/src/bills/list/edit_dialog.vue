<template>
  <dialogform
    title="Zmień rachunek"
    size="lg"
    :fetchContent="fetchContent"

    ref="dialog"
    v-model="form"
    @submit="onSubmit"
    @afterFetchContent="onAfterFetchContent">

    <template slot="anhor">
      <icon name="edit"></icon>
    </template>
    <template slot="content">
      <text-input v-model="form.place" label="Miejsce" placeholder="nazwa sklepu"></text-input>
      <date-input v-model="form.billed_at" label="Kiedy"></date-input>
      <item-row
        v-for="(item, index) in form.items"
        v-model="form.items[index]"
        :index="item._index"
        :key="item._index"
        @input="onInput"
        @removeItem="removeItem"></item-row>

      <div class="form-row">
        <div role="group" class="form-group col-md-8">
          &nbsp;
        </div>
        <div role="group" class="form-group col">
          Suma:
        </div>
        <div role="group" class="form-group col">
          {{sum}} PLN
        </div>
      </div>
    </template>
  </dialogform>
</template>
<script>
  import newDialog from '@/bills/list/new_dialog'

  export default {
    props: [ 'bill_uid' ],
    extends: newDialog,
    methods: {
      onSubmit (form) {
        form.submit(
          () => this.resource.update({bill_uid: this.bill_uid}, form.toData()),
          (response) => {
            this.$refs.dialog.hide()
            this.$emit('success')
          }
        )
      },
      fetchContent () {
        return this.resource.get({bill_uid: this.bill_uid})
      },
      onAfterFetchContent () {
        this.ensureEmptyItemAtEnd()
        this.countSum()
      }
    }
  }
</script>
