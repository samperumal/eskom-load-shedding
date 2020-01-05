import Vue from 'vue';
import App from './App';

const moment = require("moment");

import Buefy from "buefy";
Vue.use(Buefy, {
  defaultDateFormatter: (date) => moment(date).format("ddd, DD MMMM YYYY"),
  defaultIconPack: 'fas',
});
Vue.config.productionTip = false;

new Vue({
  el: '#app',
  data() {
    return {
      
    }
  },
  render: function (h) { return h(App, { props: { currentStage: this.currentStage } }); },
  mounted: function () { 
  }
});