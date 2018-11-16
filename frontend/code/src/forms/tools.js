export function toFormField (value) {
  return {
    value: value,
    errors: [],
    default: value
  }
}

export function toFormObject (obj) {
  obj._schema = []
  for (let index in obj) {
    let value = obj[index]
    if (index.startsWith('_')) {
      // do nothing. "_" prefixed names are special fields
    } else if (typeof (value) === 'object') {
      obj[index] = toFormObject(value)
    } else {
      obj[index] = toFormField(value)
    }
  }
  return obj
}

export function resetFields (field) {
  for (let index in field) {
    let value = field[index]
    if (value.default !== undefined) {
      field[index].value = value.default
    } else {
      field[index] = resetFields(value)
    }
  }
  return field
}

export function resetForm (form) {
  form = resetErrors(form)
  return resetFields(form)
}

export function toFieldsList (form) {
  let fields = []
  for (let item of form) {
    fields.push(toFields(item))
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

export function toFields (form) {
  let fields = {}
  for (let index in form) {
    let value = form[index]
    if (index.startsWith('_')) {
      // do nothing
    } else if (value.value !== undefined) {
      fields[index] = value.value
    } else if (Array.isArray(value)) {
      fields[index] = toFieldsList(value)
    } else {
      fields[index] = toFields(value)
    }
  }
  return fields
}

export function resetErrors (field) {
  for (let index in field) {
    let value = field[index]
    if (index === 'errors') {
      field[index] = []
    } else if (value.default !== undefined) {
      field[index].errors = []
    } else {
      field[index] = resetErrors(value)
    }
  }
  return field
}

export function setErrors (form, errors) {
  for (let index in errors) {
    if (index.startsWith('_')) {
      form._schema = errors[index]
    } else if (typeof (errors[index][0]) === 'string') {
      form[index].errors = errors[index]
    } else {
      form[index] = setErrors(form[index], errors[index])
    }
  }
  return form
}

export function parseErrorResponse (form, response) {
  if (response.status === 400) {
    return setErrors(resetErrors(form), response.body)
  }
}

export function setFormDefaults (form, defaults) {
  for (let index in defaults) {
    let value = defaults[index]
    if (Array.isArray(value)) {
      form[index] = setFormDefaultsForList(value)
    } else if (typeof (value) === 'object') {
      form[index] = setFormDefaults(form[index], value)
    } else if (form[index] === undefined) {
      // Ignore missing fields
    } else {
      form[index].default = value
    }
  }
  return form
}

export function setDefaults (form, defaults) {
  form = setFormDefaults(form, defaults)
  return resetFields(form)
}

export function setFormDefaultsForList (defaults) {
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
