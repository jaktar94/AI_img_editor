import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentEffect: 'отсутствует', // отображает текущий примененный фильтр к картинке, динамически отображается в поле "эффект"
    currentFilter: 'отсутствует', // фильтр, выбранный в текущей итерации, обнуляется каждый раз при применении очередного фильтра
    activeFilter: 'отсутствует', // последний сохраненный фильтр
    currentFile: '',
    initFile: '',
    imgUploadStatus: false,
    modalBoxStatus: false,
    urlInitFile: '',
    urlCurFile: '',
    resWidth: 0,
    resHeight: 0,
    curFileId: -1,
    isLoading: false

  },
  getters: {
    CUR_EFFECT: state => { return state.currentEffect },
    CUR_FILTER: state => { return state.currentFilter },
    CUR_FILE: state => { return state.currentFile },
    URL_CUR_FILE: state => { return state.urlCurFile },
    CUR_STATUS: state => { return state.imgUploadStatus },
    MODAL_STATUS: state => { return state.modalBoxStatus },
    INIT_FILE: state => { return state.initFile },
    URL_INIT_FILE: state => { return state.urlInitFile },
    CUR_RESOLUTION_WIDTH: state => { return state.resWidth },
    CUR_RESOLUTION_HEIGHT: state => { return state.resHeight },
    ACT_FILTER: state => { return state.activeFilter },
    CUR_FILE_ID: state => { return state.curFileId },
    IS_LOADING: state => { return state.isLoading }
  },
  mutations: {
    CHANGE_EFF (state, effect) {
      state.currentEffect = effect
    },
    CHANGE_CUR_FILE (state, file) {
      state.currentFile = file
    },
    CHANGE_STATUS (state, status) {
      state.imgUploadStatus = status
    },
    CHANGE_MODAL_STATUS (state, modalStatus) {
      state.modalBoxStatus = modalStatus
    },
    CHANGE_URL_INIT_FILE (state, url) {
      state.urlInitFile = url
    },
    CHANGE_URL_CUR_FILE (state, url) {
      state.urlCurFile = url
    },
    CHANGE_RES_WIDTH (state, width) {
      state.resWidth = width
    },
    CHANGE_RES_HEIGHT (state, height) {
      state.resHeight = height
    },
    CHANGE_ACT_FILTER (state, actFil) {
      state.activeFilter = actFil
      state.currentFilter = 'отсутствует'
    },
    CHANGE_CUR_FILTER (state, curFil) {
      state.currentFilter = curFil
    },
    CHANGE_INIT_FILE (state, file) {
      state.initFile = file
    },
    CHANGE_CUR_FILE_ID (state, id) {
      state.curFileId = id
    },
    CHANGE_LOAD (state, flag) {
      state.isLoading = flag
    }
  },
  actions: {
    changeEffect ({ commit }, effect) {
      const curEffect = effect
      commit('CHANGE_EFF', curEffect)
    },
    changeCurFile ({ commit }, file) {
      const curImg = file
      commit('CHANGE_CUR_FILE', curImg)
    },
    changeInitFile ({ commit }, file) {
      const initImg = file
      commit('CHANGE_INIT_FILE', initImg)
    },
    changeStatus ({ commit }, status) {
      const curStatus = status
      commit('CHANGE_STATUS', curStatus)
    },
    changeModalStatus ({ commit }, modalStatus) {
      const modStatus = modalStatus
      commit('CHANGE_MODAL_STATUS', modStatus)
    },
    changeURLInitFile ({ commit }, url) {
      const urlFile = url
      commit('CHANGE_URL_INIT_FILE', urlFile)
    },
    changeURLCurFile ({ commit }, url) {
      const urlFile = url
      commit('CHANGE_URL_CUR_FILE', urlFile)
    },
    changeResolutionWidth ({ commit }, width) {
      const resWidth = width
      commit('CHANGE_RES_WIDTH', resWidth)
    },
    changeResolutionHeight ({ commit }, height) {
      const resHeight = height
      commit('CHANGE_RES_HEIGHT', resHeight)
    },
    changeActiveFilter ({ commit }, act) {
      const actFil = act
      commit('CHANGE_ACT_FILTER', actFil)
    },
    changeCurrentFilter ({ commit }, cur) {
      const curFil = cur
      commit('CHANGE_CUR_FILTER', curFil)
    },
    changeCurFileId ({ commit }, id) {
      const idFil = id
      commit('CHANGE_CUR_FILE_ID', idFil)
    },
    changeLoading ({ commit }, flag) {
      const fl = flag
      commit('CHANGE_LOAD', fl)
    }
  },
  modules: {
  }
})
