import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios';
import VueAxios from 'vue-axios';
import VueCryptojs from 'vue-cryptojs'
 


Vue.config.productionTip = false
Vue.use(VueCryptojs)
Vue.use(VueAxios,axios);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
