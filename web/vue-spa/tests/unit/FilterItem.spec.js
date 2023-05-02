/* eslint-disable */
import { createLocalVue, mount, shallowMount } from '@vue/test-utils'
import FilterItem from '../../src/components/FilterItem.vue'
import flushPromises from 'flush-promises'
import axios from 'axios'
import Vuex from 'vuex'
import store from '@/store'

const localVue = createLocalVue()
localVue.use(Vuex)

jest.mock('axios')

const mockData = [
  {success: true}
]
const file = {
  name: 'image.jpg',
  size: 50000,
  type: 'image/jpg'
}
const mockDataPost = [
  {h: 40, w: 40}
]
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
jest.spyOn(axios, "get").mockImplementation(() => Promise.resolve(responseGet))

describe('FilterItem testing', () => {
  const vueInstance = createLocalVue()
  const wrapper = shallowMount(FilterItem, {
    vueInstance,
    propsData: {
      previewImage: 'candy.jpg',
    }
  })
  it('initialized correctly', () => {
    expect(wrapper).toBeTruthy()
    expect(wrapper.is(FilterItem)).toBe(true)
  })
})

describe('FilterItem testing', () => {
  let wrapper
  wrapper = mount(FilterItem, {
    localVue,
    propsData: {
      previewImage: 'candy.jpg',
    },
    store
  })
  it('Click is calling method "onClickFilter"', async () => {
    jest.spyOn(wrapper.vm, 'onClickFilter')
    await wrapper.find('.filter').trigger('click');
    expect(wrapper.vm.onClickFilter).toHaveBeenCalled();
    expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/ping')
  })

  it('"onClickFilter" is calling "sendFilter"', async () => {
    jest.spyOn(wrapper.vm, 'sendFilter')
    // axios.post.mockImplementationOnce(() => Promise.resolve(responseGetId))
    axios.get.mockImplementationOnce(() => Promise.resolve(responseGet))
    await wrapper.get('.filter').trigger('click');
    expect(wrapper.vm.sendFilter).toHaveBeenCalled()
    expect(axios.get).toHaveBeenCalled()
    expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/ping')
  })
})

describe('FilterItem testing vuex', () => {
  let actions
  let store
  let wrapper
  actions = {
    changeLoading: jest.fn(),
    actionInput: jest.fn()
  }
  store = new Vuex.Store({
    actions
  })
  wrapper = mount(FilterItem, {
    localVue,
    store,
    propsData: {
      previewImage: 'candy.jpg',
    }
  })
})

describe('FilterItem testing axios', () => {
  const wrapper = mount(FilterItem, {
    localVue,
    store,
    propsData: {
      previewImage: 'candy.jpg',
    }
  })
  it('Testing axios post"', async () => {
    const filter = 'kek'
    const formData = new FormData()
    formData.append('filter_name', filter)
    formData.append('image', file)
    jest.spyOn(wrapper.vm, 'sendFilter')
    axios.post.mockImplementationOnce(() => Promise.resolve(responseGetId))
    wrapper.vm.sendFilter();
    expect(axios.post).toHaveBeenCalled()
    expect(axios.post).toHaveBeenCalledWith('http://localhost:5000/', expect.any(FormData))
  })
  it('Testing axios get"', () => {
    jest.spyOn(wrapper.vm, 'sendFilter')
    axios.post.mockImplementationOnce(() => Promise.resolve(responseGetId))
    expect(axios.post).toHaveBeenCalled()
    axios.get.mockResolvedValue(file)
    wrapper.vm.sendFilter();
    expect(axios.get).toHaveBeenCalled()
  })
})
