<template>
  <div class="wrapper">
    <b-table :data="tableData">
      <template slot-scope="props">
        <b-table-column v-for="(column, index) in tableColumns" :key="index" :label="column.title">
          <template v-if="column.field == 'block'">{{ props.row[column.field] }}</template>
          <template v-else>
            <ZoneBlock
              :zoneData="props.row[column.field]"
              :selectedZone="selectedZone"
              :selectedStages="selectedStages"
            ></ZoneBlock>
          </template>
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
import Vue from "vue";
import ZoneBlock from './ZoneBlock';

var moment = require("moment");

function modBase1(dividend, divisor) {
  const ret = dividend % divisor;
  if (ret == 0) return divisor;
  else return ret;
}  

export default Vue.extend({
  data: function() {
    return {
      days: [],
      selectedDay: -1
    }
  },
  components: {
    ZoneBlock
  },
  props: {
    selectedDate: Date,
    selectedZone: Number,
    selectedStages: Array
  },
  computed: {
    tableColumns: function() {
      const headers = [{ title: "Block", field: "block" }];
      const localDate = moment(this.selectedDate);
      for (let i = 0; i < 7; i++) {
        const d = moment(this.selectedDate);
        d.add(i, "days");

        headers.push({
          title: d.format("ddd Do MMM"),
          field: `day${i}`
        });
      }

      return headers;
    },

    tableData: function() {
      const rows = [];
      if (this.days.length == 0) return [];

      for (let blockIndex = 0; blockIndex < 12; blockIndex += 1) {
        const row = {};
        
        row["block"] = `${blockIndex * 2}:00-${(blockIndex + 1) * 2}:30`;
        
        let dayStart = this.selectedDate.getDate() - 1;
        for (let day = 0; day < 7; day += 1) {
          const dayData = this.days[dayStart + day];
          if (dayData != null) 
            row[`day${day}`] = dayData.blocks[blockIndex];
        }
        
        rows.push(row);
      }
      return rows;
    }
  },
  mounted: function() {
    this.selectedDay = new Date().getDate();

    for (let i = 1; i <= 31; i++) {
      let day = i;
      if (day >= 17) day = i - 16;
      const data = {};
      data["day"] = i;

      data["offset"] = Math.ceil(day / 4);
      let stageBase = modBase1(data["offset"] + 12 * (day - 1), 16);
      const blocks = [];
      for (let blockIndex = 0; blockIndex < 12; blockIndex += 1) {
        const block = {
          stage1: modBase1(stageBase + blockIndex, 16),
          stage2: modBase1(stageBase + blockIndex + 8, 16),
          stage3: modBase1(stageBase + blockIndex + 12, 16),
          stage4: modBase1(stageBase + blockIndex + 4, 16)
        };

        blocks.push(block);
      }

      data["blocks"] = blocks;
      this.days.push(data);
    }
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
