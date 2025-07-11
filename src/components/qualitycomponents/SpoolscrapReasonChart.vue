<template>
    <div class="elcardalternative" style="width: 100%; height: 100%; position:relative; display: flex; flex-direction: column; align-items: center; justify-content: center; box-sizing: border-box">
        <div style="font-weight: 600">{{ title }}</div>
        <div ref="chartRef" style="width: 100%; height: 100%; margin-top: 40px;" :class="leftshiftactive ? 'leftshift' : 'noshift'"></div>
    </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue';
import * as echarts from 'echarts'; 
import { fetchpoolscrapreason } from '@/services/qualitydataapis'
import { spoolscrapfilteroptionsstore } from '@/stores/filterinformationstore';
import { ElLoading } from 'element-plus';

import { renameinfostorage } from '@/stores/renameinfostore';
const renameinfoptions = renameinfostorage()

const title = ref('Spool scrap according to cause')


import { resizeinfostore } from '@/stores/resizeinfostore';

const leftshiftactive = ref(false)

const resizeinfooptions = resizeinfostore()

watch(
    () => resizeinfooptions.windowsizechanged, () =>{
        leftshiftactive.value = !leftshiftactive.value;
    }
)

const spoolscrapfilteroptions = spoolscrapfilteroptionsstore()

//dadurch fällt die Notwendigkeit für watch() weg, da die Werte so nun automatisch in der .vue aktualisiert werden, wenn sie sich im Pinia store ändern

import { materialselectionstore, selectedmonthstore } from '@/stores/filterinformationstore';

const materialselection = materialselectionstore()
const selectedmonthinfo = selectedmonthstore()

watch(
    () => materialselection,
    () => {
        loadchart()
    }
)

watch(
    () => selectedmonthinfo.selectedmonthforvisualization,
    () =>{
        loadchart()
    }
)

watch(
  () => spoolscrapfilteroptions.selectedproductforspoolfilter,
  async () => {
    // Async-Funktion innerhalb des Watch-Callbacks aufrufen
    const updateDiagram = async () => {
        const loading = ElLoading.service({
            target: chartRef.value,
            text: 'Data is updating',
            background: 'rgba(255, 255, 255, 0.7)'
        })
        try{
            const spoolscrapreasons = await fetchpoolscrapreason()
            diagramdata.value = spoolscrapreasons.map(element => {
                return {value: element.cost, name: element.issue };
            })
            initChart()
        } catch(error){
            console.error(error)
        } finally{
            loading.close()
        }
    }

    updateDiagram()
  }
)

const diagramdata = ref([])

const chart = ref(null);
const chartRef = ref(null);

const initChart = () => {

    if(chart.value){
        chart.value.dispose()
    }

    chart.value = echarts.init(chartRef.value)

    const option = {
        // title: {
        //     text: 'Spool Scrap according to cause',
        //     left: 'center'
        // },
        tooltip: {
            trigger: 'item'
        },
        series: [
            {
            name: 'Access From',
            type: 'pie',
            radius: '70%',
            data: diagramdata.value,
            emphasis: {
                itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
            }
        ]
        };

    chart.value.setOption(option)

}

async function loadchart(){
    const loading = ElLoading.service({
        target: chartRef.value,
        text: 'Data is loading',
        background: 'rgba(255, 255, 255, 0.7)'
    })
    try{
        const spoolscrapreasons = await fetchpoolscrapreason()
        diagramdata.value = spoolscrapreasons.map(element => {
            return {value: element.cost, name: element.issue };
        })
        initChart()
    } catch(error){
        console.error(error)
    } finally{
        loading.close()
    }
}

onMounted(async () =>{
    title.value = renameinfoptions.getcomponentrenaming('spoolscrapaccordingtocause')
    loadchart()
})

onBeforeUnmount(() =>{
    if(chart.value){
        chart.value.dispose()
        chart.value = null
    }
})

</script>

<style scoped>
.leftshift{
    transform: translateX(-50px);
}
.noshift{
    transform: translateX(0px);
}
</style>