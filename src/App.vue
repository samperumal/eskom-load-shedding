<template>
  <div id="app">
    <!-- <img width="25%" src="./assets/logo.png" /> -->
    <section>
      <b-field label="Select a date">
        <b-datepicker          
          placeholder="Click to select..."
          icon="calendar-today"
          v-model="selectedDate"          
        ></b-datepicker>
      </b-field>
      <b-field label="Zone">
        <b-select placeholder="Select a zone" v-model="selectedZone" type="is-info">
          <option
            v-for="option in 16"
            :value="option"
            :key="option">
            Zone {{ option }}
          </option>
        </b-select>
      </b-field>
      <div class="block">
        <b-checkbox v-model="selectedStages" native-value="stage1" type="is-stage1">Stage 1</b-checkbox>
        <b-checkbox v-model="selectedStages" native-value="stage2" type="is-stage2">Stage 2</b-checkbox>
        <b-checkbox v-model="selectedStages" native-value="stage3" type="is-stage3">Stage 3</b-checkbox>
        <b-checkbox v-model="selectedStages" native-value="stage4" type="is-stage4">Stage 4</b-checkbox>
      </div>
    </section>
    <ZoneGrid :selectedDate="selectedDate" :selectedZone="selectedZone" :selectedStages="selectedStages"></ZoneGrid>
  </div>
</template>

<script>
import Vue from "vue";
import Component from "vue-class-component";
import ZoneGrid from "./components/ZoneGrid";

@Component({
  components: {
    ZoneGrid
  },
  props: {
    
  }
})
export default class App extends Vue {
  selectedDate = new Date();
  selectedZone = 11;
  selectedStages = ["stage1", "stage2", "stage3", "stage4"];

  mount() {
    
  }

}
</script>

<style lang="scss">
// Import Bulma's core
@import "~bulma/sass/utilities/_all";

@import "./styles/styles.scss";

// Import Bulma and Buefy styles
@import "~bulma";
@import "~buefy/src/scss/buefy";

</style>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.zone {
  text-align: center;
  color: white;
  font-weight: bold;
}
</style>
