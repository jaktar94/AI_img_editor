<template>
  <div class="text-wrapper">
    <div class="effect-text">Эффект: {{ CUR_EFFECT }}</div>
    <div class="effect-preloader"><img src="../assets/Spinner.gif" alt="spin" :class="classObjLoader"></div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default ({
  name: 'EffectText',
  computed: {
    ...mapGetters(['CUR_EFFECT', 'IS_LOADING']),
    classObjLoader () {
      return {
        'loader-disabled': this.IS_LOADING === false
      }
    }
  }
})
</script>

<style scoped>
  .effect-text{
    display: inline-block;
    font-size: 20px;
    background-color: rgba(0, 0, 0, 0.329);
    max-width: 50%;
    margin: auto;
    padding: 5px 20px;
    border-radius: 20px;
    margin-top: 10px;
  }
  .loader-disabled {
    display: none;
  }
  .effect-preloader {
    display: inline-block;
    vertical-align: middle;
  }
</style>
