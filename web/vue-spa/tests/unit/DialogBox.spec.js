/* eslint-disable */
import { createLocalVue, mount } from '@vue/test-utils'
import DialogBox from '../../src/components/DialogBox.vue'

describe('DialogBox instance testing', () => {
  const vueInstance = createLocalVue()
  const wrapper = mount(DialogBox, {
    vueInstance
  })
  it('initialized correctly', () => {
    expect(wrapper).toBeTruthy()
    expect(wrapper.is(DialogBox)).toBe(true)
  })
})

describe('DialogBox buttons are correct', () => {
  let wrapper
  beforeEach(() => {
    const localVue = createLocalVue()
    wrapper = mount(DialogBox, {
      localVue
    })
  })
  it('Click is calling method "cancel"', async () => {
    jest.spyOn(wrapper.vm, 'cancel')
    await wrapper.find('button.no').trigger('click');
    expect(wrapper.vm.cancel).toHaveBeenCalled();
  })
  it('Click is calling method "submit"', async () => {
    jest.spyOn(wrapper.vm, 'submit')
    await wrapper.find('button.yes').trigger('click');
    expect(wrapper.vm.submit).toHaveBeenCalled();
  })
  it('Clicks were emitted', async () => {
    wrapper.vm.$emit('submit')
    wrapper.vm.$emit('submit', 'accept')
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted().submit[1]).toEqual(['accept'])
  })
  it('emits return "close" if button is clicked', () => {
    const cmp = wrapper.findComponent('.no')
    expect(cmp.getComponent('.no').exists()).toBe(true);
    wrapper.vm.$emit('cancel', 'close')
    expect(wrapper.emitted()['cancel'][0]).toEqual(['close'])
  })
  it('emits return "accept" if button is clicked', () => {
    const cmp = wrapper.findComponent('.yes')
    expect(cmp.getComponent('.yes').exists()).toBe(true);
    wrapper.vm.$emit('submit', 'accept')
    expect(wrapper.emitted()['submit'][0]).toEqual(['accept'])
  })
})
