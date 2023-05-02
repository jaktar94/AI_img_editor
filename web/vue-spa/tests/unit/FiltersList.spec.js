import { createLocalVue, mount } from '@vue/test-utils'
import FiltersList from '../../src/components/FiltersList.vue'

describe('FiltersList testing', () => {
  const vueInstance = createLocalVue()
  const wrapper = mount(FiltersList, {
    vueInstance
  })
  it('initialized correctly', () => {
    expect(wrapper).toBeTruthy()
    expect(wrapper.is(FiltersList)).toBe(true)
  })
  it('onChangeModal is called correctly', () => {
    const spy = jest.spyOn(wrapper.vm, 'onChangeModal')
    wrapper.vm.onChangeModal(true, 'errorText', 'error')
    expect(wrapper.emitted().onChangeModal).toBeTruthy()
    expect(spy).toHaveBeenCalled()
  })
})
