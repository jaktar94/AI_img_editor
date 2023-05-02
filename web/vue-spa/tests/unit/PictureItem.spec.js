import { createLocalVue, mount } from '@vue/test-utils'
import PictureItem from '../../src/components/PictureItem.vue'
import store from '@/store'

describe('PictureItem testing', () => {
  const vueInstance = createLocalVue()
  const wrapper = mount(PictureItem, {
    vueInstance,
    store
  })
  it('initialized correctly', () => {
    expect(wrapper).toBeTruthy()
    expect(wrapper.is(PictureItem)).toBe(true)
  })
})
