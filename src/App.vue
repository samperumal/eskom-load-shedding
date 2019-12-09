<template>
  <div id="app">
    <!-- <img width="25%" src="./assets/logo.png" /> -->
    <section>
      <b-field>
        <b-field label="Date">
          <b-datepicker
            placeholder="Click to select..."
            icon="calendar-today"
            v-model="selectedDate"
          ></b-datepicker>
        </b-field>
        <b-field label="Zone">
          <b-select placeholder="Select a zone" v-model="selectedZone" type="is-info">
            <option v-for="option in 16" :value="option" :key="option">Zone {{ option }}</option>
          </b-select>
        </b-field>
        <b-field label="Stage">
          <b-field>
          <b-radio-button
            v-model="selectedStage"
            v-for="stage in possibleStages"
            :key="stage.key"
            :native-value="stage.value"
            :type="stage.type"
          >
            <i class="material-icons md24 mdi-icon">{{ stage.icon }}</i>
            <span style="padding-left: 0.5em;">{{ stage.label }}</span>
          </b-radio-button>
          </b-field>
        </b-field>
      </b-field>
    </section>
    <ZoneGrid
      :selectedDate="selectedDate"
      :selectedZone="selectedZone"
      :selectedStage="selectedStage"
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
      selectedStage: 1
    };
  },
  components: {
    ZoneGrid
  },
  props: {},
  computed: {
    possibleStages: function() {
      const stages = [];
      const icons = ["mood", "sentiment_satisfied", "sentiment_dissatisfied", "sentiment_very_dissatisfied", "mood_bad"];
      for (let i = 0; i <= 4; i++)
        stages.push({
          key: `stage${i}`,
          label: i == 0 ? "None" : `Stage ${i}`,
          value: i,
          type: i == 0 ? "is-success" : `is-stage${i}`,
          icon: icons[i]
        });
      return stages;
    }
  },
  mount: function() {}
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
}
</style>
