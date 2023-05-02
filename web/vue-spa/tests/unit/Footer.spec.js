/* eslint-disable */
import { createLocalVue, mount, shallowMount } from '@vue/test-utils'
import Footer from '../../src/components/Footer.vue'
import axios from 'axios'
import store from '@/store'

const event = {
  target: {
    files: [
      {
        name: 'image.jpg',
        size: 50000,
        type: 'image/jpg'
      }
    ]
  }
}

const file = {
  name: 'image.jpg',
  size: 50000,
  type: 'image/jpg'
}

const mockData = [
  { success: true }
]
const mockDataPost = [
  { h: 40, w: 40 }
]

jest.mock('axios', () => ({
  get: jest.fn(() => mockData),
  post: jest.fn(() => mockDataPost)
}))

const responseGetSize = {
  data:
  {
    h: 60,
    w: 60
  }
}
const responseGetSizeIncorrect = {
  data:
  {
    h: 10,
    w: 10
  }
}
const responseGet = {
  data:
  {
    success: true
  }
}

describe('Footer.vue testing', () => {
  const vueInstance = createLocalVue();
  const wrapper = shallowMount(Footer, {
    vueInstance,
    store
  })
  it('initialized correctly', () => {
    expect(wrapper).toBeTruthy()
    expect(wrapper.is(Footer)).toBe(true)
  })
  it('limitations - correct resolution', () => {
    wrapper.setData({ isUploaded: false })
    jest.spyOn(wrapper.vm, 'checkLimitations')
    wrapper.vm.checkLimitations(responseGetSize, event)
    expect(wrapper.vm.isUploaded).toBe(true)
  })
  it('limitations - incorrect resolution', () => {
    wrapper.setData({ isUploaded: false })
    jest.spyOn(wrapper.vm, 'checkLimitations')
    wrapper.vm.checkLimitations(responseGetSizeIncorrect, event)
    expect(wrapper.vm.isUploaded).toBe(false)
    expect(wrapper.emitted().onChangeModal).toBeTruthy()
  })
})

describe('Testing handlefileupload', () => {
  const wrapper = mount(Footer)
  const responseGet = {
    data:
    {
      success: true
    }
  }
  const responseGetSize = {
    data:
    {
      h: 40,
      w: 40
    }
  }
  it('Testing filereader', () => {
    const fileReaderSpy = jest.spyOn(FileReader.prototype, 'readAsDataURL').mockImplementation(() => null)
    axios.get.mockResolvedValue(responseGet)
    wrapper.vm.handleFileUpload(event)
    expect(fileReaderSpy).toHaveBeenCalledWith(event.target.files[0])
  })
  it('Testing axios get', async () => {
    jest.spyOn(wrapper.vm, 'handleFileUpload')
    axios.get.mockResolvedValue(responseGet)
    expect(axios.get).toHaveBeenCalled()
    expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/ping')
  })
  it('Testing axios post', async () => {
    const formData = new FormData()
    formData.append('image', file)
    jest.spyOn(wrapper.vm, 'handleFileUpload')
    axios.post.mockImplementationOnce(() => Promise.resolve(responseGetSize))
    expect(axios.post).toHaveBeenCalled()
    expect(axios.post).toHaveBeenCalledWith('http://localhost:5000/get_size', formData)
  })
})

describe('Testing buttons', () => {
  let wrapper
  beforeEach(() => {
    const localVue = createLocalVue()
    wrapper = mount(Footer, {
      localVue,
      store,
      propsData: {
        isImageUploaded: true
      }
    })
  })
  it('Click classic button is changing type of filters', async () => {
    jest.spyOn(wrapper.vm, 'onClickBtnClassic')
    await wrapper.find('button.classic-btn').trigger('click');
    expect(wrapper.vm.onClickBtnClassic).toHaveBeenCalled();
  })
  it('Click neural button is changing type of filters', async () => {
    jest.spyOn(wrapper.vm, 'onClickBtnNeural')
    await wrapper.find('button.neural-btn').trigger('click');
    expect(wrapper.vm.onClickBtnNeural).toHaveBeenCalled();
  })
})
