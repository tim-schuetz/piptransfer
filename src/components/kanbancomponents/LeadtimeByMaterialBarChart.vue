<template>

    <div class="elcardalternative" style="display: flex; flex-direction: column; align-items: center; width: 100%; height: 100%; box-sizing: border-box; padding: 10px;">
        <div style="font-weight: 600;">Leadtimechart</div>
        <div ref="chartRef" style="width: 100%; height: 100%; margin-top: 30px;"></div>
    </div>

</template>

<script setup>
import { ElLoading } from 'element-plus';
import { onMounted, onBeforeUnmount, watch, ref } from 'vue';
import * as echarts from 'echarts'
import { getleadtimebymatnrs } from '@/services/kanbandataapis';
import { kanbanfilterinfostore } from '@/stores/kanbanfilterinformationstore';

const kanbanfilterinfooptions = kanbanfilterinfostore()

watch(
    [() => kanbanfilterinfooptions.selectedLoop, () => kanbanfilterinfooptions.selectedMaterials, () => kanbanfilterinfooptions.selectedMonthasint],
    () =>{
        loadChart()
    }
)

onMounted( async () =>{
    await loadChart()
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

async function loadChart(){
    const loader = ElLoading.service({
        target: chartRef.value,
        text: 'Data is being loaded',
        background: 'rgba(255, 255, 255, 0.7)'
    })
    try{
        const data = await getleadtimebymatnrs()
        xdata.value = data.materials
        ydata.value = data.leadtimes
        initChart()
    } catch(error){
        console.error(error)
    } finally{
        loader.close()
    }
}

const chartRef = ref(null)
const chart = ref(null)
const xdata = ref([])
const ydata = ref([])

function initChart() {

    if (chart.value) {
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
                axisLabel: {
                    rotate: 45,
                    interval: 0, //sorgt dafür, dass keine Werte ausgelassen werden, auch wenn die Schriftgröße das eigentlich nicht zulässt
                    fontSize: 10
                },
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

</script>

<style scoped>

</style>