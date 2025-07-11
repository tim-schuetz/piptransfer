<template>
    <div class="elcardalternative" style="width: 100%; height: 100%; box-sizing: border-box; display: flex; flex-direction: column">
        <div style="font-weight: 600;">{{ title }}</div>
        <div class="elcardalternative" style="margin-top: 15px; color: #666; padding: 13px">Product filter</div>
        <el-select filterable v-model="selectedproductforspoolfilter">
            <el-option v-for="(product, index) in uniqueproductlist" :key="index" :value="product">{{ product }}</el-option>
            <el-option value="all">All</el-option>
        </el-select>
        <el-button type="primary" @click="applyfilterchangestostore" style="margin-top: 5px;">Apply</el-button>
    </div>

</template>

<script setup>
import { fetchproductlistforspoolscrap } from '@/services/qualitydataapis';
import { ref, onMounted } from 'vue'
import { spoolscrapfilteroptionsstore } from '@/stores/filterinformationstore';
import { renameinfostorage } from '@/stores/renameinfostore';

const renameinfoptions = renameinfostorage()

const title = ref('Spool scrap filter options')

const spoolscrapfilteroptions = spoolscrapfilteroptionsstore()

const selectedproductforspoolfilter = ref('')
const uniqueproductlist = ref([])

function applyfilterchangestostore(){
    spoolscrapfilteroptions.selectedproductforspoolfilter = selectedproductforspoolfilter.value
}

onMounted( async() =>{
    title.value = renameinfoptions.getcomponentrenaming('spoolscrapfilteroptions')
    uniqueproductlist.value = (await fetchproductlistforspoolscrap()).filter(p => p != null)
})

</script>

<style scoped>

</style>