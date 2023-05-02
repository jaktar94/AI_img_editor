import { createLocalVue, mount } from '@vue/test-utils'
import EffectText from '../../src/components/EffectText.vue'
import store from '@/store'
import Vuex from 'vuex'

describe('EffectText testing', () => {
  const vueInstance = createLocalVue()
  const wrapper = mount(EffectText, {
    vueInstance,
    store
  })
  it('initialized correctly', () => {
    expect(wrapper).toBeTruthy()
    expect(wrapper.is(EffectText)).toBe(true)
  })
})

it('when photo is uploaded effect text is "отсутствует"', () => {
  const vueInstance = createLocalVue()
  vueInstance.use(Vuex)
  const wrapper = mount(EffectText, {
    vueInstance,
    store
  })
  expect(wrapper.vm.$options.name).toMatch('EffectText')
  expect(wrapper).toBeTruthy()
  expect(wrapper.is(EffectText)).toBe(true)
  expect(wrapper.findAll('div').at(1).text()).toMatch('Эффект: отсутствует')
})
