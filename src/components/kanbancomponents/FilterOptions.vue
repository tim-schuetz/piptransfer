<template>

    <div class="filtercardcontainer">

        <div class="headingcontainer">
            <label>Filter parameters</label>
            <div class="switchiconcontainer">
                <el-tooltip content="Switch to KPI overview">
                    <el-icon class="iconhover" @click="switchbetweenkpifilters"><Switch /></el-icon>
                </el-tooltip>
            </div>
        </div>
        
        <el-card class="filtercard" shadow="hover">
            <div style="display: flex; align-items: center;">
                <label style="font-weight: 600; margin-bottom: 5px;">Material Filter</label>
                <el-icon style="transform: translate(2px, -2px);"><Filter /></el-icon>
            </div>
            <el-select v-model="materialfilter">
                <el-option v-for="matnr in materialfilteroptions" :key="matnr" :value="matnr">{{ matnr }}</el-option>
                <el-option value="all">All</el-option>
            </el-select>
        </el-card>

        <el-card class="filtercard" shadow="hover">
            <div style="display: flex; align-items: center;">
                <label style="font-weight: 600; margin-bottom: 5px;">Loop Filter</label>
                <el-icon style="transform: translate(2px, -2px);"><Filter /></el-icon>
            </div>
            <el-select v-model="loopfilter">
                <el-option v-for="loop in loopfilteroptions" :key="loop" :value="loop">{{ loop }}</el-option>
                <el-option value="all">All</el-option>
            </el-select>
        </el-card>

        <el-card class="filtercard" style="margin-bottom: 5px;">
            <div style="display: flex; align-items: center;">
                <label style="font-weight: 600; margin-bottom: 5px;">Month filter</label>
                <el-icon style="transform: translate(2px, -2px);"><Filter /></el-icon>
            </div>                
            <el-select v-model="monthfilter">
                <el-option value="all" label="All"></el-option>
                <el-option value="jan" label="January"></el-option>
                <el-option value="feb" label="February"></el-option>
                <el-option value="mar" label="March"></el-option>
                <el-option value="apr" label="April"></el-option>
                <el-option value="may" label="May"></el-option>
                <el-option value="jun" label="June"></el-option>
                <el-option value="jul" label="July"></el-option>
                <el-option value="aug" label="August"></el-option>
                <el-option value="sep" label="September"></el-option>
                <el-option value="oct" label="October"></el-option>
                <el-option value="nov" label="November"></el-option>
                <el-option value="dec" label="December"></el-option>
            </el-select>
        </el-card>

        <el-card v-if="showxaxisselectionforleadtimebymatchart" class="filtercard" style="margin-bottom: 5px;">
            <div style="display: flex; align-items: center;">
                <label style="font-weight: 600; margin-bottom: 5px;">x-axis parameter</label>
                <el-icon class="sorticon"><SortUp /></el-icon>
            </div>
            <el-select v-model="xaxisparameter">
                <el-option value="ordernumber" label="ordernumber"></el-option>
                <el-option value="material" label="materialnumber"></el-option>
                <el-option value="kanbanid" label="kanban ID"></el-option>
            </el-select>
        </el-card>
        
        <el-card class="filtercard escalationcard" style="background-color: aliceblue;">
            <div style="display: flex; align-items: center;">
                <label style="font-weight: 600; margin-bottom: 5px;">Escalation threshold</label>
                <el-icon style="transform: translate(3px, -3px)"><WarnTriangleFilled /></el-icon>
                <el-icon class="escalationcardsettings iconhover" @click="showescalationactionwindow=true"><Setting /></el-icon>
            </div>
            <div style="display: flex; justify-content: flex-start; align-items: baseline;">
                <el-input type="number" v-model=escalationthreshold style="width: 110px"></el-input>
                <label style="margin-left: 5px;">hours</label>
            </div>
        </el-card>

        <el-button type="primary" style="margin-top: 10px; width: 100%;" @click="applyfilterselection">Apply</el-button>

    </div>
<!-- 
    <Teleport to="body">
    <div v-if="showescalationactionwindow"
        style="position: fixed; top: 50vh; left: 50vw; transform: translate(-50%, -50%); z-index: 9999; background: white; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.3); border-radius: 10px;">
        <label>Test</label>
        <EscalationWindow />
    </div>
    </Teleport> -->

    <el-dialog v-model="showescalationactionwindow" title="Define Escalation Action" width="700px" center>
        <EscalationWindow />
    </el-dialog>

</template>

<script setup>
import { Filter, Switch, SortUp, WarnTriangleFilled, Setting } from '@element-plus/icons-vue'
import { getkanbanfilteroptions } from '@/services/kanbandataapis';
import { onMounted, ref, watch, defineEmits } from 'vue';
import { currentlydisplayedchartstore } from '@/stores/kanbanfilterinformationstore';
import { kanbanfilterinfostore } from '@/stores/kanbanfilterinformationstore';
import EscalationWindow from './EscalationWindow.vue';

const showescalationactionwindow = ref(false)

const emits = defineEmits(['switchbetweenkpifilters'])

function switchbetweenkpifilters(){
    emits('switchbetweenkpifilters')
}

const kanbanfilterinfooptions = kanbanfilterinfostore()

const materialfilter = ref('all')
const loopfilter = ref('all')
const monthfilter = ref('all')
const xaxisparameter = ref('ordernumber')

function applyfilterselection(){
    kanbanfilterinfooptions.setselectedmaterial(materialfilter.value)
    kanbanfilterinfooptions.setselectedloop(loopfilter.value)
    kanbanfilterinfooptions.setselectedmonth(monthfilter.value)
    kanbanfilterinfooptions.setxaxisparameter(xaxisparameter.value)
    console.log("aus applyfilterselection")
}


const currentlydisplayedchartoptions = currentlydisplayedchartstore()

watch(
    () => currentlydisplayedchartoptions.currentchart,
    () => {
        recalculateadditionalvisuals
    }
)

const showxaxisselectionforleadtimebymatchart = ref(false)

function recalculateadditionalvisuals(){
    if (currentlydisplayedchartoptions.currentchart == 'leadtimebymaterials'){
        showxaxisselectionforleadtimebymatchart.value = true;
    } else {
        showxaxisselectionforleadtimebymatchart.value = false;
    }
}

const escalationthreshold = ref(30)

const materialfilteroptions = ref([])
const loopfilteroptions = ref([])
const monthfilteroptions = ref([])


onMounted( async () =>{
    recalculateadditionalvisuals()
    const data = await getkanbanfilteroptions()
    materialfilteroptions.value = data.uniquematerialslist
    loopfilteroptions.value = data.uniqueloopslist
    monthfilteroptions.value = data.uniquemonths_as_int
})

</script>

<style scoped>
.filtercardcontainer{
    display: flex; 
    flex-direction: column; 
    align-items: center;
}
.filtercard{
    width: 100%;
}
.headingcontainer{
    font-weight: 600; 
    font-size: 20px; 
    transform: translate(10px, -5px); 
    display: flex; 
    align-items: center; 
    gap: 5px;
    transition: transform 0.3s ease;
}
.switchiconcontainer{
    display: flex;
    align-items: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}
.filtercardcontainer:hover .headingcontainer{
    transform: translate(0px, -5px);
    transition: transform 0.3s ease;
}
.filtercardcontainer:hover .switchiconcontainer{
    opacity: 1;
    transition: opacity 0.3s ease;
}
.sorticon{
    transform: translate(3px, -2px) rotate(90deg) scaleX(-1);
}

.escalationcardsettings{
    transform: translate(-17px, -3px);
    opacity: 0;
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.escalationcard:hover .escalationcardsettings{
    transform: translate(9px, -3px);
    opacity: 1;
    transition: transform 0.3s ease, opacity 0.3s ease;
}

</style>
