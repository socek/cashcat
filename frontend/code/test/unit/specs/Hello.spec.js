import Login from '@/auth/login'
import { shallowMount } from '@vue/test-utils'

console.log('0')
describe('Login', () => {
  console.log('a0')
  it('should render correct contents', () => {
    console.log('a')
    const wrapper = shallowMount(Login, {})
    console.log('b')
    expect(wrapper.isAuthenticated()).toEqual(false)
    console.log('c')
  })
})
