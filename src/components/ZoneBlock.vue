<template>
  <div>
    <div v-for="(value, key) in zoneData" :key="key" class="zone" :class="`stage${key}`">
      <span v-if="value == selectedZone && key <= selectedStage">Stage {{ key }}</span>
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