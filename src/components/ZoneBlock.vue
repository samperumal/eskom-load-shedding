<template>
  <div>
    <div v-for="(zones, key) in zoneData" :key="key">
      <div v-for="(zone, zkey) in zones" :key="zkey" class="zone" :class="`stage${key}`">
      <span v-if="zone == selectedZone && key <= selectedStage">Stage {{ key }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  props: {
    zoneData: Object,
    selectedZone: String,
    selectedStages: Array,
    selectedStage: Number
  } 
});
</script>