
<template>
  <div>
    <div class="container mx-12 my-4 w-full flex flex-row justify-around content-center items-center">
      <div class="w-fit">
        <div class="text-sm mb-2 font-bold text-gray-600">Intervalo de análise:</div>
        <DatePicker v-model="date_range" range :preset-dates="presetDates">
          <template #preset-date-range-button="{ label, value, presetDate }">
            <span 
                role="button"
                :tabindex="0"
                @click="presetDate(value)"
                @keyup.enter.prevent="presetDate(value)"
                @keyup.space.prevent="presetDate(value)">
              {{ label }}
            </span>
          </template>
        </DatePicker>
      </div>
      <div class="w-3/12">
        <div>Filtrando por: {{ picked }}</div>

        <div class="">
          <input type="radio" id="cais" value="CAIS" v-model="picked" />
          <label for="cais">CAIS</label>
        </div>

        <div class="">
          <input type="radio" id="pop" value="PoP" v-model="picked" />
          <label for="two">PoP</label>
        </div>

        <div v-if="picked==='PoP'">
          <input v-model="pop_value" class="p-1 border border-gray-500 rounded" />
        </div>
      </div>
      <button @click="updateReport()" class="py-1 px-2 border border-gray-500 rounded-lg mt-4 text-sm text-gray-600 hover:bg-gray-600 hover:text-white">
        Atualizar
      </button>
    </div>
  </div>

  <div class="container mx-auto bg-gray-100 rounded-xl p-8 m-10 flex flex-col">
    <div class="flex flex-row justify-center content-center align-center">
      <div class="w-5/12">
        <Chart type="polarArea" title="grafico1" :labels="['Red', 'Orange', 'Yellow', 'Green', 'Blue']" :dataset="[11, 16, 7, 3, 14]" label="Ameaças" />
      </div>
      <div class="flex flex-row flex-wrap w-2/4">
        <div class="w-2/4">
          <Chart type="line" title="grafico2" :labels="['Red', 'Orange', 'Yellow', 'Green', 'Blue']" :dataset="[11, 16, 7, 3, 14]" label="Ameaças" />
        </div>
        <div class="w-2/4">
          <Chart type="line" title="grafico3" :labels="['Red', 'Orange', 'Yellow', 'Green', 'Blue']" :dataset="[11, 16, 7, 3, 14]" label="Ameaças" />
        </div>
        <div class="w-2/4">
          <Chart type="line" title="grafico4" :labels="['Red', 'Orange', 'Yellow', 'Green', 'Blue']" :dataset="[11, 16, 7, 3, 14]" label="Ameaças" />
        </div>
        <div class="w-2/4">
          <Chart type="line" title="grafico5" :labels="['Red', 'Orange', 'Yellow', 'Green', 'Blue']" :dataset="[11, 16, 7, 3, 14]" label="Ameaças" />
        </div>
      </div>
    </div>
    <div class="flex flex-row justify-between content-center align-center mt-10">
      <div class="w-full">
        <Table />
      </div>
    </div>
  </div>

</template>

<script setup>
  import Chart from "./components/Chart.vue"
  import Table from "./components/Table.vue"


  let date_range = ref()
  let picked = ref()
  let pop_value = ref()


  onMounted(() => {
    const startDate = new Date();
    const endDate = startDate.setHours(new Date().getHours() - 8);
    date_range.value = [startDate, endDate];

    picked.value = 'CAIS';
    pop_value = ''
  })
</script>

<script>
  import { ref, watch, computed, onMounted } from 'vue';
  import { get } from 'lodash'
  import DatePicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css';
  import axios from 'axios'
  import { endOfMonth, endOfYear, startOfMonth, startOfYear, subMonths } from 'date-fns'
    
  export default {
      components: { DatePicker },
      props: {
        'modelValue': String, 
      },

      methods:{
        updateReport(){
          console.log("teste")
        }
      },

      setup(props, { emit }) {

        const presetDates = ref([
          { label: 'Today', value: [new Date(), new Date()] },
          {
            label: 'Today (Slot)',
            value: [new Date(), new Date()],
            slot: 'preset-date-range-button'
          },
          { label: 'This month', value: [startOfMonth(new Date()), endOfMonth(new Date())] },
          {
            label: 'Last month',
            value: [startOfMonth(subMonths(new Date(), 1)), endOfMonth(subMonths(new Date(), 1))],
          },
          { label: 'This year', value: [startOfYear(new Date()), endOfYear(new Date())] },
        ]);

        // expose the ref to the template
        return {
          date_range, presetDates
        }
      }
  }
</script>
