<template>
  <header class="header">
    <div class="header__brand">
      {{ header }}
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: {
    msg: String
  },
  data: () => ({
    header: 'YourEditor'
  })
}
</script>

<style scoped>
  .header{
    height: 60px;
    background-color: #309860;
    color: white;
  }
  .header__brand{
    font-family: Roboto;
    font-style: normal;
    font-weight: 500;
    font-size: 27px;
    line-height: 32px;
    text-align: start;
    padding: 12px 30px;
    cursor: default;
  }
</style>
