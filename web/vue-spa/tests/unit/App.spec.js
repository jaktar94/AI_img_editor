/* eslint-disable */
import { createLocalVue, shallowMount } from '@vue/test-utils'
import App from '../../src/App.vue'
import store from '@/store'
import Vuex from 'vuex'
import axios from 'axios'

const mockData = [{ success: true }]

const file = {
  name: 'image.jpg',
  size: 50000,
  type: 'image/jpg'
}

const responseGet = {
  data:
  {
    success: true
  }
}
const responseGetFile = {
  data:
  {
    image: file
  }
}
const responseGetId = {
  data:
  {
    id: 5
  }
}
jest.mock('axios', () => ({
  get: jest.fn(() => mockData),
  post: jest.fn()
}))

jest.spyOn(axios, "get").mockImplementation(() => Promise.resolve({ data: file }))

describe('App testing', () => {
  const vueInstance = createLocalVue()
  const wrapper = shallowMount(App, {
    vueInstance,
  })

  it('initialized correctly', async () => {
    expect(wrapper).toBeTruthy()
    expect(wrapper.is(App)).toBe(true)
  })

  it('onChangeStatusInUpload', () => {
    wrapper.vm.onChangeStatusInUpload(true)
    expect(wrapper.vm.statusUpload).toBe(true)
    wrapper.vm.onChangeStatusInUpload(false)
    expect(wrapper.vm.statusUpload).toBe(false)
  })
  it('onChangeServerStatus', () => {
    wrapper.vm.onChangeServerStatus(true)
    expect(wrapper.vm.isServerOn).toBe(true)
    wrapper.vm.onChangeServerStatus(false)
    expect(wrapper.vm.isServerOn).toBe(false)
  })
  it('onChangeModal', () => {
    wrapper.vm.onChangeModal(true, 'errorText', 'acceptError')
    expect(wrapper.vm.isModalVisible).toBe(true)
    expect(wrapper.vm.modalMessage).toMatch('errorText')
    expect(wrapper.vm.userAction).toMatch('acceptError')
  })
  it('isModalVisible = false', () => {
    wrapper.vm.showModal()
    expect(wrapper.vm.isModalVisible).toBe(true)
    wrapper.vm.closeModal()
    expect(wrapper.vm.isModalVisible).toBe(false)
  })
})

describe('App testing axios', () => {
  const vueInstance = createLocalVue()
  const wrapper = shallowMount(App, {
    vueInstance,
    store
  })
  it('Testing isServerAnswer', async () => {
    jest.spyOn(wrapper.vm, 'isServerAnswer')
    axios.get.mockResolvedValue(responseGet)
    wrapper.vm.isServerAnswer()
    expect(axios.get).toHaveBeenCalled()
    expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/ping')
  })
  it('Testing resetBackendStore', async () => {
    jest.spyOn(wrapper.vm, 'resetBackendStore')
    axios.get.mockImplementationOnce(() => Promise.resolve(responseGet))
    wrapper.vm.resetBackendStore()
    expect(axios.get).toHaveBeenCalled()
    expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/reset')
  })
  it('Testing get_last_saved', async () => {
    jest.spyOn(wrapper.vm, 'acceptAction')
    axios.get.mockImplementationOnce(() => Promise.resolve(responseGetId))
    await wrapper.vm.acceptAction();
    expect(axios.get).toHaveBeenCalled()
  })
  it('Testing saveImage"', () => {
    jest.spyOn(wrapper.vm, 'saveImage')
    axios.post.mockImplementationOnce(() => Promise.resolve(responseGet))
    wrapper.vm.saveImage();
    expect(axios.post).toHaveBeenCalled()
    expect(axios.post).toHaveBeenCalledWith('http://localhost:5000/save_image', expect.any(FormData))
  })
})

describe('App testing acceptAction', () => {
  const vueInstance = createLocalVue()
  const wrapper = shallowMount(App, {
    vueInstance,
    store
  })

  it('Testing acceptAction type=accept', async () => {
    jest.spyOn(wrapper.vm, 'acceptAction')
    axios.get.mockImplementationOnce(() => Promise.resolve(responseGetFile))
    await wrapper.vm.acceptAction();
    expect(axios.get).toHaveBeenCalled()
  })
  it('Testing acceptAction type=help', async () => {
    const spy = jest.spyOn(wrapper.vm, 'closeModal')
    wrapper.setData({ userAction: 'help' })
    wrapper.vm.acceptAction()
    expect(spy).toHaveBeenCalled()
  })
  it('Testing acceptAction type=reset', async () => {
    const spy = jest.spyOn(wrapper.vm, 'closeModal')
    wrapper.setData({ userAction: 'reset' })
    wrapper.vm.acceptAction()
    expect(spy).toHaveBeenCalled()
  })
  it('Testing acceptAction type=upload', async () => {
    const spy = jest.spyOn(wrapper.vm, 'closeModal')
    const spy_1 = jest.spyOn(wrapper.vm, 'resetBackendStore')
    wrapper.setData({ userAction: 'upload' })
    wrapper.vm.acceptAction()
    expect(spy).toHaveBeenCalled()
    expect(spy_1).toHaveBeenCalled()
  })
  it('Testing acceptAction type=download', async () => {
    const ax = axios.get.mockImplementationOnce(() => Promise.resolve(responseGetId))
    wrapper.setData({ userAction: 'download' })
    wrapper.vm.acceptAction()
    expect(ax).toHaveBeenCalled()
  })
  it('Testing acceptAction type=delete', async () => {
    const spy = jest.spyOn(wrapper.vm, 'closeModal')
    wrapper.setData({ userAction: 'delete' })
    wrapper.vm.acceptAction()
    expect(spy).toHaveBeenCalled()
  })
})

