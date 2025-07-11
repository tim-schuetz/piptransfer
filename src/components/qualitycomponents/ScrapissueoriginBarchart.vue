<template>
    <div class="elcardalternative" style="display: flex; flex-direction: column; align-items: center; width: 100%; height: 100%; box-sizing: border-box; padding: 10px;">
        <div style="font-weight: 600;">{{ title }}</div>
        <div ref="chartRef" style="width: 100%; height: 100%; margin-top: 30px;"></div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'
import { fetchscrapissueorigins } from '@/services/qualitydataapis'
import { ElLoading } from 'element-plus';
import { materialselectionstore, selectedmonthstore } from '@/stores/filterinformationstore';
import { renameinfostorage } from '@/stores/renameinfostore';

const renameinfoptions = renameinfostorage()

const title = ref('Cause of scrap issue')

const materialselection = materialselectionstore()
const selectedmonthinfo = selectedmonthstore()
//Test
watch(
    () => selectedmonthinfo.selectedmonthforvisualization,
    () =>{
        loadchart()
    }
)

watch(
    () => materialselection.applychangetrigger,
    () =>{
        loadchart()
    }
)

const chart = ref(null);
const chartRef = ref(null);

const scrapissueorigins = ref([])

const initChart = () =>{

    if(chart.value){
        chart.value.dispose()
    }

    chart.value = echarts.init(chartRef.value)

    const rawData = scrapissueorigins.value

    // const rawData = [                           //statt den Raw Data hier die Daten aus der API reinholen
    //     { amount: "11901", issue: "阀芯尺寸", material: "NG10 Spool" },
    //     { amount: "1954",  issue: "阀芯表面", material: "NG10 Spool" },
    //     { amount: "106",   issue: " 零件损坏", material: "NG6 Spool" },
    //     { amount: "21864", issue: "阀芯尺寸", material: "NG6 Spool" },
    //     { amount: "7124",  issue: "阀芯表面", material: "NG6 Spool" }
    // ];

    // 1. Materialnamen extrahieren (X-Achse)
    const materials = [...new Set(rawData.map(item => item.material))];

    const displaymaterials = []
    for (const materialname of materials){
        const newmaterialname = renameinfoptions.getmaterialrenaming(materialname)
        displaymaterials.push(newmaterialname)
    }

    // 2. Issue-Typen extrahieren
    const issues = [...new Set(rawData.map(item => item.issue.trim()))];

    // 3. Series strukturieren
    const series = issues.map(issue => {
    return {
        name: issue,
        type: 'bar',
        stack: 'total',
        data: materials.map(material => {
        const match = rawData.find(
            item => item.material === material && item.issue.trim() === issue
        );
        return match ? parseInt(match.amount) : 0;
        })
    };
    });

    const option = {
    xAxis: {
        type: 'category',
        data: displaymaterials,
        axisLabel: {
            rotate: 45,
            interval: 0,
            fontSize: 10
        }
    },
    yAxis: {
        type: 'value'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: issues
    },
    series: series
    };

    chart.value.setOption(option)

}

async function loadchart(){
    const loader = ElLoading.service({
        target: chartRef.value,
        text: 'Data is being loaded',
        background: 'rgba(255, 255, 255, 0.7)'
    })
    try{
        scrapissueorigins.value = await fetchscrapissueorigins()
        initChart()
    } catch(error){
        console.error(error)
    } finally{
        loader.close()
    }
}

onMounted( async () =>{
    title.value = renameinfoptions.getcomponentrenaming('causeofscrapissue')
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



</style>
