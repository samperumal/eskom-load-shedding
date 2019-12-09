<template>
  <div id="app">
    <!-- <img width="25%" src="./assets/logo.png" /> -->
    <div class="columns">
      <!-- <div class="column is-one-fifth">
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
                :type="stage.type"
              >{{ stage.label }}</option>
            </b-select>
          </b-field>
        </b-field>
      </div> -->
      <div class="column">
        <!-- <ZoneGrid
          :selectedDate="selectedDate"
          :selectedZone="selectedZone"
          :selectedStage="selectedStage"
        ></ZoneGrid>-->
        <section v-for="(row, rindex) in matrixRows" :key="rindex">
          <div class="columns">
            <div v-for="(col, cindex) in row" :key="cindex" class="column">
              <div>{{ col.day }}</div>
              <div v-for="(block, bindex) in col.blocks" :key="bindex">
                <span v-for="zone in block">{{ zone }}, </span>
            </div>
          </div>
        </section>
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
      selectedStage: 1,
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
      const icons = [
        "mood",
        "sentiment_satisfied",
        "sentiment_dissatisfied",
        "sentiment_very_dissatisfied",
        "mood_bad"
      ];
      for (let i = 0; i <= 4; i++)
        stages.push({
          key: `stage${i}`,
          label: i == 0 ? "None" : `Stage ${i}`,
          value: i,
          type: i == 0 ? "is-success" : `is-stage${i}`,
          icon: icons[i]
        });
      return stages;
    },
    matrixRows: function() {
      const rows = [];
      for (let index = 0; index < this.matrixData.length; index += 11)
        rows.push(this.matrixData.slice(index, index + 11));
      return rows;
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
