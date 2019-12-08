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
        <b-select placeholder="Select a zone" v-model="zone">
          <option
            v-for="option in 16"
            :value="option"
            :key="option">
            Zone {{ option }}
          </option>
        </b-select>
      </b-field>
    </section>
    <ZoneGrid :selectedDate="selectedDate" :zone="zone"></ZoneGrid>
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
  zone = 11;

  mount() {
    
  }

}
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
