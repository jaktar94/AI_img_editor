<template>
  <div class="footer" data-hook="footer">
    <div class="welcome-container" v-if="!isImageUploaded">
      <div class="welcome-container__text">
        Добро пожаловать!<br>
        Загрузите ваше первое изображение
      </div>
      <div class="filters-container__upload">
        <label class="input__file-button" for="input-file">
          <input type="file" class="input-file" id='btn-input' ref="upload" accept="image/jpeg"
            @change="handleFileUpload( $event )">
          <span class="input__file-button-text">Загрузить</span>
        </label>
      </div>
    </div>
    <div class="filters-container" v-if="isImageUploaded">
      <div class="filters__buttons">
        <button class="classic-btn btn"
          :class="{'active-btn':isActiveClassic}"
          @click='onClickBtnClassic()'>C</button>
        <button class="neural-btn btn"
          :class="{'active-btn':isActiveNeural}"
          @click='onClickBtnNeural()'>NN</button>
      </div>
      <div class="filters__list">
        <FiltersList @onChangeModal="onChangeModalStatus" :activeType='activeType'></FiltersList>
      </div>
    </div>

  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import FiltersList from '@/components/FiltersList'
import axios from 'axios'
export default ({
  name: 'Footer',
  components: {
    FiltersList
  },
  props: ['isImageUploaded', 'isServerOn', 'isImgChanged'],
  data: () => ({
    isUploaded: false,
    isActiveClassic: true,
    isActiveNeural: false,
    activeType: 'classic',
    file: '',
    imageSrc: ''
  }),
  methods: {
    ...mapActions(['changeURLInitFile', 'changeURLCurFile', 'changeResolutionWidth', 'changeResolutionHeight', 'changeInitFile', 'changeCurFile']),
    onClickBtnClassic () {
      this.isActiveClassic = true
      this.isActiveNeural = false
      this.activeType = 'classic'
    },
    onClickBtnNeural () {
      this.isActiveClassic = false
      this.isActiveNeural = true
      this.activeType = 'neural'
      if ((this.CUR_RESOLUTION_WIDTH >= 800 && this.CUR_RESOLUTION_HEIGHT >= 450) || (this.CUR_RESOLUTION_WIDTH >= 450 && this.CUR_RESOLUTION_HEIGHT >= 800)) {
        const messageText = 'Обратите внимание: фотография с разрешением ' + this.CUR_RESOLUTION_WIDTH + 'x' + this.CUR_RESOLUTION_HEIGHT + ' не поддерживает нейронные фильтры.' +
            'Для применения нейронных фильтров загрузите фотографию меньшего разрешения (не более 800х450)'
        this.$emit('onChangeModal', true, messageText, 'neuralPhoto')
        this.onClickBtnClassic()
      }
    },
    onChangeModalStatus (status, msg, action) {
      this.$emit('onChangeModal', status, msg, action)
    },
    onClickFileUpload () {
      const btn = document.querySelector('.input-file')
      btn.click()
    },
    handleFileUpload (event) {
      this.file = event.target.files[0]
      // eslint-disable-next-line prefer-const
      let reader = new FileReader()
      reader.addEventListener('load', function () {
        this.imageSrc = reader.result
        this.changeURLInitFile(reader.result)
        this.changeURLCurFile(reader.result)
      }.bind(this), false)
      if (this.file) {
        reader.readAsDataURL(this.file)
      }
      axios.get('http://localhost:5000/ping')
      // Если сервер работает
        .then(response => {
          const formData = new FormData()
          formData.append('image', this.file)
          axios.post('http://localhost:5000/get_size', formData)
          // Проверка разрешения картинки
            .then(response => {
              this.checkLimitations(response, event)
            })
          // Если запрос с ошибкой
            .catch(error => {
              // console.log(this.file)
              // eslint-disable-next-line no-unused-vars
              const er = error
            })
        })
      // Если запрос с ошибкой
        .catch(error => {
          const errorText = 'Произошла ошибка: сервер недоступен, загрузить инструменты редактирования невозможно. Попробуйте перезагрузить страницу и снова загрузить фотографию'
          this.$emit('onChangeModal', true, errorText, 'uploadPage')
          // this.onChangeModal(true, errorText, 'uploadPage')
          this.$emit('onChangeServerStatus', false)
          // this.isServerOn = false
          // eslint-disable-next-line no-unused-vars
          const er = error
        })
    },
    checkLimitations (response, event) {
      if (((response.data.w <= 1920 && response.data.h <= 1080) ||
                (response.data.w <= 1080 && response.data.h <= 1920)) &&
                (Math.max(response.data.w, response.data.h) / Math.min(response.data.w, response.data.h) <= 2) &&
                ((response.data.w >= 20 && response.data.h >= 20))) {
        this.isUploaded = true
        this.changeResolutionWidth(response.data.w)
        this.changeResolutionHeight(response.data.h)
        // console.log(this.$store.getters.CUR_RESOLUTION_WIDTH + ' ' + this.$store.getters.CUR_RESOLUTION_HEIGHT)
        // console.log(response)
        this.changeCurFile(event.target.files[0])
        this.changeInitFile(event.target.files[0])
        this.$emit('onChangeStatus', this.isUploaded)
        this.$emit('onChangeServerStatus', true)
        // console.log('Загружена картинка и инструменты редактирования ', response)
      } else {
        const errorText = 'Фотография с разрешением ' + response.data.w + 'x' + response.data.h + ' не поддерживается.' +
                  ' Загрузите другую фотографию в рамках ограничений: от 20x20 до 1920х1080 и соотношением сторон не более чем 2 к 1'
        this.$emit('onChangeModal', true, errorText, 'uploadPhoto')
        // this.$forceUpdate()
      }
    },
    sendPicture () {
      axios.post('/', this.file)
      // Если запрос успешен
        .then(function (response) {
          console.log(response)
        })
      // Если запрос с ошибкой
        .catch(function (error) {
          console.log(error)
        })
    }
  },
  computed: {
    ...mapGetters(['CUR_FILE', 'URL_CUR_FILE', 'CUR_RESOLUTION_WIDTH', 'CUR_RESOLUTION_HEIGHT'])
  },
  mounted () {
    this.isUploaded = this.isImageUploaded
  }
})
</script>

<style scoped>
.footer{
  height: 100%;
}
.welcome-container{
  display: flex;
  padding-top:50px;
  margin: 0px 250px;
  justify-content: space-between;
}
.welcome-container__text{
  text-align: left;
  color: white;
  font-size: 22px;
  line-height: 28px;
}
.upload-file{
  height: 100%;
}
.upld-btn{
  width: 200px;
  font-size: 24px;
  background:#309860;
  border: none;
  text-align: center;
}
.filters-container{
  height: 80%;
  padding-top: 15px;
  display: flex;
  width: 100%;
}
.filters__buttons{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 55px;
  height: auto;
  margin: 13px 10px;
  gap: 10px;
}
.btn{
  color: white;
  background: #3C3939;
  border: 0px solid #4ac885a9;
  border-radius: 7px;
  font-size: 20px;
  height: 55px;
  cursor: pointer;
}
.btn:hover{
  box-shadow: inset -2px -2px #4ac885a9, inset 2px 2px #4ac885a9;
}
.active-btn{
  background-color: #52da91bd;
  transform: scale(1.1);
  box-sizing: content-box;
}
.input-file{
  opacity: 0;
  height: 100%;
  position: absolute;
  cursor: pointer;
}
.input__file-button {
  position: relative;
  width: 110px;
  font-size: 24px;
  background-color: #309860;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 9px 49px;
  border-radius: 6px;
}
.input__file-button:hover {
  background:#4ac885a9;
}
</style>
