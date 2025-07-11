<template>

    <div class="maincontainer" style="width: 100%; height: 100%; display: flex; gap: 5px; overflow-y: hidden;">

        <MachineList v-if="showmachinelist" />
            
        <div class="visualizationscontainer" style="display: flex; flex-direction: column; gap:5px; overflow-y: hidden; height: 100%; width: 100%; overflow-x: hidden">

            <DataDisplayOption @hideunhidemachinelist="showmachinelist=!showmachinelist"/>

            <div style="display: flex; gap:5px; width: 99%; height: 400px;">

                <div style="display: flex; flex-direction: column; gap:5px; width: 30.18%">
                    <div style="height: 70%; width: 100%;">
                        <NcroriginPiechart class="visualcard" @click="expandedcomponent='ncroriginpiechartopened'; showexpandedvisual=true"/>
                    </div>
                    <div style="height: 30%; width: 100%;">
                        <ScrappermethodKpi class="visualcard" @click="expandedcomponent='scrappermethodkpiopened'; showexpandedvisual=true"/>
                    </div>
                </div>
                <div style="width: 69.82%">
                    <ScrapissueoriginBarchart class="visualcard" @click="expandedcomponent='scrapissueoriginbarchartopened'; showexpandedvisual=true"/>
                </div>
            </div>

            <div style="display: flex; gap:5px; width: 99%; height: 320px; position: relative">
                <div style="width:30%">
                    <SpoolscrapReasonChart class="visualcard" @click="expandedcomponent='spoolscrapreasonchartopened'; showexpandedvisual=true"/>
                </div>
                <div style="width: 35%; height: 100%">
                    <SpoolscrapmethodsChart class="visualcard" @click="expandedcomponent='spoolscrapmethodschartopened'; showexpandedvisual=true"/> 
                </div>
                <div style="width: 35%; height: 100%; display: flex; flex-direction: column; gap:5px; position: relative;">
                    <div style="width: 100%; height: 35%;">
                        <MostfrequentscrapissuesKpi class="visualcard" @click="expandedcomponent='mostfrequentscrapissueskpiopened'; showexpandedvisual=true"/> 
                    </div>
                    <div style="width: 100%; height: 65%;">
                        <!-- <SpoolscrapexclusiveFilter class="visualcard" @click="expandedcomponent='spoolscrapexclusivefilteropened'; showexpandedvisual=true"/> -->
                        <SpoolscrapexclusiveFilter />
                    </div>
                </div>
            </div>

            <div style="display: flex; gap:5px; width: 99%; height: 300px">
                <div style="width: 30%">
                    <SupplierOfCastings class="visualcard" @click="expandedcomponent='supplierofcastingsopened'; showexpandedvisual=true"/>
                </div>
                <div style="width: 35%;">
                    <SupplierOfNoneCastings class="visualcard" @click="expandedcomponent='supplierofnonecastingsopened'; showexpandedvisual=true"/>
                </div>
                <div style="width: 35%;">
                    <SupplierInternal class="visualcard" @click="expandedcomponent='supplierinternalopened'; showexpandedvisual=true"/>
                </div>
            </div>

            <div v-if="showexpandedvisual" style="z-index: 999;">
                <div class="backgroundblur"></div>
                <div class="expandedvisualcontainer">
                    <!-- <div style="height: 100%; width: 100%; background-color: black;"></div> -->
                    <component :is="expandablecomponents[expandedcomponent]"></component>
                    <el-icon style="position: absolute; top: 60px; right: 60px; cursor: pointer; font-size: larger;" @click="showexpandedvisual=false"><Close/></el-icon>
                </div>
            </div>

        </div> 

    </div>

</template>

<script setup>
import NcroriginPiechart from '@quality/NcroriginPiechart.vue';
import SupplierOfCastings from '@quality/SupplierOfCastings.vue';
import SupplierOfNoneCastings from '@quality/SupplierOfNoneCastings.vue';
import SupplierInternal from '@quality/SupplierInternal.vue';
import ScrapissueoriginBarchart from '@quality/ScrapissueoriginBarchart.vue'
import SpoolscrapmethodsChart from '@quality/SpoolscrapmethodsChart.vue';
import SpoolscrapReasonChart from '@quality/SpoolscrapReasonChart.vue';
import SpoolscrapexclusiveFilter from '@quality/SpoolscrapexclusiveFilter.vue';
import MostfrequentscrapissuesKpi from '@quality/MostfrequentscrapissuesKpi.vue';
import ScrappermethodKpi from '@quality/ScrappermethodKpi.vue';
import DataDisplayOption from '@quality/DataDisplayOption.vue';
import MachineList from '@/components/MachineList.vue';
import { Close } from '@element-plus/icons-vue'

import { ref, onMounted, onUnmounted } from 'vue'

const showmachinelist = ref(false)

onMounted(() =>{
    window.addEventListener('keydown', closeexpandedvisual)
})

onUnmounted(() =>{
    window.removeEventListener('keydown', closeexpandedvisual)
})

function closeexpandedvisual(){
    if(showexpandedvisual.value == true){
        showexpandedvisual.value = false
    }
}

const showexpandedvisual = ref(false)
const expandedcomponent = ref('ncroriginpiechartopened')

const expandablecomponents = ref({
    ncroriginpiechartopened: NcroriginPiechart,
    supplierofcastingsopened: SupplierOfCastings,
    supplierofnonecastingsopened: SupplierOfNoneCastings,
    supplierinternalopened: SupplierInternal,
    scrapissueoriginbarchartopened: ScrapissueoriginBarchart,
    spoolscrapmethodschartopened: SpoolscrapmethodsChart,
    spoolscrapreasonchartopened: SpoolscrapReasonChart,
    spoolscrapexclusivefilteropened: SpoolscrapexclusiveFilter,
    mostfrequentscrapissueskpiopened: MostfrequentscrapissuesKpi,
    scrappermethodkpiopened: ScrappermethodKpi,
    datadisplayoptionopened: DataDisplayOption
})

// const ncroriginpiechartopened = ref(false)
// const supplierofcastingsopened = ref(false)
// const supplierofnonecastingsopened = ref(false)
// const SupplierInternalopened = ref(false)
// const scrapissueoriginbarchartopened = ref(false)
// const spoolscrapmethodschartopened = ref(false)
// const spoolscrapreasonchartopened = ref(false)
// const spoolscrapexclusivefilteropened = ref(false)
// const mostfrequentscrapissueskpiopened = ref(false)
// const scrappermethodkpiopened = ref(false)
// const datadisplayoptionopened = ref(false)

//Hier die ganzen echarts rein für die einzelnen Visualisierungen (siehe Skript Informatik zur Orientierung)

</script>

<style scoped>
.visualcard{
    transform: scale(1);
    transition: transform 0.3s ease;
    z-index: 1;
}
.visualcard:hover{
    transform: scale(1.01);
    transition: transform 0.3s ease;
}
.expandedvisualcontainer{
    position: fixed;
    top: 0px;
    left: 0px;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 50px;
    box-sizing: border-box;
    border-radius: 10px;
}
.backgroundblur{
    position: fixed;
    top: 0px;
    left: 0px;
    height: 100vh;
    width: 100vw;
    background-color: rgba(255, 255, 255, 0.8);
}

</style>


