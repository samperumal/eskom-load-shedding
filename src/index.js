import Vue from 'vue';
import App from './App';

const moment = require("moment");

import { library } from '@fortawesome/fontawesome-svg-core';
// internal icons
import { faSyncAlt, faCalendarAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(faSyncAlt, faCalendarAlt);
Vue.component('vue-fontawesome', FontAwesomeIcon);


import Buefy from "buefy";
Vue.use(Buefy, {
  defaultDateFormatter: (date) => moment(date).format("ddd, DD MMMM YYYY"),
  defaultIconComponent: 'vue-fontawesome',
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