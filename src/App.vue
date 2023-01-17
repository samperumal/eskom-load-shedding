<script setup lang="ts">
import { computed, reactive } from 'vue';
import stageDataJson from './cpt-zone-day-block.json'
import { DateTime } from 'luxon';

const stageData = reactive(stageDataJson as number[][][])

const blocks = [
  "00:00 - 02:00",
  "02:00 - 04:00",
  "04:00 - 06:00",
  "06:00 - 08:00",
  "08:00 - 10:00",
  "10:00 - 12:00",
  "12:00 - 14:00",
  "14:00 - 16:00",
  "16:00 - 18:00",
  "18:00 - 20:00",
  "20:00 - 22:00",
  "22:00 - 00:00",
]

const state = reactive({
  zone: 11,
  stage: 6
})

const days = computed<DateTime[]>(() => {
  const offsets = [0, 1, 2, 3, 4]
  const dates = offsets.map(ofst => DateTime.now().plus({ days: ofst }))

  return dates
})

function slots(day: DateTime) {
  return stageData[day.day-1].map((dayArray : number[]) => dayArray.slice(0, state.stage))//.includes(state.zone))
}

const dayData = computed(() => {
  return days.value.map(d => ({
    disp: d.setLocale('en-ZA').toLocaleString({
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      weekday: 'short'
    }),
    date: d, 
    slots: stageData[state.zone][d.day - 1]
  }))
})
</script>

<template>
  <header>
    <div>Zone: {{ state.zone }}</div>
    <div>Stage: {{ state.stage }}</div>
  </header>

  <main>
    <div v-for="day in dayData">
      <div>{{ day.disp }}</div>
      <div v-for="(slot, index) in day.slots">
        <div v-if="slot > 0 && slot <= state.stage">{{ blocks[index] }} [Stage {{ slot }}]</div>
      </div>
    </div>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
