<template>
  <dialogform
    title="Zmień rachunek"
    size="lg"
    :fetchContent="fetchContent"

    ref="form"
    v-model="form"
    @success="$emit('success')"
    @submit="onSubmit"
    @afterReset="onAfterReset"
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
    data () {
      return {
        fetchedData: {},
        removedItems: []
      }
    },
    methods: {
      fetchContent () {
        return this.resource.get({bill_uid: this.bill_uid})
      },
      onAfterFetchContent (data) {
        this.ensureEmptyItemAtEnd()
        this.countSum()
        this.fetchedData = data
      },
      onSubmit (form) {
        let diff = this.diff(this.fetchedData, form)
        if (diff.length === 0) {
          this.$refs.form.hideModal()
        } else {
          this.resource.update({bill_uid: this.bill_uid}, diff).then((response) => {
            this.$refs.form.onSuccess()
          }).catch(this.$refs.form.parseErrorResponse)
        }
      },
      diffList (oldForm, newForm, path) {
        let diff = []
        let uids = []
        let newFormByUid = {}
        for (let index in newForm) {
          let item = newForm[index]
          if (item.uid) {
            uids.push(item.uid)
            newFormByUid[item.uid] = item
          } else {
            diff.push({
              op: 'add',
              path: path + index,
              value: item
            })
          }
        }
        for (let item of oldForm) {
          if (!uids.includes(item.uid)) {
            diff.push({
              op: 'remove',
              path: path,
              value: item.uid
            })
          } else {
            let subPath = path + item.uid + '/'
            diff = diff.concat(this.diff(item, newFormByUid[item.uid], subPath))
          }
        }
        return diff
      },
      diff (oldForm, newForm, path) {
        let diff = []
        path = path || '/'
        for (let key in newForm) {
          let oldValue = oldForm[key]
          let newValue = newForm[key]
          if (Array.isArray(oldValue)) {
            let subPath = path + key + '/'
            diff = diff.concat(this.diffList(oldValue, newValue, subPath))
          } else if (oldValue !== newValue) {
            diff.push({
              op: 'replace',
              path: path + key,
              value: newValue
            })
          }
        }
        return diff
      }
    }
  }
</script>
