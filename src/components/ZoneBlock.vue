<template>
  <div>
    <div v-for="(value, key) in zoneData" :key="key" class="zone is-danger" :class="key">
      <span v-if="value == selectedZone && selectedStages.includes(key)">{{ value }}</span>
    </div>
  </div>
</template>

<script>
import Vue from "vue";

export default Vue.extend({
  props: {
    zoneData: Object,
    selectedZone: Number,
    selectedStages: Array
  } 
});
</script>