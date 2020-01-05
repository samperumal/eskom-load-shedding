<template>
  <div id="app">
    <!-- <img width="25%" src="./assets/logo.png" /> -->
    <div class="columns">
      <div class="column is-full-mobile is-one-third-tablet is-one-quarter-desktop">
        <div
          class="box is-size-5 has-text-weight-semibold"
        >{{ selectedCity }} Load Shedding Schedule</div>
        <div class="box" :class="selectedCityLiveStageData.cssclass">
          <div>
            {{ selectedCityLiveStageData.text}}
            <b-button
              class="button"
              :class="selectedCityLiveStageData.cssclass"
              size="is-small"
              style="margin-left: 1em; vertical-align:middle;"
              pack="fas"
              icon-left="sync-alt"
              :custom-class="this.loading ? 'spin' : ''"
              @click="updateLiveStageStatus"
            ></b-button>
          </div>
          <div v-if="selectedCityLiveStageData.known" class="is-size-7" style="margin-top: 1em;">
            (Source
            <a :href="selectedCityLiveStageData.url">{{ selectedCityLiveStageData.site }}</a>
            website at {{ selectedCityLiveStageData.time }})
          </div>
        </div>
        <section>
          <b-field label="City" label-position="on-border">
            <b-select placeholder="Select a zone" v-model="selectedCity" type="is-info" expanded>
              <option v-for="option in this.cities" :value="option" :key="option">{{ option }}</option>
            </b-select>
          </b-field>
          <b-field label="Date" label-position="on-border">
            <b-datepicker
              placeholder="Click to select..."
              icon="calendar-alt"
              v-model="selectedDate"
            ></b-datepicker>
          </b-field>
          <b-field grouped>
            <b-field label="Zone" label-position="on-border" expanded>
              <b-select placeholder="Select a zone" v-model="selectedZone" type="is-info" expanded>
                <option
                  v-for="option in this.possibleZones"
                  :value="option"
                  :key="option"
                >Zone {{ option }}</option>
              </b-select>
            </b-field>
            <b-field label="Stage" label-position="on-border" expanded>
              <b-select v-model="selectedStage" type="is-info" expanded>
                <option
                  v-for="stage in possibleStages"
                  :value="stage.value"
                  :key="stage.key"
                >{{ stage.label }}</option>
              </b-select>
            </b-field>
          </b-field>
        </section>
        <b-field label="Summary">
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
          :blockTitles="blockTitles"
        ></ZoneGrid>
      </div>
    </div>
    <section class="footer">
      <div>Developed by Sameshan Perumal</div>
      <div>
        <a href="https://datacartographer.com">https://datacartographer.com</a>
      </div>
      <div class="acknowledgments is-size-6">
        <div>Acknowledgments</div>
        <div class="acknowledgments-detail">
          <div>
            Developed with
            <a href="https://vuejs.org/">Vue</a>,
            <a href="https://bulma.io/">Bulma</a> and
            <a href="https://buefy.org/">Buefy</a>, hosted by
            <a href="https://www.netlify.com
">Netlify</a>
          </div>
          <div>Tshwane (Pretoria) data provided by Kobus Viljoen</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import Vue from "vue";
import ZoneGrid from "./components/ZoneGrid";
import axios from "axios";
import { createMatrix } from "./js/eskom-data";
import jhbData from "./js/jhb.json";
import dbnData from "./js/dbn.json";
import ptaData from "./js/pta.json";

var moment = require("moment");

const cptData = createMatrix();

const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

export default Vue.extend({
  data: function() {
    const data = {
      selectedDate: new Date(),
      selectedZone: null,
      selectedStage: 1,
      selectedCity: null,
      
      possibleZones: [],
      matrixData: [],
      cities: ["Cape Town", "Johannesburg", "Durban", "Tshwane (Pretoria)"],
      
      liveStageStatus: {
        "Cape Town": null,
        Johannesburg: null,
        Durban: null,
        "Tshwane (Pretoria)": null
      },
      loading: false
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
      else if (val == "Tshwane (Pretoria)") dataSource = ptaData;
      else throw Exception();

      this.possibleZones = dataSource.zones;
      this.selectedZone = dataSource.zones[0];
      this.matrixData = dataSource.matrix;

      // Remember selected city changes
      if (val) localStorage.setItem("selectedCity", val);

      // Update selected stage when selected city changes
    this.updateLiveStageForSelectedCity();
    },

    selectedZone: function(val) {
      // Remember selected zone changes
      if (val) localStorage.setItem("selectedZone", val);
    },

    // Update selected stage when live stage status changes
    liveStageStatus: function(val) {
      this.updateLiveStageForSelectedCity();
    }
  },
  mounted: function() {
    // Attempt to set selected city and zone from saved value in local storage
    const lsSelectedCity = localStorage.getItem("selectedCity");
    const lsSelectedZone = localStorage.getItem("selectedZone");
    if (lsSelectedCity || lsSelectedZone) {
      // Update selected city on next tick to avoid conflicts with initial values
      this.$nextTick(() => {
        if (lsSelectedCity) this.selectedCity = lsSelectedCity;
        // Set zone on next tick to avoid default cascade behaviour of city change
        if (lsSelectedZone)
          this.$nextTick(() => {
            this.selectedZone = lsSelectedZone;
          });
      });
    }

    // Get live stage when app starts
    this.updateLiveStageStatus();
  },
  methods: {
    // Get the latest live stages for supported cities from azure storage
    updateLiveStageStatus: function() {
      if (!this.loading) {
        this.loading = true;

        axios({
          method: "get",
          url: "https://cptloadshed.blob.core.windows.net/stage/current.json",
          headers: { "x-metaplex": "loadshed" }
        }).then(response => {
          this.liveStageStatus = response.data;
          this.loading = false;
        });
      }
    },

    // If the live stage status has data for the selected city, set 
    // the selectedStage to the live stage value
    updateLiveStageForSelectedCity: function() {
      if (
        this.liveStageStatus != null &&
        this.liveStageStatus[this.selectedCity] != null && 
        this.liveStageStatus[this.selectedCity].stage != null
      ) {
        const stageData = this.liveStageStatus[this.selectedCity];
        this.selectedStage = stageData.stage * 1;
      } else {
        this.selectedStage = 0;
      }
    }
  },
  computed: {
    // List of all possible load shedding stages
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

    // Display attributes for the live status for the currently selected city
    selectedCityLiveStageData: function() {
      if (
        this.liveStageStatus != null &&
        this.liveStageStatus[this.selectedCity] != null
      ) {
        const stageData = this.liveStageStatus[this.selectedCity];
        return {
          known: true,
          cssclass: `stage${stageData.stage}`,
          text: stageData.stage != null ? `Stage ${stageData.stage}` : "Load shedding suspended",
          url: stageData.url,
          site: stageData.site,
          time: stageData.time
        };
      } else {
        return {
          known: false,
          cssclass: null,
          text: "Current stage is unknown",
          url: null,
          site: null,
          time: null
        };
      }
    },
    
    // Format the start and end times for each block / row of data
    blockTitles: function() {
      return this.matrixData[0].blocks
        .reduce((acc, block) => [...acc, `${block.start} - ${block.end}`], [])
        .sort((a, b) => parseInt(a.slice(0, 2)) - parseInt(b.slice(0, 2)));
    },

    // Return days and blocks for 7 days from the date selected in the calendar
    // Defaults to a week from today
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
          blocks = this.matrixData[currentDay.date() - 1].blocks;
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
