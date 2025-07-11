<template>
    <div class="elcardalternative" style="display: flex; flex-direction: column; width: 100%; height: 100%; box-sizing: border-box;">
        <div style="font-weight: 600;">{{ title }}</div>
        <div ref="chartRef" style="height: 100%; width: 100%;"></div>
    </div>

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { fetchsuppliersinternal } from '@/services/qualitydataapis'
import * as echarts from 'echarts'
import { ElLoading } from 'element-plus'
import { materialselectionstore, selectedmonthstore } from '@/stores/filterinformationstore';
import { renameinfostorage } from '@/stores/renameinfostore';

const renameinfoptions = renameinfostorage()

const title = ref('P2P Part')

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

const chartRef = ref(null)
const chart = ref(null)
const xdata = ref([])
const ydata = ref([])

async function loadchart(){
    const loader = ElLoading.service({
        target: chartRef.value,
        text: 'Data is being loaded',
        background: 'rgba(255, 255, 255, 0.7)'
    })
    try{
        const suppliersinternal = await fetchsuppliersinternal()
        const xdata_raw = suppliersinternal.map(element => element.supplier)
        xdata.value = xdata_raw.map(item => {
            if(item.toLowerCase().startsWith('hodgen')){
                return 'HIT'
            } else if(item.toLowerCase().startsWith('jiangsu')){
                return 'HJ'
            } else if(item.toLowerCase().startsWith('king')){
                return 'KKHT'
            } else if(item.toLowerCase().startsWith('liaoning')){
                return 'SW'
            } else if(item.toLowerCase().startsWith('suzhou')){
                return 'CMS'
            }
            else if(item.toLowerCase().startsWith('not')){
                return 'not defined'
            } else{
                return item
            }
        })
        ydata.value = suppliersinternal.map(element => element.amount)
        initchart()
    } catch(error){
        console.error(error)
    } finally{
        loader.close()
    }
}

onMounted( async () =>{
    title.value = renameinfoptions.getcomponentrenaming('p2ppart')
    loadchart()
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

