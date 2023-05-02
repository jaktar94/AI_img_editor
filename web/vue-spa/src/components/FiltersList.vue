<template>
  <div class="filters">
    <div class="filters_list__classic filters_list" v-if="this.activeType == 'classic'">
      <FilterItem @onChangeModal ="onChangeModal" :activeType='activeType' nameFilter='Черно-белое' previewImage='greyscale.jpg'></FilterItem>
      <FilterItem @onChangeModal ="onChangeModal" :activeType='activeType' nameFilter='Сепия' previewImage='brown.jpg'></FilterItem>
      <FilterItem @onChangeModal ="onChangeModal" :activeType='activeType' nameFilter='Инвертирование' previewImage='invert.jpg'></FilterItem>
      <FilterItem @onChangeModal ="onChangeModal" :activeType='activeType' nameFilter='Рисунок' previewImage='handdraw.jpg'></FilterItem>
      <FilterItem @onChangeModal ="onChangeModal" :activeType='activeType' nameFilter='Рельеф' previewImage='emboss.jpg'></FilterItem>
    </div>
    <div class="filters_list__neural filters_list" v-else-if="this.activeType == 'neural'">
      <FilterItem @onChangeModal ="onChangeModal" :activeType='activeType' nameFilter='Starry night' previewImage='candy.jpg'></FilterItem>
      <FilterItem @onChangeModal ="onChangeModal" :activeType='activeType' nameFilter='Feathers' previewImage='feathers.jpg'></FilterItem>
      <FilterItem @onChangeModal ="onChangeModal" :activeType='activeType' nameFilter='Mosaic' previewImage='mosaic.jpg'></FilterItem>
      <FilterItem @onChangeModal ="onChangeModal" :activeType='activeType' nameFilter='Candy' previewImage='starry_night.jpg'></FilterItem>
      <FilterItem @onChangeModal ="onChangeModal" :activeType='activeType' nameFilter='Wave' previewImage='wave.jpg'></FilterItem>
    </div>
  </div>
</template>

<script>
import FilterItem from '@/components/FilterItem'

export default {
  components: {
    FilterItem
  },
  data: () => ({
  }),
  props: ['activeType', 'nameFilter'],
  methods: {
    onChangeModal (status, msg, action) {
      this.$emit('onChangeModal', status, msg, action)
    }
  }
}
</script>

<style scoped>
  .filters_list{
  margin-left: 30px;
  display: flex;
  height: auto;
  gap: 20px;
}
</style>
