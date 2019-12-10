<template>
  <div class="wrapper">
    <b-table :data="tableData">
      <template slot-scope="props">
        <b-table-column v-for="(column, index) in tableColumns" :key="index" :label="column.title">
          <template v-if="column.field == 'block'">
            <div class="box is-white is-half-height">{{ props.row[column.field] }}</div>
          </template>
          <template v-if="props.row[column.field] != null && column.field != 'block'">
            <div class="zone box" :class="props.row[column.field].className">
              {{ props.row[column.field].stageLabel }}
            </div>
          </template>
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script>
import Vue from "vue";

var moment = require("moment");

function modBase1(dividend, divisor) {
  const ret = dividend % divisor;
  if (ret == 0) return divisor;
  else return ret;
}  

export default Vue.extend({
  data: function() {
    return {}
  },
  components: {
  },
  props: {
    selectedDaysData: Array,
    selectedDate: Date,
    selectedZone: String,
    selectedStage: Number
  },
  computed: {
    tableColumns: function() {
      const headers = [{ title: "Block", field: "block" }];
      const dayHeaders = this.selectedDaysData.map((d, i) => ({
        title: d.label,
        field: `day${i}`
      }));

      return headers.concat(dayHeaders);
    },

    tableData: function() {
      const rows = [];
      if (this.selectedDaysData.length == 0) return [];

      for (let blockIndex = 0; blockIndex < 12; blockIndex += 1) {
        const row = {};
        
        row["block"] = `${String(blockIndex * 2).padStart(2, '0')}:00 - ${String(blockIndex * 2 + 2).padStart(2, '0')}:30`;
        
        rows.push(row);
      }

      for (const day of this.selectedDaysData) {
          for (const block of day.blocks){
            if (block.blockIndex >= 0 && rows[block.blockIndex] != null)
              rows[block.blockIndex][`day${day.dayIndex}`] = block;
          }
        }
        
      return rows;
    }
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
