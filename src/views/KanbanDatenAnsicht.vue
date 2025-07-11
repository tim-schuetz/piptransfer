<template>

    <div class="header" style="position: fixed; top:0px; left:0px; background-color: aquamarine; height: 60px; width: 100vw; display: flex; justify-content: center; align-items: center;">
        <h1>Kanban Super Time Analysis Dashboard</h1>
        <div class="uploadicon" @click="renewkanbandatafromsource">
            <el-tooltip content="renew data from source">
                <el-icon style="z-index: 4;">
                    <Upload />
                </el-icon>
            </el-tooltip>
        </div>
    </div>

    <div class="maincontainer" style="display: flex; margin-top: 10px; height: calc(100vh - 90px);" ref="maincontainerref">
        <div class="leftcol" style="width: 250px; padding: 10px; background-color: #f8f9fa; border-right: 1px solid #ddd; overflow-y: auto;"> <!--width: 220px-->
            <div v-if="!showkpioverview">
                <div style="font-weight: 600; font-size: 20px; transform: translateY(-5px);">Filter parameters</div>

                <el-card class="leftcol-card" shadow="hover">
                    <div style="display: flex; align-items: center;">
                        <label style="font-weight: 600; margin-bottom: 5px;">Sorting Parameter</label>
                        <el-icon style="transform: translate(2px, -2px);"><Sort /></el-icon>
                    </div>
                    <el-select v-model="sorftfor" placeholder="Sort by" style="width: 100%;">
                        <el-option value="leadtime">Lead time</el-option>
                        <el-option value="kanbanID">Kanban ID</el-option>
                        <el-option value="Date">Creation date</el-option>
                    </el-select>
                </el-card>

                <el-card class="leftcol-card" shadow="hover">
                    <div style="display: flex; align-items: center;">
                        <label style="font-weight: 600; margin-bottom: 5px;">Material Filter</label>
                        <el-icon style="transform: translate(2px, -2px);"><Filter /></el-icon>
                    </div>
                    <el-select v-model="materialfilter">
                        <el-option v-for="matnr in materialfilteroptions" :key="matnr" :value="matnr">{{ matnr }}</el-option>
                        <el-option value="all">All</el-option>
                    </el-select>
                </el-card>

                <el-card class="leftcol-card" shadow="hover">
                    <div style="display: flex; align-items: center;">
                        <label style="font-weight: 600; margin-bottom: 5px;">Loop Filter</label>
                        <el-icon style="transform: translate(2px, -2px);"><Filter /></el-icon>
                    </div>
                    <el-select v-model="loopfilter">
                        <el-option v-for="loop in loopfilteroptions" :key="loop" :value="loop">{{ loop }}</el-option>
                        <el-option value="all">All</el-option>
                    </el-select>
                </el-card>

                <el-card class="leftcol-card">
                    <div style="display: flex; align-items: center;">
                        <label style="font-weight: 600; margin-bottom: 5px;">Condensed view</label>
                        <el-switch v-model="showscondensedview" style="margin-left: 8px;"></el-switch>
                    </div>
                </el-card>
                
                <el-card>
                    <div style="font-weight: 600; margin-bottom: 5px; transform: translateX(-20px);">Escalation threshold</div>
                    <div style="display: flex; justify-content: flex-start; align-items: baseline;">
                        <el-input type="number" v-model=escalationthreshold style="width: 110px"></el-input>
                        <label style="margin-left: 5px;">hours</label>
                    </div>
                </el-card>

                <el-button type="primary" @click="showkpioverview=true" style="margin-top: 10px; width: 100%;">Switch to KPI Overview</el-button>

            </div>

            <div v-else>
                <el-card class="leftcol-card" shadow="hover">
                    <h3>Kanban KPI Overview</h3>
                    <p>Average leadtime: <strong> {{ avgleadtime.toFixed(2) }}</strong></p>
                    <p>Longest leadtime: <strong> {{ maxleadtime.toFixed(2) }} </strong></p>
                    <p>Shortest leadtime: <strong> {{ minleadtime.toFixed(2) }} </strong></p>
                    <p>Total amount: <strong> {{ totalvalues }} </strong></p>
                    <el-button type="primary" @click="showkpioverview=false" style="margin-top: 10px; width: 100%;">Back to Filters</el-button>
                </el-card>
            </div>

        </div>
        
        <div class="rightcol" style="width: calc(100vw - 200px); height: 90vh; background-color: aliceblue; position: relative; margin-left: 5px;">
            
            <div v-if="showscondensedview" style="margin-top: 5px; overflow-x: scroll; position: absolute; top:0px; left:0px; height: 100%; width: 100%; display: flex; flex-direction: column; gap: 3px; overflow-y: scroll;">

                <div v-for="(element, index) in kanbaninfos" :key="index" class="materialelement" :style="{ display: element.month === selectedmonthasnumber ? 'block' : 'none', width: element.leadtimeinh * lengthofanhourunit + 'px', color: element.leadtimeinh > escalationthreshold ? 'red' : 'black'}" @click="showmaterialdetails(element.material, element.idnumber, element.creationdate, element.creationtime, element.status, element.ordernumber, element.cntcycle, element.leadtimeinh, element.activationstatus)">
                    <div>
                        <label style="font-size: medium; font-weight: 600;"> {{ element.idenumber }} </label>
                        <label style="font-size: small; color:grey; margin-left: 10px;"> {{ element.material }} </label>
                    </div>
                </div>

                <el-select v-model="selectedmonth" style="position: fixed; top:80px; right:25px; width: 100px;">
                    <el-option v-for="(month, index) in monthselectoptions.monthsasword" :key="index" :value="month">{{ month }}</el-option>
                </el-select>

            </div>

            <div v-else style="margin-top: 5px; overflow-x: scroll; position: absolute; top:0px; left:0px; height: 100%; width: 100%; display: flex; flex-direction: column; gap: 3px; overflow-y: scroll;">

                <div v-for="(element, index) in kanbaninfos" :key="index" class="materialelement" :style="{ display: element.month === selectedmonthasnumber ? 'block' : 'none', width: element.leadtimeinh * lengthofanhourunit + 'px', transform: 'translatex(' + element.hourssincemonthbeginning * 30 + 'px)'}" @click="showmaterialdetails(element.material, element.idnumber, element.creationdate, element.creationtime, element.status, element.ordernumber, element.cntcycle, element.leadtimeinh, element.activationstatus)">
                    {{ element.material }}
                </div>

                <el-select v-model="selectedmonth" style="position: fixed; top:80px; right:25px; width: 100px;">
                    <el-option v-for="(month, index) in monthselectoptions.monthsasword" :key="index" :value="month">{{ month }}</el-option>
                </el-select>

                <div class="dateelementcontainer" style="display: flex; position: absolute; bottom:0px; left:0px;">
                    <div v-for="h in 744" :key="h" style="display: flex;"> 
                        <div v-if="h % 24 == 0" :style="{ width: lengthofanhourunit + 'px'}" style="height: 20px; background-color: rgba(128, 128, 128, 0.1); border-left: 1px solid black; display: flex; align-items: center; justify-content: center;">{{ selectedmonthasnumber }}-{{ h / 24 }}</div>
                        <div v-else :style="{ width: lengthofanhourunit + 'px'}" style="height: 20px; background-color: rgba(128, 128, 128, 0.1); border-left: 1px solid black; display: flex; align-items: center; justify-content: center; color:grey; font-size: 12px;">{{ transformnumber(h) }}</div>
                    </div>
                </div>

            </div>

            <div style="position: fixed; top: 80px; right: 140px; width: 200px; display: flex; justify-content: center; align-items: center; padding-left:8px; padding-right:15px; border-radius: 8px; background-color: rgba(128, 128, 128, 0.1);">
                <el-slider ref="sliderRef" v-model="lengthofanhourunit" :min="1" :max="30" :step="1"></el-slider>
            </div>

            <div style="position: absolute; bottom: 13px; display: flex; align-items: center ;width: 4500px">
                <div v-for="t in 5" :key="t" :style="{ width: lengthofanhourunit * 24 + 'px' }" class="timelineelement">{{ t }}</div>
                <div style="position: absolute; left: 10px; color: white; margin-top: 2px;">Duration unit: Days</div>
            </div>

            <div v-if="showmaterialinfowindow" style="position: fixed; top:50vh; left:50vw; transform: translate(-50%, -50%); background-color: white; border:3px solid black; border-radius: 8px; display: flex; flex-direction: column; width:400px">
                <div style="position: absolute; top:3px; left:3px; font-weight: 600; font-size: 20px;">{{ selectedorder }}</div>
                <div style="position: absolute; top:25px; left:3px; color:grey; font-size: 14px">Kanban-ID: {{ selectedidenumber }} | Material: {{ selectedmaterial }} | CntCycle: {{ selectedcntcycle }}</div>
                <el-card style="height: 45px;"></el-card>
                <el-card>Created: {{ selectedcreationdate }}</el-card>
                <el-card>Leadtime: {{ selectedleadtime.toFixed(2) }}h</el-card>
                <el-card :class="selectedactivationstatus == 'open' ? 'activeelement' : 'inactiveelement' ">Kanban status: {{ selectedkanbanstatus }} [{{ selectedactivationstatus }}]</el-card>
                <el-icon class="closeicon" style="position: absolute; top: 5px; right: 5px" @click="showmaterialinfowindow=false">
                    <close-bold />
                </el-icon>
            </div>

        </div>

    </div>

    <SettingsWindow v-if="showsettingswindow" @removesettingswindow="showsettingswindow=false" @changelanguage="changelanguagesettings(language)" @changefetchinterval="changefetchintervalsettings(interval)" @changeviewmode="changeviewmodesettings(mode)" />

</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { ElIcon, ElMessage, ElSlider } from 'element-plus'
import { Filter, Sort, Upload } from '@element-plus/icons-vue'
import SettingsWindow from '@kanban/SettingsWindow.vue'
import { CloseBold } from '@element-plus/icons-vue'
import { ElLoading } from 'element-plus'
import { fetchkanbaninfo } from '@/services/kanbandataapis'
import { updatekanbandatabase } from '@/services/kanbandataapis'


import { nextTick } from 'vue'

const sliderRef = ref(null)

const showscondensedview = ref(true)

watch(showscondensedview, async (newVal) => {
  if (newVal) {
    await nextTick()
    // Falls du Zugriff auf den Slider-Ref hast:
    sliderRef.value?.updatePopper?.()
  }
})


const avgleadtime = ref('')
const minleadtime = ref('')
const maxleadtime = ref('')
const totalvalues = ref('')

const showkpioverview = ref(false)

const escalationthreshold = ref(50)

const lengthofanhourunit = ref(30)

function transformnumber(n) {
  return ((n - 1) % 24) + 1;
}

const showmaterialinfowindow = ref(false)
const selectedmaterial = ref('')
const selectedidenumber = ref('')
const selectedcreationdate = ref('')
const selectedcreationtime = ref('')
const selectednumber = ref('')
const selectedkanbanstatus = ref('')
const selectedorder = ref('')
const selectedcntcycle = ref('')
const selectedleadtime = ref(0)
const selectedactivationstatus = ref('') 

function showmaterialdetails(material, idenumber, creationdate, creationtime, number, kanbanstatus, order, cntcycle, leadtime, activationstatus){
    showmaterialinfowindow.value = true
    selectedmaterial.value = material
    selectedidenumber.value = idenumber
    selectedcreationdate.value = creationdate
    selectedcreationtime.value = creationtime
    selectednumber.value = number
    selectedkanbanstatus.value = kanbanstatus
    selectedorder.value = order
    selectedcntcycle.value = cntcycle
    selectedleadtime.value = Number(leadtime)
    selectedactivationstatus.value = activationstatus
}


//Wozu ref wichtig ist: Macht die Variablen zu reaktiven Objekten, d.h. das bei Verändeurng der Variablen die Werde dieser im Div geupdated werden.
//Das ist beispielweise entscheident, wenn die Daten für die Variablen aus einer API im Backend kommen und damit erst nachdem das Template gerendert wurde.

const showsettingswindow = ref(false)

// const earliesttimestamp = ref([])
const monthselectoptions = ref({monthsasnumber: [], monthsasword: []})

const sorftfor = ref('leadtime')
const materialfilter = ref('All')
const loopfilter = ref('All')
const materialfilteroptions = ref([])
const loopfilteroptions = ref([])

const selectedmonth = ref('May')
const selectedmonthasnumber = ref(5)

watch(selectedmonth, async () =>{
    if(selectedmonth.value == 'January'){
        selectedmonthasnumber.value = 1
    } 
    else if(selectedmonth.value == 'February'){
        selectedmonthasnumber.value = 2
    }
    else if(selectedmonth.value == 'March'){
        selectedmonthasnumber.value = 3
    }
    else if(selectedmonth.value == 'April'){
        selectedmonthasnumber.value = 4
    }
    else if(selectedmonth.value == 'May'){
        selectedmonthasnumber.value = 5
    }
    else if(selectedmonth.value == 'June'){
        selectedmonthasnumber.value = 6
    }
    else if(selectedmonth.value == 'July'){
        selectedmonthasnumber.value = 7
    }
    else if(selectedmonth.value == 'August'){
        selectedmonthasnumber.value = 8
    }
    else if(selectedmonth.value == 'September'){
        selectedmonthasnumber.value = 9
    }
    else if(selectedmonth.value == 'October'){
        selectedmonthasnumber.value = 10
    }
    else if(selectedmonth.value == 'November'){
        selectedmonthasnumber.value = 11
    }
    else if(selectedmonth.value == 'December'){
        selectedmonthasnumber.value = 12
    }
})

onMounted(() =>{
    getkanbaninfo(materialfilter.value, loopfilter.value, sorftfor.value)
})

watch(sorftfor, async () => {
    await getkanbaninfo(materialfilter.value, loopfilter.value, sorftfor.value)
})

watch(materialfilter, async () => {
    await getkanbaninfo(materialfilter.value, loopfilter.value, sorftfor.value)
})

watch(loopfilter, async () => {
    await getkanbaninfo(materialfilter.value, loopfilter.value, sorftfor.value)
})

const maincontainerref = ref(null)

const kanbaninfos = ref([])

async function getkanbaninfo(){
    const loading = ElLoading.service({
        target: maincontainerref.value,
        text: 'data is being loaded',
        background: 'rgba(255, 255, 255, 0.7)'
    })
    try{
        const [kanbaninfos_dummy, materialfilteroptions_dummy, loopfilteroptions_dummy, monthselectoptions_dummy, avgleadtime_dummy, minleadtime_dummy, maxleadtime_dummy, totalvalues_dummy] = await fetchkanbaninfo()
        kanbaninfos.value = kanbaninfos_dummy
        materialfilteroptions.value = materialfilteroptions_dummy
        loopfilteroptions.value = loopfilteroptions_dummy
        monthselectoptions.value = monthselectoptions_dummy
        avgleadtime.value = avgleadtime_dummy
        minleadtime.value = minleadtime_dummy
        maxleadtime.value = maxleadtime_dummy
        totalvalues.value = totalvalues_dummy
    } catch(error){
        console.error(error)
        ElMessage(`Error: ${error}`)
    } finally{
        loading.close()
    }
}

async function renewkanbandatafromsource(){
    await updatekanbandatabase()
    await getkanbaninfo(materialfilter.value, loopfilter.value, sorftfor.value)
}

function changelanguagesettings(language){
    ElMessage(language)
}

function changefetchintervalsettings(interval){
    ElMessage(interval)
}

function changeviewmodesettings(mode){
    ElMessage(mode)
}

</script>

<style scoped>
.timelineelement{
    height: 20px; 
    font-size: 12px; 
    background-color: rgb(50, 50, 50); 
    border-left: 1px solid white;
}
.test{
    background-color: rgb(50, 50, 50);
}
.uploadicon{
    position: absolute; 
    right: 32px; 
    font-size: 25px; 
    margin-top: 4px; 
    cursor: pointer;
    border-radius: 10px;
    color: black;
    z-index: 3;
    padding: 10px;
    background-color: rgba(255, 255, 255, 0);
}
.uploadicon:hover{
    color: rgb(0, 157, 255);
    transition: color 0.3s ease, background-color 0.3s ease;
    background-color: rgba(240, 248, 255, 0.488);
}
.activeelement{
    box-shadow: inset 0 0 10px 5px rgba(0, 255, 42, 0.5)
}
.inactiveelement{
    box-shadow: inset 0 0 5px 1px rgba(255, 0, 0, 0.5);
}
.closeicon{
    color: black;
    cursor: pointer;
    transition: color 0.3s ease;
}
.closeicon:hover{
    color: red;
    transition: color 0.3s ease;
}

.materialelement{
    background-color: rgba(128, 128, 128, 0.2);
    padding: 4px;
    border-radius: 5px;
    border: 1px solid black;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.materialelement:hover{
    background-color: rgba(128, 128, 128, 0.4);
}

.timebar{
    background-color: lightblue;
    padding-top: 3px;
    padding-bottom: 3px;
    border-radius: 4px;
    max-height: 17px;
    transition: background-color 0.2s ease;
}
.timebar:hover{
    background-color: rgba(173, 216, 230, 0.7)
}
.timebarxaxiselement{
    background-color: rgb(56, 99, 255); 
    border: 1px solid black; 
    width: 100px;
}
.ganttchartcontainer{
    display: flex;
    flex-direction: column;
    gap: 1px;
}
</style>
