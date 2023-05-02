import Vue from 'vue'
import App from './App.vue'
import store from './store'
import './plugins/elements'
import './plugins/axios'

Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
