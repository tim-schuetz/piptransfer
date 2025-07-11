<template>
    <div class="elcardalternative" style="display: flex; flex-direction: column; width: 100%; height: 100%; box-sizing: border-box; padding: 10px;">
        <div style="font-weight: 600;">{{ title }}</div>
        <div ref="chartRef" style="width: 100%; height: 100%; margin-top: 10px;" :class="leftshiftactive ? 'leftshift' : 'noshift'"></div>
    </div>

</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue';
import * as echarts from 'echarts'; 
import { ElLoading } from 'element-plus';
import { fetchncrorigins } from '@/services/qualitydataapis'
import { materialselectionstore, selectedmonthstore } from '@/stores/filterinformationstore'
import { renameinfostorage } from '@/stores/renameinfostore';
import { resizeinfostore } from '@/stores/resizeinfostore';

const leftshiftactive = ref(false)

const resizeinfooptions = resizeinfostore()

watch(
    () => resizeinfooptions.windowsizechanged, () =>{
        leftshiftactive.value = !leftshiftactive.value;
    }
)

const renameinfoptions = renameinfostorage()

const title = ref('ncr')

const selectedmonthinfo = selectedmonthstore()

const materialselection = materialselectionstore()

watch(
    () => materialselection.applychangetrigger, () =>{
        loadchart()
    }
)

watch(
    () => selectedmonthinfo.selectedmonthforvisualization,
    () =>{
        loadchart()
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
        //     text: 'NCR',
        //     subtext: 'PP | P2P | Internal Scrap',
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
            center: ['50%', '50%'],
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
        text: 'Data is being loaded',
        background: 'rgba(255, 255, 255, 0.7)'
    })
    try{
        const ncrorigins = await fetchncrorigins()
        diagramdata.value = ncrorigins.map(element => {
            return {value: element.amount, name: element.origin };
        })        
        initChart()
    } catch(error){
        console.error(error)
    } finally{
        loading.close()
    }
}

onMounted(async () =>{
    title.value = renameinfoptions.getcomponentrenaming('ncr')
    loadchart()
    window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() =>{
    if(chart.value){
        chart.value.dispose()
        chart.value = null
    }

    window.removeEventListener('resize', handleResize)

})

function handleResize() {
  if (chart.value) {
    chart.value.resize()
  }
}

</script>

<style scoped>
.leftshift{
    transform: translateX(-50px);
}
.noshift{
    transform: translateX(0px);
}
</style>
