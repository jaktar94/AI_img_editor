<template>
  <div id="app">
    <div>
      <header>
        <Header></Header>
      </header>
      <main>
        <ButtonsList  @onChangeModalStatus="onChangeModal" :statusUpload = statusUpload :isImgChanged = isImgChanged></ButtonsList>
        <InfoPicture v-if='statusUpload'></InfoPicture>
        <PictureItem v-if='statusUpload'></PictureItem>
        <EffectText v-if='statusUpload'></EffectText>
      </main>
      <footer>
        <Footer
          v-show="isServerOn"
          :isImageUploaded="statusUpload"
          :isImgChanged="isImgChanged"
          @onChangeStatus="onChangeStatusInUpload"
          @onChangeServerStatus="onChangeServerStatus"
          @onChangeModal="onChangeModal">
        </Footer>
      </footer>
    </div>
    <modal
      :userAction = userAction
      :msg = modalMessage
      v-show="isModalVisible"
      @close="closeModal"
      @accept="acceptAction"
    />
  </div>
</template>

<script>
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import PictureItem from '@/components/PictureItem'
import InfoPicture from './components/InfoPicture.vue'
import EffectText from './components/EffectText.vue'
import ButtonsList from './components/ButtonsList.vue'
import modal from './components/DialogBox.vue'
import { mapGetters, mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    Header,
    Footer,
    PictureItem,
    InfoPicture,
    EffectText,
    ButtonsList,
    modal
  },
  data: () => ({
    statusUpload: false,
    isImgChanged: false,
    isModalVisible: false,
    modalMessage: '',
    userAction: '',
    isServerOn: false
  }),
  methods: {
    ...mapActions(['changeURLCurFile', 'changeEffect', 'changeCurFile', 'changeActiveFilter', 'changeCurrentFilter']),
    onChangeStatusInUpload (status) {
      this.statusUpload = status
    },
    onChangeServerStatus (status) {
      this.isServerOn = status
    },
    onChangeModal (status, msg, action) {
      this.isModalVisible = status
      this.modalMessage = msg
      this.userAction = action
    },
    showModal () {
      this.isModalVisible = true
    },
    closeModal () {
      this.isModalVisible = false
    },
    acceptAction () {
      if (this.userAction === 'accept') {
        const id = this.CUR_FILE_ID
        axios({
          method: 'get',
          url: `http://localhost:8000/${id}.jpg`,
          responseType: 'blob'
        }).then(response => {
          // console.log(response)
          this.changeCurFile(response.data)
        })
          .catch(function (error) {
            // eslint-disable-next-line no-unused-vars
            const er = error
          })
        this.saveImage()
        // Если запрос с ошибкой

        this.closeModal()
        // this.changeActiveFilter(this.CUR_EFFECT)
        // this.changeEffect('отсутствует')
      }
      if (this.userAction === 'reset') {
        if (this.ACT_FILTER === 'отсутствует') {
          this.changeCurFile(this.INIT_FILE)
          this.changeURLCurFile(this.URL_INIT_FILE)
          this.changeEffect('отсутствует')
          // this.changeCurrentFilter('отсутствует')
        } else {
          axios.get('http://localhost:5000/get_last_saved')
          // Если запрос успешен
            .then(response => {
              const id = response.data.id
              axios({
                method: 'get',
                url: `http://localhost:8000/${id}.jpg`,
                responseType: 'blob'
              }).then(response => {
                // console.log(response)
                this.changeCurFile(response.data)
                const reader = new FileReader()
                reader.addEventListener('load', function () {
                  this.imageSrc = reader.result
                  this.changeURLCurFile(reader.result)
                }.bind(this), false)
                if (response.data) {
                  reader.readAsDataURL(response.data)
                }
                this.changeEffect(this.ACT_FILTER)
                // this.changeCurrentFilter('отсутствует')
              })
            })
          // Если запрос с ошибкой
            .catch(error => {
              const errorText = 'Произошла ошибка: сервер недоступен. Попробуйте перезагрузить страницу'
              this.onChangeModal(true, errorText, 'uploadPage')
              this.isServerOn = false
              console.log(error)
            })
        }
        this.changeCurrentFilter('отсутствует')
        this.closeModal()
        // this.isImgChanged = true
      }
      if (this.userAction === 'upload') {
        this.onChangeStatusInUpload(false)
        this.changeEffect('отсутствует')
        this.changeActiveFilter('отсутствует')
        this.closeModal()
        this.resetBackendStore()
      }
      if (this.userAction === 'download') {
        this.closeModal()
        if (this.ACT_FILTER === 'отсутствует' && this.CUR_EFFECT === 'отсутствует') {
          const link = document.createElement('a')
          link.href = this.URL_INIT_FILE
          // link.download = this.$store.getters.CUR_FILE.name
          link.download = 'file.jpg'
          link._target = 'blank'
          link.click()
        } else if ((this.CUR_EFFECT !== this.ACT_FILTER) || (this.ACT_FILTER === this.CUR_FILTER)) {
          const mesText = 'На данный момент у вас есть несохраненные изменения. Для загрузки изображения сохраните текущий фильтр и вновь нажмите кнопку "Скачать"'
          this.onChangeModal(true, mesText, 'downloadUnsaved')
        } else {
          axios.get('http://localhost:5000/get_last_saved')
          // Если запрос успешен
            .then(response => {
              const id = response.data.id
              axios({
                method: 'get',
                url: `http://localhost:8000/${id}.jpg`,
                responseType: 'blob'
              }).then(response => {
                // console.log(response)
                // this.changeCurFile(response.data)
                const reader = new FileReader()
                reader.addEventListener('load', function () {
                  this.imageSrc = reader.result
                  const urlSavedFile = reader.result
                  // console.log(urlSavedFile)
                  const link = document.createElement('a')
                  link.href = urlSavedFile
                  // link.download = this.$store.getters.CUR_FILE.name
                  link.download = 'file.jpg'
                  link._target = 'blank'
                  link.click()
                  // this.changeURLCurFile(reader.result)
                }.bind(this), false)
                if (response.data) {
                  reader.readAsDataURL(response.data)
                }
              })
                .catch(error => {
                  const errorText = 'Произошла ошибка: сервер недоступен. Попробуйте перезагрузить страницу'
                  this.onChangeModal(true, errorText, 'uploadPage')
                  this.isServerOn = false
                  console.log(error)
                })
            })
          // Если запрос с ошибкой
            .catch(error => {
              const errorText = 'Произошла ошибка: сервер недоступен. Попробуйте перезагрузить страницу'
              this.onChangeModal(true, errorText, 'uploadPage')
              this.isServerOn = false
              console.log(error)
            })
          this.closeModal()
        }

      }
      if (this.userAction === 'delete') {
        this.changeURLCurFile(this.$store.getters.URL_INIT_FILE)
        this.changeCurFile(this.$store.getters.INIT_FILE)
        this.changeEffect('отсутствует')
        this.changeActiveFilter('отсутствует')
        this.closeModal()
        this.resetBackendStore()
      }
      if (this.userAction === 'help') {
        this.closeModal()
      }
    },
    saveImage () {
      const formData = new FormData()
      formData.append('saved_image_id', this.CUR_FILE_ID)
      axios.post('http://localhost:5000/save_image', formData)
        // Если запрос успешен
        .then(response => {
          // console.log(response.data, 'Фото сохранено')
          this.closeModal()
          if (response.data.success === false) {
            throw new Error('Произошла ошибка: не удалось сохранить файл. Попробуйте снова')
          }
          this.isImgChanged = true
          this.changeActiveFilter(this.CUR_EFFECT)
        }).catch(error => {
          const errorText = 'Произошла ошибка: не удалось сохранить файл. Попробуйте снова'
          this.onChangeModal(true, errorText, 'acceptError')
          console.log(error)
        })
    },
    isServerAnswer () {
      axios.get('http://localhost:5000/ping')
      // Если запрос успешен
        .then(response => {
          this.isServerOn = true
          // console.log('Сервер готов к работе ', response.data)
        })
      // Если запрос с ошибкой
        .catch(error => {
          const errorText = 'Произошла ошибка: сервер недоступен. Попробуйте перезагрузить страницу'
          this.onChangeModal(true, errorText, 'uploadPage')
          this.isServerOn = false
          console.log(error)
        })
    },
    resetBackendStore () {
      axios.get('http://localhost:5000/reset')
        // Если запрос успешен
        .then(response => {
          // console.log(response.data)
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  computed: {
    ...mapGetters(['MODAL_STATUS', 'URL_CUR_FILE', 'CUR_FILE', 'CUR_EFFECT', 'CUR_FILE_ID', 'INIT_FILE', 'URL_INIT_FILE', 'ACT_FILTER', 'CUR_FILTER'])
  },
  created () {
    this.isServerAnswer()
    this.resetBackendStore()
  }
  // updated () {
  //   this.isServerAnswer()
  // }
}
</script>

<style scoped>
#app {
  font-family: Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #ffffff;
  margin-top: 60px;
  width: 1240px;
  margin: auto;
  overflow:hidden;
}
main {
  background-color: rgba(54, 51, 51, 0.81);
  height: 600px;
  padding:0px;
  border:0px solid grey;
}
footer{
  background-color: #4D4E53;
  height: 150px;
}

</style>
