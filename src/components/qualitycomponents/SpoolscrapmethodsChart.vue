<template>
    <div class="elcardalternative" style="display: flex; flex-direction: column; height: 100%; width: 100%; box-sizing: border-box;">
        <div style="font-weight: 600;">{{ title }}</div>
        <div ref="chartRef" style="height: 100%; width: 100%;"></div>
    </div>

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { fetchspoolscrapmethods } from '@/services/qualitydataapis'
import * as echarts from 'echarts'
import { ElLoading } from 'element-plus';
import { renameinfostorage } from '@/stores/renameinfostore';

const renameinfoptions = renameinfostorage()

const title = ref('Spool scrap according to method')


import { spoolscrapfilteroptionsstore } from '@/stores/filterinformationstore';

const spoolscrapfilteroptions = spoolscrapfilteroptionsstore()

import { materialselectionstore, selectedmonthstore } from '@/stores/filterinformationstore';

const materialselection = materialselectionstore()
const selectedmonthinfo = selectedmonthstore()

watch(
    () => materialselection.applychangetrigger,
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
  () => {
    // Async-Funktion innerhalb des Watch-Callbacks aufrufen
    const updateDiagram = async () => {
        const loading = ElLoading.service({
            target: chartRef.value,
            text: 'Data is updating according to filter selections',
            background: 'rgba(255, 255, 255, 0.7)'
        })
        try{
            const spoolscrapmethods = await fetchspoolscrapmethods()
            xdata.value = spoolscrapmethods.map(element => element.method)
            ydata.value = spoolscrapmethods.map(element => element.cost)
            initchart()
        } catch(error){
            console.error(error)
        } finally{
            loading.close
        }
    }

    updateDiagram()
  }
)

const chartRef = ref(null)
const chart = ref(null)
const xdata = ref([])
const ydata = ref([])

async function loadchart(){
    const loading = ElLoading.service({
        target: chartRef.value,
        text: 'Data is loading',
        background: 'rgba(255, 255, 255, 0.7)'
    })
    try{
        const spoolscrapmethods = await fetchspoolscrapmethods()
        xdata.value = spoolscrapmethods.map(element => element.method)
        ydata.value = spoolscrapmethods.map(element => element.cost)
        initchart()
    } catch(error){
        console.error(error)
    } finally{
        loading.close()
    }
}

onMounted( async () =>{
    loadchart()
    title.value = renameinfoptions.getcomponentrenaming('spoolscrapaccordingtomethod')
})

function initchart(){
    
    if(chart.value){
        chart.value.dispose()
    }

    chart.value = echarts.init(chartRef.value)

    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
            type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
            type: 'category',
            data: xdata.value,
            axisTick: {
                alignWithLabel: true
            }
            }
        ],
        yAxis: [
            {
            type: 'value'
            }
        ],
        series: [
            {
            name: 'Direct',
            type: 'bar',
            barWidth: '60%',
            data: ydata.value
            }
        ]
    };

    chart.value.setOption(option)

}

onBeforeUnmount(() =>{
    if(chart.value){
        chart.value.dispose()
        chart.value = null
    }
})

</script>

<style scoped>

</style>

