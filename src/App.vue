<script setup lang="ts">
import { computed, onMounted, reactive } from 'vue';
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

const zones = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

const stages = [0, 1, 2, 3, 4, 5, 6, 7, 8]

type Schedule = {
  url: string,
  site: string,
  time: string,
  stages: { stage: number, start: string, end: string }[]
}

type State = {
  zone: number,
  stage: number,
  schedule: Schedule | null
}

type Block = {
  stage: number,
  desc: string,
  period: string,
  show: boolean
}

const state = reactive<State>({
  zone: 11,
  stage: 0,
  schedule: null
})

function loadSchedule() {
  fetch("https://cptloadshed.blob.core.windows.net/stage/current.json", {
    headers: { "x-metaplex": "loadshed" }
  })
    .then(resp => {
      if (resp.status == 200) {
        resp.json()
          .then(data => state.schedule = data["Cape Town"])
          .catch(error => state.schedule = null)
      }
    })
    .catch(error => state.schedule = null)
}

onMounted(() => {
  loadSchedule()
})

const days = computed<DateTime[]>(() => {
  const offsets = [0, 1, 2, 3, 4]
  const dates = offsets.map(ofst => DateTime.now().plus({ days: ofst }))

  return dates
})

const currentStage = computed<{ show: Boolean, text: string }>(() => {
  let ret = { show: false, text: "" }
  if (state.schedule != null && state.schedule.stages != null) {
    const now = DateTime.now()
    for (const stage of state.schedule.stages) {
      const start = DateTime.fromISO(stage.start)
      const end = DateTime.fromISO(stage.end)
      if (start <= now && now <= end) {
        ret.show = true
        ret.text = `Stage ${stage.stage} from ${start.toLocaleString(DateTime.TIME_24_SIMPLE)} until ${end.toLocaleString(DateTime.TIME_24_SIMPLE)}`
      }
    }
  }

  return ret;
})

function mapBlock(value: number, index: number, day: number, state: State): Block {
  let desc = "Possible"
  const ret = {
    stage: value,
    desc: desc,
    period: blocks[index],
    show: value > 0 && value <= state.stage
  }

  if (state.schedule != null) {
    const start = DateTime.now().startOf('day').plus({ hours: index * 2 })
    const end = DateTime.now().startOf('day').plus({ hours: (index + 1) * 2 })
  
    for (const period of state.schedule.stages) {
      const periodStart = DateTime.fromISO(period.start)
      const periodEnd = DateTime.fromISO(period.end)
      
      if (0 < value && value <= period.stage && periodStart < end && periodEnd >= start) {
        ret.desc = "Confirmed"
        ret.show = true
      }
      
    }
  }

  return ret
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
    slots: stageData[state.zone][d.day - 1].map((v, i) => mapBlock(v, i, d.day, state))
  }))
})
</script>

<template>
  <header style="display: flex; flex-direction: column; place-content: center;">
    <div>Zone:
      <select v-model="state.zone">
        <option v-for="zone in zones" :value="zone">{{ zone }}</option>
      </select>
    </div>
    <div>Stage:
      <select v-model="state.stage">
        <option v-for="stage in stages" :value="stage">{{ stage }}</option>
      </select>
    </div>
    <div v-if="state.schedule != null">
      <div>Updated at {{ state.schedule.time }} from <a :href="state.schedule.url">{{ state.schedule.site }}</a></div>
      <div>{{ currentStage.text }}</div>
    </div>
  </header>

  <main>
    <div v-for="day in dayData">
      <div>{{ day.disp }}</div>
      <div v-if="day.slots != null && day.slots.length == 0">No load shedding</div>
      <div v-for="(slot, index) in day.slots">
        <div v-if="slot.show">{{ slot.period }} [Stage {{ slot.stage }} - {{ slot.desc }}]</div>
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
