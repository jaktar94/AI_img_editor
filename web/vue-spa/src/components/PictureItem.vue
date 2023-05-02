<template>
  <div class="picture-item" ref='picture'>
    <img  height="450px" :src= 'URL_CUR_FILE' alt="picture">
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default ({
  name: 'PictureItem',
  data: () => ({
    imageURL: '',
    file: ''
  }),
  computed: {
    ...mapGetters(['INIT_FILE', 'URL_INIT_FILE', 'URL_CUR_FILE'])
  },
  methods: {
  },
  created () {
    this.imageURL = this.$store.getters.URL_INIT_FILE
  }

})
</script>

<style scoped>
  .picture-item{
    margin: auto;
    padding-top: 20px;
    width: 1000px;
  }
</style>
