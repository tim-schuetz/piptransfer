<template>
    <el-card class="maincontainer" shadow="hover">
        <div style="display: flex; gap: 3px">
            <el-select v-model="escalationoption">
                <el-option value="maildelivery" label="Mail delivery"></el-option>
            </el-select>
            <el-button type="primary" style="border-radius: 50%; padding: 7px">
                <el-icon @click="addmaildeliveroption"><Plus /></el-icon>
            </el-button>
        </div>
        <div style="min-height: 100px; display: flex; flex-direction: column; gap: 5px; align-items: flex-start; margin-top: 7px;">
            <div v-for="(entry, index) in maildeliveroptions" :key="index" style="display: flex; gap: 5px; align-items: center;">

                <div class="maildeliveryoptionelement">
                    <div>To:</div>
                    <el-input v-model="entry.to" class="mailelementinput"></el-input>
                    <div>Threshold:</div>
                    <el-input v-model="entry.threshold" type="number" style="width: 200px;" class="mailelementinput"></el-input>
                    <div>Content:</div>
                    <el-input v-model="entry.customizedContent" class="mailelementinput"></el-input>
                </div>

                <el-button class="deleteicon" type="danger">
                    <el-icon @click="removemaildeliveroption(index)"><Delete /></el-icon>
                </el-button>

            </div>
        </div>

        <el-button v-if="maildeliveroptions.length === 0" type="primary" style="width: 100%; margin-top: 5px;">View previous actions</el-button>
        <el-button v-else type="primary" style="width: 100%; margin-top: 5px;">Save Actions</el-button>

    </el-card>
</template>

<script setup>
import { Plus, Delete } from '@element-plus/icons-vue'
import { ref } from 'vue'

const escalationoption = ref('maildelivery')

const maildeliveroptions = ref([])

function addmaildeliveroption(){
    maildeliveroptions.value.push({to: "", threshold: 30, customizedContent: ""})
}

function removemaildeliveroption(index){
    maildeliveroptions.value.splice(index, 1)
}

</script>

<style scoped>
.maincontainer{
    /* position: fixed;
    top: 50vh;
    left: 50vw;
    transform: translate(-50%, -50%); */
    display: flex;
    flex-direction: column;
}
.heading{
    font-weight: 600;
    margin-bottom: 7px;
    border-bottom: 1px solid #ddd;
}
.maildeliveryoptionelement{
    width: 100%;
    border: 1px solid #ddd;
    display: flex;
    align-items: center;
    border-radius: 2px;
    padding: 8px;
    width: 93%;
}
.deleteicon{
    border-radius: 50%; 
    padding: 7px;
    /* background-color: #EC4134; */
    /* color: white; */
}

.mailelementinput{
    height: 24px; 
    margin-right: 8px; 
    margin-left: 3px;
}

</style>

