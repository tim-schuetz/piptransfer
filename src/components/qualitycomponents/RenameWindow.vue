<template>
    <div class="elcardalternative containerneu">

        <div style="position: absolute; top: 5px; right: 5px">
            <el-icon class="iconhover" @click="closerenamewindow"><Close /></el-icon>
        </div>
        <div style="font-weight: 600; margin-bottom: 7px;">{{ originalname }}</div>
        <div style="display: flex; width: 100%;">
            <label class="elcardalternative" style="width: 26%; white-space: nowrap; padding-bottom: 6px; padding-top: 7px;">Previous name:</label>
            <label class="elcardalternative" style="width: 64%; padding-bottom: 6px; padding-top: 7px;">{{ givenname ? givenname : "No name set" }}</label>
        </div>
        <div style="display: flex; width: 100%;">
            <label class="elcardalternative" style="width: 30%; white-space: nowrap; padding-bottom: 5px; padding-top: 7px;">Set new name:</label>
            <el-input @keyup.enter="newgivennameassignedfunction" v-model="newgivenname"></el-input>
            <el-button type="primary" @click="newgivennameassignedfunction">Apply</el-button>
        </div>

    </div>

</template>

<script setup>
import { defineEmits, defineProps, ref } from 'vue';
import { Close } from '@element-plus/icons-vue'

const newgivenname = ref('')

defineProps({
    originalname: {
        type: String,
        required: true
    },
    givenname: {
        type: String,
        required: true
    }
})

const emits = defineEmits(['closerenamewindow', 'newgivennameassigned'])

function closerenamewindow(){
    emits('closerenamewindow')
}

function newgivennameassignedfunction(){
    emits('newgivennameassigned', newgivenname.value)
    emits('closerenamewindow')
}

</script>

<style scoped>
.containerneu{
    position: fixed;
    left: 50vw;
    top: 50vh;
    transform: translate(-50%, -50%);
    display: flex; 
    flex-direction: column; 
    gap: 5px;
    overflow-y: hidden;
    z-index: 1000;
}
</style>
