import { createLocalVue, mount } from '@vue/test-utils'
import InfoPicture from '../../src/components/InfoPicture.vue'
import store from '@/store'

describe('InfoPicture testing', () => {
  const vueInstance = createLocalVue()
  const wrapper = mount(InfoPicture, {
    vueInstance,
    store
  })
  it('initialized correctly', () => {
    expect(wrapper).toBeTruthy()
    expect(wrapper.is(InfoPicture)).toBe(true)
  })
  it('setNewFile correct', () => {
    const spy = jest.spyOn(wrapper.vm, 'setNewFile')
    wrapper.vm.setNewFile()
    expect(spy).toHaveBeenCalled()
  })
})
