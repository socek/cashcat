function isFunction (functionToCheck) {
  return functionToCheck && {}.toString.call(functionToCheck) === '[object Function]'
}

export function convertToForm (obj) {
  let toField = function (value) {
    return {
      value: value,
      errors: [],
      default: value
    }
  }

  let toObject = function (obj) {
    obj._schema = []
    for (let index in obj) {
      let value = obj[index]
      if (index.startsWith('_')) {
        // do nothing. "_" prefixed names are special fields
      } else if (typeof (value) === 'object') {
        obj[index] = toObject(value)
      } else {
        obj[index] = toField(value)
      }
    }
    return obj
  }

  obj = toObject(obj)

  obj.toData = function () {
    // Convert Form object into a key -> value structure.
    let toList = function (form) {
      let fields = []
      for (let item of form) {
        fields.push(toValue(item))
      }
      let lastItemIndex = fields.length - 1
      let lastItem = fields[lastItemIndex]
      let isEmpty = true
      for (let item in lastItem) {
        if (lastItem[item]) {
          isEmpty = false
          break
        }
      }
      if (isEmpty) {
        fields.pop(lastItemIndex)
      }
      return fields
    }

    let toValue = function (form) {
      let fields = {}
      for (let index in form) {
        let value = form[index]
        if (index.startsWith('_') || isFunction(value)) {
          // do nothing
        } else if (value.value !== undefined) {
          fields[index] = value.value
        } else if (Array.isArray(value)) {
          fields[index] = toList(value)
        } else {
          fields[index] = toValue(value)
        }
      }
      return fields
    }

    return toValue(this)
  }

  obj._resetErrors = function (field) {
    // Remove error state from all fields
    for (let index in field) {
      let value = field[index]
      if (index === 'errors') {
        field[index] = []
      } else if (value.default !== undefined) {
        field[index].errors = []
      } else {
        field[index] = this._resetErrors(value)
      }
    }
    return field
  }

  obj._resetFields = function (field) {
    // Set fields to default values
    for (let index in field) {
      let value = field[index]
      if (value.default !== undefined) {
        field[index].value = value.default
      } else {
        field[index] = this._resetFields(value)
      }
    }
    return field
  }

  obj.reset = function () {
    // Reset fields to default values and remove error states
    this._resetErrors(this)
    this._resetFields(this)
  }

  obj._setErrors = function (form, errors) {
    // Set error states and messages
    for (let index in errors) {
      if (index.startsWith('_')) {
        form._schema = errors[index]
      } else if (typeof (errors[index][0]) === 'string') {
        form[index].errors = errors[index]
      } else {
        form[index] = this._setErrors(form[index], errors[index])
      }
    }
    return form
  }

  obj.setErrors = function (errors) {
    this._resetErrors(this)
    this._setErrors(this, errors)
  }

  obj.setDefaults = function (defaults) {
    // Set default values for form, and reset that from
    this._setDefaults(this, defaults)
    this._resetFields(this)
  }

  obj._setDefaults = function (form, defaults) {
    // Set default values for form object fields.
    for (let index in defaults) {
      let value = defaults[index]
      if (Array.isArray(value)) {
        form[index] = this._setDefaultsForList(value)
      } else if (typeof (value) === 'object') {
        form[index] = this._setDefaults(form[index], value)
      } else if (form[index] === undefined) {
        // Ignore missing fields
      } else {
        form[index].default = value
      }
    }
    return form
  }

  obj._setDefaultsForList = function (defaults) {
    let form = []
    for (let index in defaults) {
      let value = defaults[index]
      let item = {
        _index: form.length
      }
      for (let key in value) {
        item[key] = {
          value: value[key],
          errors: [],
          default: value[key]
        }
      }
      form.push(item)
    }
    return form
  }

  obj._parseErrorResponse = function (response) {
    if (response.status === 400) {
      this.setErrors(response.body)
    } else {
      console.log('something bad has happened', response)
    }
  }

  obj.submit = function (query, success) {
    query().then(success).catch(this._parseErrorResponse.bind(this))
  }

  return obj
}
