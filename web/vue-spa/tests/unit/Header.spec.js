/* eslint-disable */
import { createLocalVue, mount } from '@vue/test-utils'
import Header from '../../src/components/Header.vue'

describe('Header testing', () => {
  const vueInstance = createLocalVue()
  const wrapper = mount(Header, {
    vueInstance
  })
  it('initialized correctly', () => {
    expect(wrapper).toBeTruthy()
    expect(wrapper.is(Header)).toBe(true)
  })

  it('header is correct', () => {
    expect(wrapper.isVisible()).toBe(true)
    expect(wrapper.classes('header')).toBe(true)
    expect(wrapper.classes()).toContain('header')
    expect(wrapper.is(Header)).toBe(true)
    expect(wrapper.findAll('div').at(0).text()).toMatch('YourEditor')
  })
})
