<script setup lang="ts">
import { computed, onMounted, reactive, watch } from 'vue';
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

watch(
  () => state.zone,
  (zone) => localStorage.setItem("selectedZone", zone.toString())
)

type DisplaySchedule = { active: Boolean, text: string, date: string }

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
  const prevZone = localStorage.getItem("selectedZone")
  if (prevZone != null && (+prevZone >= 1) && (+prevZone <= 16))
    state.zone = +prevZone

  loadSchedule()
})

const days = computed<DateTime[]>(() => {
  const offsets = [0, 1, 2, 3, 4, 10]
  const dates = offsets.map(ofst => DateTime.now().plus({ days: ofst }))

  return dates
})

const latestSchedule = computed<Map<string, DisplaySchedule[]>>(() => {
  let ret = { show: false, text: "" }
  let schedDict = new Map<string, DisplaySchedule[]>()

  if (state.schedule != null && state.schedule.stages != null) {
    const now = DateTime.now()

    let schedule = state.schedule.stages.map(stage => {
      const start = DateTime.fromISO(stage.start)
      const end = DateTime.fromISO(stage.end)

      return {
        text: `Stage ${stage.stage} from ${start.toLocaleString(DateTime.TIME_24_SIMPLE)} until ${end.toLocaleString(DateTime.TIME_24_SIMPLE)}`,
        date: start.setLocale('en-ZA').toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY),
        end: end,
        active: (start <= now && now <= end)
      }
    })
      .filter(sched => sched.end > DateTime.now())


    for (const sched of schedule) {
      if (!schedDict.has(sched.date))
        schedDict.set(sched.date, []);

      (schedDict.get(sched.date) ?? []).push(sched)
    }
  }

  return schedDict;
})

function mapBlock(value: number, index: number, day: number, state: State): Block {
  let desc = ""
  const ret = {
    stage: value,
    desc: desc,
    period: blocks[index],
    show: value > 0 && value <= state.stage
  }

  const today = DateTime.now().day

  if (state.schedule != null) {
    const start = DateTime.now().startOf('day').plus({ hours: index * 2, days: day - today })
    const end = DateTime.now().startOf('day').plus({ hours: (index + 1) * 2, days: day - today })

    for (const period of state.schedule.stages) {
      const periodStart = DateTime.fromISO(period.start)
      const periodEnd = DateTime.fromISO(period.end)

      if (0 < value && value <= period.stage && periodStart < end && periodEnd >= start) {
        ret.desc = " - Confirmed"
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
    slots: stageData[state.zone][d.day - 1]
      .map((v, i) => mapBlock(v, i, d.day, state))
      .filter(b => b.show)
  }))
})
</script>

<template>
  <header>
    <h3>Cape Town Loadshedding</h3>
  </header>

  <main>
    <div>
      <div class="input">
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
      </div>
      <div v-for="day in dayData" class="day">
        <div class="date">{{ day.disp }}</div>
        <div v-if="day.slots != null && day.slots.length == 0" class="no-shed">No load shedding</div>
        <div v-for="(slot, index) in day.slots">
          <div v-if="slot.show">{{ slot.period }} [Stage {{ slot.stage }}{{ slot.desc }}]</div>
        </div>
      </div>
    </div>
    <div class="schedule">
      <div v-if="state.schedule != null">
        <div style="margin-bottom: 0.5rem;"><a :href="state.schedule.url">{{ state.schedule.site }}</a> schedule updated
          at {{ state.schedule.time }}</div>
        <div v-for="schedPair in latestSchedule" class="sched-day">
          <div>{{ schedPair[0] }}</div>
          <div v-for="sched in schedPair[1]">{{ sched.text }}</div>
        </div>
      </div>
    </div>
  </main>

  <footer>
    <div class="developer">
      <div>Developed by Sameshan Perumal</div>
      <div>
        <a href="https://datacartographer.com">https://datacartographer.com</a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.day {
  margin: 1rem 0;
}

.day .date {
  text-align: center;
  border-bottom: 1px solid gray;
}

.day .no-shed {
  text-align: center;
}

footer {
  text-align: center;
}

.sched-day {
  margin-bottom: 1rem;
}

.developer {
  border-top: 1px solid gray;
  margin-top: 2rem;
}



main>div {
  text-align: center;
}

main .input {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  gap: 1rem;
  margin-top: 1rem;
}

main .schedule {
  border-top: 1px solid gray;
  margin-top: 2rem;
}
</style>
