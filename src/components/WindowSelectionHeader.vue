<template>
    <div style="display: flex;">

        <div class="elcardalternative cardtitle" @click="passselectedwindow('icoperformanceoverview')" style="padding-top: 10px; padding-bottom: 10px;" :style="{fontWeight: icoperformanceoverviewvisible ? '600' : '400'}">ICO Performance overview</div>
        <div class="elcardalternative cardtitle" @click="passselectedwindow('kanbanleadtimeanalysis')" style="padding-top: 10px; padding-bottom: 10px;" :style="{fontWeight: kanbanleadtimeanalysisvisible ? '600' : '400'}">Kanban lead time analysis</div>
        <div class="elcardalternative cardtitle" @click="passselectedwindow('qualitydashboard')" style="padding-top: 10px; padding-bottom: 10px;" :style="{fontWeight: qualitydashboardvisible ? '600' : '400'}">Quality Dashboard</div>

    </div>

</template>

<script setup>
import { ElMessage } from 'element-plus'
import { ref, defineEmits } from 'vue'

const icoperformanceoverviewvisible = ref(true)
const kanbanleadtimeanalysisvisible = ref(false)
const qualitydashboardvisible = ref(false)

const emits = defineEmits(['activewindow'])

function passselectedwindow(selectedwindow){
    ElMessage(selectedwindow)
    if(selectedwindow == 'qualitydashboard'){
        qualitydashboardvisible.value = true
        kanbanleadtimeanalysisvisible.value = false
        icoperformanceoverviewvisible.value = false
    } else if (selectedwindow == 'kanbanleadtimeanalysis'){
        qualitydashboardvisible.value = false
        kanbanleadtimeanalysisvisible.value = true
        icoperformanceoverviewvisible.value = false
    } else{
        qualitydashboardvisible.value = false
        kanbanleadtimeanalysisvisible.value = false
        icoperformanceoverviewvisible.value = true
    }
    emits('transmitwindowchange', selectedwindow)
}

</script>

<style scoped>
.cardtitle {
  font-size: 1.1rem; /* ca. 20px */
  font-weight: 400;
  margin-bottom: 12px;
  color: #2c3e50; /* dunkles Grau für Klarheit */
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
  letter-spacing: 0.3px;
  cursor: pointer;
}
</style>


