<template>
  <div id="app">
    <!-- <img width="25%" src="./assets/logo.png" /> -->
    <div class="columns">
      <div class="column is-one-fifth">
        <b-field grouped group-multiline>
          <b-field label="Date" expanded>
            <b-datepicker
              placeholder="Click to select..."
              icon="calendar-today"
              v-model="selectedDate"
            ></b-datepicker>
          </b-field>
          <b-field label="Zone" expanded>
            <b-select placeholder="Select a zone" v-model="selectedZone" type="is-info" expanded>
              <option v-for="option in 16" :value="option" :key="option">Zone {{ option }}</option>
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
        <b-label>Summary</b-label>
        <div class="block">
          <div v-for="(block, index) in activeBlocks" :key="index" :class="block.stage">
            {{ block.block }}
          </div>
        </div>
      </div>
      <div class="column">
        <ZoneGrid
          :matrixData="matrixData"
          :selectedDate="selectedDate"
          :selectedZone="selectedZone"
          :selectedStage="selectedStage"
        ></ZoneGrid>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import ZoneGrid from "./components/ZoneGrid";
import { createMatrix } from "./js/eskom-data";

// console.log("Starting");
// const data = createMatrix();
// console.log(data);

export default Vue.extend({
  data: function() {
    return {
      selectedDate: new Date(),
      selectedZone: 11,
      selectedStage: 6,
      matrixData: createMatrix()
    };
  },
  components: {
    ZoneGrid
  },
  props: {},
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
    matrixRows: function() {
      const rows = [];
      for (let index = 0; index < this.matrixData.length; index += 11)
        rows.push(this.matrixData.slice(index, index + 11));
      return rows;
    },
    activeBlocks: function() {
      const blocksResult = [];
      const selectedDay = this.selectedDate.getDate();

      for (const day of this.matrixData) {
        if (day.day != selectedDay) continue;
        for (const blockIndex in day.blocks) {
          const block = day.blocks[blockIndex];
          for (const stage in block) {
            const zone = block[stage];
            if (zone != this.selectedZone) continue;
            if (stage > this.selectedStage) continue;
            blocksResult.push({
              day: day.day,
              block: `${blockIndex * 2}:00 - ${blockIndex * 2 + 2}:30`,
              stage: `stage${stage}`
            });
          }
        }
      }

      return blocksResult;
    }
  },
  mounted: function() {}
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
  margin-top: 20px;
  padding-left: 1em;
  padding-right: 1em;
}
</style>
