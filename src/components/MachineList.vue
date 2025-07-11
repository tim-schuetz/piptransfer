<template>

    <div style="display: flex;">
        
        <div class="machineitemcontainer elcardalternative" style="position: relative;" ref="machinepanelref">

            <div class="elcardalternative" style="padding-top: 10px; padding-bottom: 10px; display: flex; gap:2px; margin-top: 1px; z-index: 999; position: relative; background-color: darkgray; align-items: center; margin-bottom: 5px; width: 160px;">
                <el-tooltip content="Select all">
                    <img :src="selectallicon" width="20px" @click="selectall" style="cursor: pointer;">
                </el-tooltip>
                <el-tooltip content="Deselect all">
                    <img :src="deselectallicon" width="20px" @click="deselectall" style="cursor: pointer;">
                </el-tooltip>

                <el-tooltip content="Change View">
                    <div @click="showmachineasnumber=!showmachineasnumber" style="cursor: pointer; margin-left: 4px; margin-right: 4px;">
                        <label v-if="showmachineasnumber" style="padding: 5px; cursor: pointer; white-space: nowrap;">MAE Name</label>
                        <label v-else style="padding: 5px; cursor: pointer; white-space: nowrap">MAE Number</label>
                    </div>
                </el-tooltip>

                <el-tooltip content="Add workplace">
                    <div>
                        <el-icon style="cursor: pointer; font-size: 20px; margin-top: 4px;" @click="foldandunfoldworkplace" width="20px" class="iconhover"><Plus /></el-icon>
                    </div>
                </el-tooltip>
                
                <!-- <img style="position: absolute; right:0px; cursor: pointer;" :src="addicon" width="16px" @click="foldandunfoldworkplace"> -->

            </div>

            <div style="position: absolute; left:0px; top:0px; height: 22px; width: 95%; background-color: white; z-index:998"></div>

            <!-- <el-button @click="selectall" style="margin-top: 2px; width: 100%; display: block;">Select all</el-button>
            <el-button @click="deselectall" style="margin-top: 2px; width: 100%; display: block; transform:translateX(-12px);">Deselect all</el-button> -->
            <div class="elcardalternative" v-if="addworkcenterexpanded" style="display: flex; flex-direction: column;">
                <el-input v-if="addworkcenterexpanded" v-model="workcenterEingabe" placeholder="workcenter number"></el-input>

                <el-input v-if="addworkcenterexpanded" v-model="nameEingabe" placeholder="display name"></el-input>
                
                <div v-if="addworkcenterexpanded && !materialsfound" style="display: flex; align-items: center; justify-content: center">
                    <div>
                        <el-tooltip content="Get material list from SAP">
                            <el-button style="white-space: nowrap;" type="primary" @click="searchformaterialsinsap">Get materials</el-button>
                        </el-tooltip>
                    </div>
                    <el-button @click="showmaterialaddoption=true">
                        <el-tooltip content="Add material manually">
                            <el-icon class="plusicon"><Plus/></el-icon>
                        </el-tooltip>
                    </el-button>
                </div>

                <el-input v-if="addworkcenterexpanded && showmaterialaddoption" @keyup.enter="showmaterialaddoption=false; addmatnumbertomachinelist()" v-model="matnrtoadd" placeholder="material number"></el-input>
                <div class="elcardalternative" style="padding-top: 8px; padding-bottom: 8px;" v-if="addworkcenterexpanded" ref="matnrsearchbuttonref">
                    <div v-if="materialsformachine.length == 0" style="color:darkgray">no materials yet</div>
                    <div v-for="(material, index) in materialsformachine" :key="index">{{ material }}</div>
                </div>
                <el-button type="primary" v-if="addworkcenterexpanded" @click="addworkplace" style="font-weight: 600">Add machine</el-button>
            </div>

            <div v-for="(machine, index) in machinelist" :key="index">
                <el-tooltip :content="showmachineasnumber ? machine.name : machine.workcenter">
                    <div class="elcardalternative machineitem" :class="machine.active ? 'machineitemactive' : 'machineiteminactive'" style="padding-bottom: 8px; padding-top: 8px;" @click="changemachinestatus(machine.workcenter, machine.active)">
                        <div v-if="showmachineasnumber">{{ machine.workcenter }}</div>
                        <div v-else>{{ machine.name }}</div>

                        <el-icon style="position: absolute; top: 8px; right: 10px; display: flex" @click.stop="getmateriallist(machine.workcenter)"><ArrowRight /></el-icon>
                        <el-icon style="position: absolute; top: 8px; left: 10px; display: flex" @click.stop="removemachine(machine.workcenter)"><Close /></el-icon> <!--Das .stop sorgt dafür, dass das Event nicht an das click Elternelement weiteregeben wird, was nötig ist, da ein Klick auf das x ja nur die Maschine entfernen soll und keine Statusänderung auslösen soll-->
                    </div>
                </el-tooltip>

            </div>

            <el-button type="primary" style="margin-top: 5px; width: 100%;" @click="removeallfilters">Remove all filters</el-button>

        </div>

        <div class="materialitemcontainer elcardalternative" v-if="materialsoverviewexpanded" style="position: relative;">

            <div style="position: absolute; left:0px; top:6px; height: 16px; width: 75%; background-color: white; z-index:998"></div>

            <div style="font-weight: 600;">{{ selectedmachineformaterialview }}</div>
            <el-icon style="position: absolute; top:3px; right:3px; cursor: pointer;" @click="materialsoverviewexpanded=false"><Close /></el-icon>
            
            <div style="margin-top: 7px;">
                <div v-for="(material, index) in materialsforselectedmachine" :key="index" class="materialandiconelementcontainer">
                    <div class="removematerialicon" @click="deletematerial(material)">
                        <el-icon><Delete /></el-icon>
                    </div>
                    <div class="materialitem elcardalternative" style="padding-bottom: 8px; padding-top: 8px;" @click="changeselection(material)" :class="{ 'highlighted': materialselection.selectedmaterials.includes(material) }">
                        {{ material }}
                    </div> 
                </div>
            </div>
            
            <div style="margin-top: 7px;">
                <div v-for="(material, index) in allothermaterials" :key="index" class="materialandiconelementcontainer">
                    <div class="removematerialicon iconhover" @click="deletematerial(material)">
                        <el-icon><Delete /></el-icon>
                    </div>
                    <div class="materialitem elcardalternative" style="padding-bottom: 8px; padding-top: 8px;" @click="changeselection(material)" :class="{ 'highlighted': materialselection.selectedmaterials.includes(material) }">
                        {{ material }}
                    </div> 
                </div>
            </div>

            <el-button type="primary" @click="updatealldata">Apply Selection</el-button>

        </div>

    </div>

</template>

<script setup>
import { getmachinelist, changemachineactivationstatus, addnewmachine, removeworkcenter, fetchmateriallist, removematerial } from '@/services/machinedataapis'
import { fetchmaterialsfromsap } from '@/services/odataapis'
import { onMounted, ref } from 'vue'
import { ArrowRight, Close, Plus, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElLoading } from 'element-plus'
import selectallicon from '@/assets/selectallicon.png'
import deselectallicon from '@/assets/deselectallicon.png'



async function deletematerial(material){
    try{
        await removematerial(material)
        allothermaterials.value = allothermaterials.value.filter(m => m !== material)
    } catch (error) {
        console.error('Fehler beim Entfernen des Materials:', error)
    }
}

// import addicon from '@/assets/addicon.png'
import { materialselectionstore } from '@/stores/filterinformationstore'

const materialselection = materialselectionstore()

function changeselection(material){
    materialselection.changeselectedmaterial(material)
}

async function updatealldata(){
    materialselection.applychangetrigger = !materialselection.applychangetrigger
}

function removeallfilters(){
    materialselection.removeentireselection()
    // Danach automatisch updaten, also nochmal Daten aus dem Backend ziehen
    materialselection.applychangetrigger = !materialselection.applychangetrigger
}

function foldandunfoldworkplace(){
    if(addworkcenterexpanded.value){
        addworkcenterexpanded.value = false;
        materialsformachine.value = []
        materialsfound.value = false
        matnrtoadd.value = ''
    } else{
        addworkcenterexpanded.value = true
    }
}

const matnrsearchbuttonref = ref(null)

const materialsfound = ref(false)
const showmaterialaddoption = ref(false)

const materialsformachine = ref([])
const matnrtoadd = ref('')

function addmatnumbertomachinelist(){
    if(matnrtoadd.value != ''){
        materialsformachine.value.push(matnrtoadd.value)
        matnrtoadd.value = ''
    } else{
        ElMessage.warning('Please first enter a valid material number')
    }
}

async function searchformaterialsinsap(){
    const loader = ElLoading.service({
        target: matnrsearchbuttonref.value,
        background: 'rgba(255, 255, 255, 0.7)'
    })
    try{
        const materialsfromsapref = await fetchmaterialsfromsap()
        if(materialsfromsapref.length > 0){
            materialsformachine.value = materialsfromsapref
        } else{
            ElMessage.warning(`No materials found for the given machine`)
        }
    } catch(error){
        console.error(error)
        ElMessage('The workcenter could not be found in SAP')
    } finally{
        loader.close()
    }
}

const machinepanelref = ref(null)

const materialsoverviewexpanded = ref(false)
const machinelist = ref([])
const showmachineasnumber = ref(true)
const addworkcenterexpanded = ref(false)
const workcenterEingabe = ref('')
const nameEingabe = ref('')
const selectedmachineformaterialview = ref('')

const materialsforselectedmachine = ref([])
const allothermaterials = ref([])

onMounted( async ()=>{
    machinelist.value = await getmachinelist()
})

async function changemachinestatus(machineworkcenter, currentstatus){
    await changemachineactivationstatus(machineworkcenter, !currentstatus)
    machinelist.value = await getmachinelist()
}

async function selectall(){
    for(const machine of machinelist.value){
        await changemachineactivationstatus(machine.workcenter, true)
    }
    machinelist.value = await getmachinelist()
}

async function deselectall(){
    for(const machine of machinelist.value){
        await changemachineactivationstatus(machine.workcenter, false)
    }
    machinelist.value = await getmachinelist()
}

async function addworkplace(){
    if(!workcenterEingabe.value || !nameEingabe.value){
        ElMessage.warning('Please fill in both fields')
    } else{
        const loading = ElLoading.service({
            // lock: true,
            target: machinepanelref.value,
            text: 'Machine is being added',
            background: 'rgba(255, 255, 255, 0.7)',
        })
        try{
            await addnewmachine(workcenterEingabe.value, nameEingabe.value, materialsformachine.value)
            workcenterEingabe.value = "" 
            nameEingabe.value = ""
            materialsformachine.value = []
            addworkcenterexpanded.value = false
        } catch(error){
            console.error('Fehler beim hinzugügen', error)
        } finally{
            loading.close()
            machinelist.value = await getmachinelist()
        }
    }
}

async function removemachine(workcenter){
    try{
        await removeworkcenter(workcenter)
    } catch(error){
        console.error(error)
    }
    finally {
        machinelist.value = await getmachinelist() //mit finally, damit die Liste erst geladen wurde, wenn die API zum Entfernen der Maschine durchgelaufen ist
    }
}

async function getmateriallist(workcenter){

    const allmaterials = await fetchmateriallist(workcenter)
    
    materialsforselectedmachine.value = allmaterials
        .filter(material => material.machineworkcenter === workcenter)
        .map(material => material.materialnumber)
    allothermaterials.value = allmaterials
        .filter(material => !materialsforselectedmachine.value.includes(material.materialnumber))
        .map(material => material.materialnumber)

    selectedmachineformaterialview.value = workcenter
    materialsoverviewexpanded.value = true
}


</script>

<style scoped>
.refreshicon{
    color: rgb(99, 99, 99);
    margin-top: 4px;
}
.refreshicon:hover{
    color: rgb(0, 136, 255)
}
.plusicon{
    color: rgb(99, 99, 99);
    margin-top: 4px;
}
.plusicon:hover{
    color: rgb(0, 136, 255)
}
.highlighted{
    background-color: green;
}
.machineviewselectoption{
    cursor: pointer;
    background-color: white;
    transition: background-color 0.3s ease;
    border: 1px solid grey; 
    padding-top: 1px;
    padding-bottom: 1px;
    padding-left: 2px;
    padding-right: 2px; 
    border-radius: 2px;
    margin-left: 2px;
}
.machineviewselectoption:hover{
    background-color: rgba(128, 128, 128, 0.2);
    transition: background-color 0.3s ease;
}
.materialitemcontainer{
    display: flex;
    flex-direction: column;
    gap: 1px;
    overflow-y: auto;
    height: calc(100vh - 100px);
}

.materialandiconelementcontainer{
    position: relative;
}

.materialitem{
    left: 0px;
    cursor: pointer;
    transition: transform 0.3s ease;
    z-index: 1000;
    transition: transform 0.3s ease;
}
.materialitem:hover{
    transform: scale(1.02);
}

.materialandiconelementcontainer:hover .removematerialicon{
    left: 118px;
    opacity: 1;
}

.materialandiconelementcontainer:hover .materialitem{
    transform: translateX(-13px);
}

.removematerialicon{
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    left: 100px;
    cursor: pointer;
    background-color: #EC4134;
    padding: 5px;
    padding-top: 9px;
    padding-bottom: 9px;
    top: 1px;
    z-index: 1000;
    opacity: 0;
    transition: left 0.3s ease, opacity 0.3s ease;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}




.machineitemcontainer{
    display: flex;
    flex-direction: column;
    gap: 1px;
    min-width: 120px;
    justify-content: flex-start;
    align-items: center;
}
.machineitemactive{
    background-color: white;
}
.machineiteminactive{
    opacity: 0.5;
}
.machineitem{
    cursor: pointer;
    width: 160px;
    transition: transform 0.3s ease;
}
.machineitem:hover{
    transform: scale(1.02);
}
.arrowright{
    transform: rotate(0deg);
    transition: transform 0.3s ease;
}
.arrowdown{
    transform: rotate(90deg);
    transition: transform 0.3s ease;
}


</style>
