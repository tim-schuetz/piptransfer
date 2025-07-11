<template>

    <div style="position: fixed; left:50vw; top:50vh; width: 250px; transform: translate(-50%, -50%); display: flex; flex-direction: column; z-index: 999; border: 2px solid black; border-radius: 10px; padding-left: 15px; padding-right: 15px; padding-bottom: 15px; padding-top: 0px; background-color: white;">

        <div style="font-weight: 600; font-size: 20px; margin: 8px;">Settings</div>
        <el-card>
            <label style="font-weight: 600;">Language</label>
            <el-select v-model="language" @change="languagechange(language)" style="margin-top: 5px;">
                <el-option value="chinese">Chinese</el-option>
                <el-option value="english">English</el-option>
            </el-select>
        </el-card>

        <el-card>
            <label style="font-weight: 600;">Refresh rate</label>
            <el-select v-model="refreshrate" @change="fetchintervalchange(refreshrate)" style="margin-top: 5px;">
                <el-option value="hourly">Hourly</el-option>
                <el-option value="daily">Daily</el-option>
                <el-option value="weekly">Weekly</el-option>
            </el-select>
            <el-input v-model="refreshtime" style="width: 100%"></el-input>
        </el-card>

        <el-card>
            <label>Light layout</label>
            <el-switch v-model="lightlayout" style="margin-left: 10px;" @change="viewmodechange(lightlayout)"></el-switch>
        </el-card>

        <el-icon class="closebutton" @click="closesettingswindow">
            <close-bold />
        </el-icon>
    
    </div>

    <div style="z-index: 10; position: fixed; top:0px; left:0px; width: 100vw; height: 100vh; background-color: rgba(128, 128, 128, 0.3);"></div>

</template>

<script setup>
/* global defineEmits */
import { ref } from 'vue'
import { CloseBold } from '@element-plus/icons-vue'

const refreshtime = ref('08:00:00')

const language = ref('English')
const refreshrate = ref('Daily')
const lightlayout = ref(true)

const emit = defineEmits(['removesettingswindow', 'changelanguage', 'changefetchinterval', 'changeviewmode'])

function closesettingswindow(){
    emit('removesettingswindow')
}

function languagechange(language){
    emit('changelanguage', language)
}

function fetchintervalchange(interval){
    emit('changefetchinterval', interval)
}

function viewmodechange(mode){
    emit('changeviewmode', mode)
}

</script>

<style scoped>
.closebutton{
    position: absolute;
    top: 8px;
    right: 8px;
    cursor: pointer;
    transition: color 0.3s ease;
}
.closebutton:hover{
    color: red;
    transition: color 0.3s ease;
}

</style>
