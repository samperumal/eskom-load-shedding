import Vue from 'vue';
import Buefy from "buefy";
import App from './App';
import axios from 'axios';

const moment = require("moment");

Vue.use(Buefy, {
  defaultDateFormatter: (date) => moment(date).format("ddd, DD MMMM YYYY")
});
Vue.config.productionTip = false;

new Vue({
  el: '#app',
  data() {
    return {
      currentStage: {
        "Cape Town": null,
        "Johannesburg": null,
        "Durban": null
      }
    }
  },
  render: function (h) { return h(App, { props: { currentStage: this.currentStage } }); },
  mounted: function () {
    //checkStage();
    axios({
      method: "get",
      url: "https://cptloadshed.blob.core.windows.net/stage/current.json",
      headers: { "x-metaplex": "loadshed" }
    })
      .then((response) => {
        this.currentStage = response.data;
      });
  }
});