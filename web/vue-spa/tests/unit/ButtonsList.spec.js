/* eslint-disable */
import { createLocalVue, mount, shallowMount } from '@vue/test-utils'
import ButtonsList from '../../src/components/ButtonsList.vue'
import store from '@/store'
import Vuex from 'vuex'
import axios from 'axios'

describe('ButtonsList testing', () => {
  const vueInstance = createLocalVue()
  const wrapper = shallowMount(ButtonsList, {
    vueInstance,
    store
  })
  it('initialized correctly', () => {
    expect(wrapper).toBeTruthy()
    expect(wrapper.is(ButtonsList)).toBe(true)
  })
})

describe('Clicking buttons is calling methods', () => {
  let wrapper
  beforeEach (() => {
    const localVue = createLocalVue()
    wrapper = mount(ButtonsList, {
      localVue, store
    })
  })
  it('Click is calling method "accept"', async () => {
    jest.spyOn(wrapper.vm, 'onClickAccept')
    await wrapper.find('.acpt-btn').trigger('click');
    expect(wrapper.vm.onClickAccept).toHaveBeenCalled();
  })
  it('Click is calling method "reset"', async () => {
    jest.spyOn(wrapper.vm, 'onClickReset')
    await wrapper.find('.rst-btn').trigger('click');
    expect(wrapper.vm.onClickReset).toHaveBeenCalled();
  })
  it('Click is calling method "upload"', async () => {
    jest.spyOn(wrapper.vm, 'onClickUpload')
    await wrapper.find('.upld-btn').trigger('click');
    expect(wrapper.vm.onClickUpload).toHaveBeenCalled();
  })
  it('Click is calling method "delete"', async () => {
    jest.spyOn(wrapper.vm, 'onClickDelete')
    await wrapper.find('.dlt-btn').trigger('click');
    expect(wrapper.vm.onClickDelete).toHaveBeenCalled();
  })
  it('Click is calling method "download"', async () => {
    jest.spyOn(wrapper.vm, 'onClickDownload')
    await wrapper.find('.dwld-btn').trigger('click');
    expect(wrapper.vm.onClickDownload).toHaveBeenCalled();
  })
  it('Click is calling method "help"', async () => {
    jest.spyOn(wrapper.vm, 'onClickHelp')
    await wrapper.find('.help-btn').trigger('click');
    expect(wrapper.vm.onClickHelp).toHaveBeenCalled();
  })
})
