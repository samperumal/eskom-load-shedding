<template>
  <div id="app">
    <!-- <img width="25%" src="./assets/logo.png" /> -->
    <div class="columns">
      <div class="column is-full-mobile is-one-third-tablet is-one-quarter-desktop">
        <div
          class="box is-size-5 has-text-weight-semibold"
        >{{ selectedCity }} Load Shedding Schedule</div>
        <b-field label="City" expanded>
          <b-select placeholder="Select a zone" v-model="selectedCity" type="is-info" expanded>
            <option v-for="option in this.cities" :value="option" :key="option">{{ option }}</option>
          </b-select>
        </b-field>
        <b-field label="Date" expanded>
          <b-datepicker
            placeholder="Click to select..."
            icon="calendar-today"
            v-model="selectedDate"
          ></b-datepicker>
        </b-field>
        <b-field grouped group-multiline expanded>
          <b-field label="Zone" expanded>
            <b-select placeholder="Select a zone" v-model="selectedZone" type="is-info" expanded>
              <option
                v-for="option in this.possibleZones"
                :value="option"
                :key="option"
              >Zone {{ option }}</option>
            </b-select>
          </b-field>
          <b-field label="Stage" expanded>
            <b-select v-model="selectedStage" type="is-info" expanded>
              <option
                v-for="stage in possibleStages"
                :value="stage.value"
                :key="stage.key"
              >{{ stage.label }}</option>
            </b-select>
          </b-field>
        </b-field>
        <b-field label="Summary" expanded>
          <div class="block">
            <div v-for="(day, dindex) in selectedDaysData" :key="dindex" class="block">
              <div class="day-summary">{{ day.label }}</div>
              <div
                v-for="(block, bindex) in day.blocks"
                :key="bindex"
                :class="block.className"
              >{{ block.blockLabel }}</div>
            </div>
          </div>
        </b-field>
      </div>
      <div class="column is-hidden-mobile">
        <ZoneGrid
          :selectedDaysData="selectedDaysData"
          :selectedDate="selectedDate"
          :selectedZone="selectedZone"
          :selectedStage="selectedStage"
        ></ZoneGrid>
      </div>
    </div>
    <section class="footer">
      <div>Developed by Sameshan Perumal</div>
      <div><a href="https://datacartographer.com">https://datacartographer.com</a></div>
    </section>
  </div>
</template>

<script>
import Vue from "vue";
import ZoneGrid from "./components/ZoneGrid";
import { createMatrix, modBase1 } from "./js/eskom-data";
import jhbData from "./js/jhb.json";
import dbnData from "./js/dbn.json";

var moment = require("moment");

const cptData = createMatrix();

export default Vue.extend({
  data: function() {
    const data = {
      selectedDate: new Date(),
      selectedZone: null,
      selectedStage: 1,
      possibleZones: [],
      matrixData: [],
      selectedCity: null,
      cities: ["Cape Town", "Johannesburg", "Durban"]
    };

    data.selectedCity = "Cape Town";
    data.possibleZones = cptData.zones;
    data.selectedZone = cptData.zones[0];
    data.matrixData = cptData.matrix;

    return data;
  },
  components: {
    ZoneGrid
  },
  props: {},
  watch: {
    selectedCity: function(val) {
      let dataSource = null;
      if (val == "Cape Town") dataSource = cptData;
      else if (val == "Johannesburg") dataSource = jhbData;
      else if (val == "Durban") dataSource = dbnData;
      else throw Exception();

      this.possibleZones = dataSource.zones;
      this.selectedZone = dataSource.zones[0];
      this.matrixData = dataSource.matrix;
    }
  },
  methods: {},
  computed: {
    possibleStages: function() {
      const stages = [];
      for (let i = 0; i <= 8; i++)
        stages.push({
          key: `stage${i}`,
          label: i == 0 ? "None" : `Stage ${i}`,
          value: i
        });
      return stages;
    },
    selectedDaysData: function() {
      const localSelectedDate = this.selectedDate;
      const daysResult = [];
      for (let dayOffset = 0; dayOffset < 7; dayOffset++) {
        const currentDay = moment(localSelectedDate).add(dayOffset, "days");

        const dayData = {
          dayIndex: dayOffset,
          label: currentDay.format("ddd Do MMM"),
          blocks: []
        };

        let blocks;
        if (this.selectedCity == "Durban") {
          blocks = this.matrixData[currentDay.day()].blocks;
        } else {
          blocks = this.matrixData[currentDay.date()].blocks;
        }

        for (const block of blocks) {
          for (const stageData of block.stages) {
            if (
              stageData.stage <= this.selectedStage &&
              stageData.zones.includes(this.selectedZone)
            ) {
              dayData.blocks.push({
                blockIndex: block.block,
                blockLabel: `${block.start} - ${block.end}`,
                stageLabel: `Stage ${stageData.stage}`,
                className: `stage${stageData.stage}`,
                zone: this.selectedZone
              });
            }
          }
        }

        if (dayData.blocks.length == 0)
          dayData.blocks.push({
            blockIndex: -1,
            blockLabel: `No load shedding`,
            stageLabel: "",
            className: `stage-0`,
            zone: this.selectedZone
          });

        daysResult.push(dayData);
      }

      return daysResult;
    }
  }
});
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
  padding-left: 1em;
  padding-right: 1em;
  margin-top: 20px;
}
</style>
