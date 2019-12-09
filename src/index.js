import Vue from 'vue';
import Buefy from "buefy";
import App from './App';

Vue.use(Buefy);
Vue.config.productionTip = false;

new Vue({
  el: '#app',
  render: h => h(App),
});