<template>
  <div id="app">
    <!-- <img width="25%" src="./assets/logo.png" /> -->
    <section>
      <b-field label="Select a date">
        <b-datepicker placeholder="Click to select..." icon="calendar-today" v-model="selectedDate"></b-datepicker>
      </b-field>
      <b-field label="Zone">
        <b-select placeholder="Select a zone" v-model="selectedZone" type="is-info">
          <option v-for="option in 16" :value="option" :key="option">Zone {{ option }}</option>
        </b-select>
      </b-field>
      <div class="block">
        <b-checkbox v-model="selectedStages" native-value="stage1" type="is-stage1">Stage 1</b-checkbox>
        <b-checkbox v-model="selectedStages" native-value="stage2" type="is-stage2">Stage 2</b-checkbox>
        <b-checkbox v-model="selectedStages" native-value="stage3" type="is-stage3">Stage 3</b-checkbox>
        <b-checkbox v-model="selectedStages" native-value="stage4" type="is-stage4">Stage 4</b-checkbox>
      </div>
    </section>
    <ZoneGrid
      :selectedDate="selectedDate"
      :selectedZone="selectedZone"
      :selectedStages="selectedStages"
    ></ZoneGrid>
  </div>
</template>

<script>
import Vue from "vue";
import ZoneGrid from "./components/ZoneGrid";

export default Vue.extend({
  data: function() {
      return {
        selectedDate: new Date(),
        selectedZone: 11,
        selectedStages: ["stage1", "stage2", "stage3", "stage4"],
      }
  },
  components: {
    ZoneGrid
  },
  props: {
    
  },
  mount() {
    
  }
});
</script>