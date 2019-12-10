<template>
  <div class="wrapper">
    <b-table :data="tableData">
      <template slot-scope="props">
        <b-table-column v-for="(column, index) in tableColumns" :key="index" :label="column.title">
          <template v-if="column.field == 'block'">{{ props.row[column.field] }}</template>
          <template v-else>
            <!-- <ZoneBlock
              :zoneData="props.row[column.field]"
              :selectedZone="selectedZone"
              :selectedStage="selectedStage"
            ></ZoneBlock> -->
            {{ column.field }}
           {{ props.row[column.field] }} 
          </template>
          <div style="color: red">{{props.row}}</div>
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
      selectedDay: -1
    }
  },
  components: {
    ZoneBlock
  },
  props: {
    matrixData: Array,
    selectedDate: Date,
    selectedZone: String,
    selectedStage: Number
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
      if (this.matrixData.length == 0) return [];

      for (let blockIndex = 0; blockIndex < 12; blockIndex += 1) {
        const row = {};
        
        row["block"] = `${String(blockIndex * 2).padStart(2, '0')}:00 - ${String(blockIndex * 2 + 2).padStart(2, '0')}:30`;
        
        let dayStart = this.selectedDate.getDate() - 1;
        for (let day = 0; day < 7; day += 1) {
          const dayData = this.matrixData[dayStart + day];
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
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
