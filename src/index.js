import Vue from 'vue';
import Buefy from "buefy";
import App from './App';

const moment = require("moment");

Vue.use(Buefy, {
  defaultDateFormatter: (date) => moment(date).format("ddd, DD MMMM YYYY")
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