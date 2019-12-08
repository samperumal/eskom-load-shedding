<template>
    <div>
        <div v-for="(value, key) in zoneData" class="zone is-danger" :class="key">
            <span v-if="value == selectedZone && selectedStages.includes(key)">{{ value }}</span>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import Component from "vue-class-component";

@Component({
  props: {
    zoneData: Object,
    selectedZone: Number,
    selectedStages: Array
  }
})
export default class ZoneBlock extends Vue {
    
}
</script>