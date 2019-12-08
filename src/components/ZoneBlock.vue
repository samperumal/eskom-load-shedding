<template>
    <div>
        <div v-for="(value, key) in zoneData" class="zone" :class="key">
            <span v-if="value == selectedZone">{{ value }}</span>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import Component from "vue-class-component";

@Component({
  props: {
    zoneData: Object,
    selectedZone: Number
  }
})
export default class ZoneBlock extends Vue {
    
}
</script>