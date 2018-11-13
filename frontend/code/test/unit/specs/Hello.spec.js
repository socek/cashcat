import Login from '@/auth/login'
import { shallowMount } from '@vue/test-utils'

describe('Login', () => {
  it('should render correct contents', () => {
    const wrapper = shallowMount(Login, {})
    expect(wrapper.isAuthenticated()).toEqual(false)
  })
})
