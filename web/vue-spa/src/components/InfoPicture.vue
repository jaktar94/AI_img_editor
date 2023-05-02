<template>
  <div class="info-picture">
    <div class="info-picture__name">
      {{ fileProperty }}
    </div>
    <div class="info-picture__resolution">
      {{ fileResolution }}
      <!-- {{ this.file }} -->
      <!-- {{ getImgSize() }} -->
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default ({
  name: 'InfoPicture',
  components: {
  },
  data: () => ({
    resolution: '',
    file: 'empty',
    isFileReceived: false
  }),
  methods: {
    setNewFile () {
      this.file = this.$store.getters.INIT_FILE
    }
  },
  computed: {
    ...mapGetters(['INIT_FILE', 'CUR_RESOLUTION_WIDTH', 'CUR_RESOLUTION_HEIGHT']),
    fileProperty () {
      return this.INIT_FILE.name
    },
    fileResolution () {
      return this.CUR_RESOLUTION_WIDTH + 'x' + this.CUR_RESOLUTION_HEIGHT
    }
  }
})

</script>

<style scoped>
  .info-picture{
    /* position: relative; */
    background-color: rgba(0, 0, 0, 0.329);
    display: flex;
    margin-left: 360px;
    width: 500px;
    justify-content: space-between;
    padding: 10px 15px;
    /* margin-top: 55px; */
    border-radius: 20px;
    /* top: 25px; */
  }
</style>
