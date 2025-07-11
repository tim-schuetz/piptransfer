<template>

    <div style="display: flex; gap: 5px; width: max-content;" class="mainwrapper">

        <div class="elcardalternative filterbutton" @click="togglemachinelistview" :style="{backgroundColor: showmachinelist ? 'darkgray' : ''}">
            <label style="cursor:pointer">Filters</label>
            <el-icon style="cursor: pointer;"><Filter /></el-icon>
        </div>

        <div class="wrapper" style="position: relative; display: flex; width: max-content;">
        
            <div class="elcardalternative displayedmonthoption" @mouseenter="showdatahovered=true" @mouseleave="showdatahovered=false">
                <label>Show data for</label>
                <el-select v-model="selectedmonthforvisualization" style="width: 150px; margin-left: 5px;">
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
            </div>

            <div class="elcardalternative" style="padding-right: 25px;" :class="adddataoptionexpanded? 'adddataoptionexpanded' : 'adddataoption'" @mouseenter="showdatahovered=true" @mouseleave="showdatahovered=false">
                <el-select v-model="selectedmonthforimport" style="min-width: 120px; margin-left: 25px;">
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
                <el-icon style="position: absolute; margin-left: 5px; top:5px; right:5px; cursor: pointer;" :style="{transform: adddataoptionexpanded ? 'rotate(180deg)' : 'rotate(0deg)'}" @click="adddataoptionexpanded=!adddataoptionexpanded"><ArrowRight/></el-icon>
                <el-tooltip content="Read new data from source">
                    <el-button @click="readnewdatafromsource" style="width: 100%; margin-left: 5px;" type="success">
                        <el-icon><Plus /></el-icon>
                    </el-button>
                </el-tooltip>
                <el-tooltip content="Remove data">
                    <el-button @click="deletedataformonth" style="width: 100%; margin-left: 5px;" type="danger">
                        <el-icon>
                            <Minus />
                        </el-icon>
                    </el-button>
                </el-tooltip>
            </div>

        </div>

        <div class="elcardalternative annualcomparisonbutton" :style="{transform: adddataoptionexpanded ? 'translatex(285px)' : (showdatahovered ? 'translatex(30px)' : '')}">
            <label style="cursor: pointer;">Annual comparison</label>
            <el-icon style="cursor: pointer;"><DataAnalysis/></el-icon>
        </div>

        <div class="elcardalternative renameoptionsbutton" @click="showrenamingoptions=true">
            <label style="cursor: pointer;">Renaming options</label>
            <el-icon><Setting /></el-icon>
        </div>

        <RenamingOptions v-if="showrenamingoptions" @closewindow="closerenamingwindow"/>

    </div>

</template>

<script setup>
import { getnewdatafromsource } from '@/services/qualitydataapis'
import { ref, defineEmits, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { selectedmonthstore } from '@/stores/filterinformationstore';
import { ArrowRight, DataAnalysis, Filter, Plus, Minus, Setting } from '@element-plus/icons-vue'
import { removedataformonth } from '@/services/qualitydataapis';
import RenamingOptions from './RenamingOptions.vue';
import { resizeinfostore } from '@/stores/resizeinfostore';

const resizeinfooptions = resizeinfostore()

function togglemachinelistview(){
    emits('hideunhidemachinelist')
    showmachinelist.value = !showmachinelist.value
    resizeinfooptions.triggerwindowsizechange()
}


function closerenamingwindow(){
    showrenamingoptions.value = false
}

const showrenamingoptions = ref(false)

const emits = defineEmits(['hideunhidemachinelist'])

const showmachinelist = ref(false)

const showdatahovered = ref(false)

const adddataoptionexpanded = ref(false)

const selectedmonthinfo = selectedmonthstore() //selected month for visualization 

const selectedmonthforvisualization = ref('jan')

watch( selectedmonthforvisualization, () => {
    selectedmonthinfo.selectedmonthforvisualization = selectedmonthforvisualization.value
})

const selectedmonthforimport = ref('jan')

async function readnewdatafromsource(){
    if(selectedmonthforimport.value == 'none'){
        ElMessage.warning('Please select month first')
    } else{
        await getnewdatafromsource(selectedmonthforimport.value)
    }
}

async function deletedataformonth(){
    try{
        await removedataformonth(selectedmonthforimport.value)
        ElMessage(`Data for ${selectedmonthforimport.value} was removed`)
    } catch(error){
        console.error(error)
    }
}

</script>

<style scoped>
.annualcomparisonbutton{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    cursor: pointer;
    transform: translateX(0px);
    transition: transform 0.3s ease, color 0.3s ease;
}
.annualcomparisonbutton:hover{
    color: rgb(0, 157, 255);
}
.filterbutton{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    transition: color 0.3s ease;
    cursor: pointer;
}
.filterbutton:hover{
    /* color: lightskyblue; */
    color: rgb(0, 157, 255);
}

.displayedmonthoption{
    display: flex; 
    align-items: center; 
    width: max-content; 
    position: relative;
    z-index: 3;
}

.adddataoption{
    width: 200px;
    position: absolute; 
    left: 0px;
    top:0px;
    transition: left 0.3s ease;
    z-index: 2;
    display: flex;
    width: max-content;
}

.wrapper:hover .adddataoption{
    left: 27px;
    transition: left 0.3s ease;
}

.adddataoptionexpanded{
    display: flex;
    width: max-content;
    position: absolute; 
    left: 265px;
    top:0px;
    transition: left 0.3s ease;
    z-index: 2;
}

.renameoptionsbutton{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    cursor: pointer;
    transition: color 0.3s ease;
    position: absolute;
    right: 23px;    
    height: 30px;
    transition: color 0.3s ease;
}

.renameoptionsbutton:hover{
    color: rgb(0, 157, 255);
}

</style>
