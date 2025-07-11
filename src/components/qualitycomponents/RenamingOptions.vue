<template>
    <div class="background"></div>
    <div class="container elcardalternative">
        <div style="position: absolute; top: 10px; right: 10px;" class="iconhover" @click="closewindowfunction"><el-icon><Close /></el-icon></div>
        <div class="heading">Component Renaming Options</div>
        <div v-for="(component, index) in componentrenamings" :key="index" class="renameoptionelement">
            <div style="display: flex; gap: 7px; width: 45%">
                <div style="color: #121212">Original name:</div>
                <div>{{ component.originalname }}</div>
            </div>
            <div style="display: flex; gap: 7px; width: 45%">
                <div style="margin-left: 10px; color: #121212">Given name:</div>
                <div>{{ component.givenname ? component.givenname : "none" }}</div>
            </div>
            <div style="width: 10%; cursor: pointer; display: flex; justify-content: flex-end;" class="iconhover" @click="showeditwindowfunction(component.originalname, component.givenname, 'component')">
                <el-icon><Edit /></el-icon>
            </div>
        </div>

        <div class="heading">Material Renaming Options</div>
        <div v-for="(renaming, index) in materialrenamings" :key="index" class="renameoptionelement">
            <div style="display: flex; gap: 7px; width: 45%">
                <div style="color: #121212">Original name:</div>
                <div>{{ renaming[0] }}</div>
            </div>
            <div style="display: flex; gap: 7px; width: 45%">
                <div style="margin-left: 10px; color: #121212">Given name:</div>
                <div>{{ renaming[1] ? renaming[1] : "none" }}</div>
            </div>
            <div style="width: 10%; cursor: pointer; display: flex; justify-content: flex-end;" class="iconhover" @click="showeditwindowfunction(renaming[0], renaming[1], 'material')">
                <el-icon><Edit /></el-icon>
            </div>
        </div>

        <div class="heading">Supplier Renaming Options</div>
        <div v-for="(supplier, index) in supplierrenamings" :key="index" class="renameoptionelement">
            <div style="display: flex; gap: 7px; width: 45%">
                <div style="color: #121212">Original name:</div>
                <div>{{ supplier.fullname }}</div>
            </div>
            <div style="display: flex; gap: 7px; width: 45%">
                <div style="margin-left: 10px; color: #121212">Given name:</div>
                <div>{{ supplier.shortname ? supplier.shortname : "none" }}</div>
            </div>
            <div style="width: 10%; cursor: pointer; display: flex; justify-content: flex-end;" class="iconhover" @click="showeditwindowfunction(supplier.fullname, supplier.shortname, 'supplier')">
                <el-icon><Edit /></el-icon>
            </div>
        </div>

    </div>

    <RenameWindow v-if="showeditwindow" 
        :originalname="originalnameref" :givenname="givennameref" 
        @closerenamewindow="closeeditwindow" @newgivennameassigned="assignname"             
        />

</template>

<script setup>
import { Close, Edit } from '@element-plus/icons-vue'
import { defineEmits, onMounted, ref } from 'vue';
import { renameinfostorage } from '@/stores/renameinfostore';
import RenameWindow from './RenameWindow.vue';

const showeditwindow = ref(false)
const originalnameref = ref('')
const givennameref = ref('')
const changetype = ref('')

function showeditwindowfunction(originalname, givenname, changetyperef){
    showeditwindow.value = true;
    originalnameref.value = originalname
    givennameref.value = givenname
    changetype.value = changetyperef
}

function assignname(newgivenname){
    if(changetype.value == "material"){
        renamingoptions.changematerialrenaming(originalnameref.value, newgivenname)
    } else if (changetype.value == "component"){
        renamingoptions.changecomponentname(originalnameref.value, newgivenname)
    } else if (changetype.value == "supplier"){
        renamingoptions.changesuppliershortname(originalnameref.value, newgivenname)
    }
}

function closeeditwindow(){
    showeditwindow.value = false
    originalnameref.value = ''
    givennameref.value = ''
    changetype.value = ''
}

const renamingoptions = renameinfostorage()

const componentrenamings = ref([])
const supplierrenamings = ref([])
const materialrenamings = ref([])

onMounted( ()=>{
    componentrenamings.value = renamingoptions.componentrenamings;
    supplierrenamings.value = renamingoptions.supplierrenamings;
    materialrenamings.value = renamingoptions.materialrenamings;
})


const emits = defineEmits(['closewindow'])

function closewindowfunction(){
    closeeditwindow() //damit das Unterfenster nicht aufbleibt, wenn das große Fenster geschlossen wird
    emits('closewindow')
}

</script>

<style scoped>
.background{
    position: fixed;
    left: 0px; 
    top: 0px;
    height: 100vh;
    width: 100vw;
    background-color: rgba(255, 255, 255, 0.7);
    z-index: 998;
}
.container{
    width: 60vw;
    height: 80vh;
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    z-index: 999;
    align-items: center;
    overflow-y: scroll;
    overflow-x: hidden;
}
.heading{
    font-size: larger; 
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 20px;
}
.renameoptionelement{
    padding: 8px;
    border-bottom: 1px solid grey;
    transition: background-color 0.3s ease, transform 0.3s ease;
    display: flex;
    gap: 3px;
    width: 100%;
}
.renameoptionelement:hover{
    background-color: rgba(140, 140, 140, 0.7);
    transform: scale(1.01);
}

</style>

