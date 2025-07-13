<template>
  <div class="filtercardcontainer">

    <div class="headingcontainer">
      <label>Kanban KPI overview</label>
      <div class="switchiconcontainer">
        <el-tooltip content="Switch to filter options">
          <el-icon class="iconhover" @click="switchbetweenkpifilters"><Switch /></el-icon>
        </el-tooltip>
      </div>
    </div>

    <!-- KPI Grid -->
    <div class="kpicardgrid">
      <div class="kpicard" style="background-color: #e0f7fa;">
        <el-icon class="kpiicon"><Clock /></el-icon>
        <div class="kpinumber">{{ avgleadtime }}</div>
        <div class="kpilabel">Ø Leadtime</div>
      </div>

      <div class="kpicard" style="background-color: #ffebee;">
        <el-icon class="kpiicon"><ArrowUpBold /></el-icon>
        <div class="kpinumber">{{ minleadtime }}</div>
        <div class="kpilabel">Longest Leadtime</div>
      </div>

      <div class="kpicard" style="background-color: #e8f5e9;">
        <el-icon class="kpiicon"><ArrowDownBold /></el-icon>
        <div class="kpinumber">{{ maxleadtime }}</div>
        <div class="kpilabel">Shortest Leadtime</div>
      </div>
    </div>

    <el-card v-if="filtersactive" class="filterinfo" shadow="hover">
      <el-icon style="margin-right: 5px;"><WarnTriangleFilled /></el-icon>
      <span>Filters are in place</span>
    </el-card>

    <el-card v-else class="filterinfo" shadow="hover">
      <span>No filters in place</span>
    </el-card>

  </div>
</template>

<script setup>
import { Switch, WarnTriangleFilled } from '@element-plus/icons-vue'
import { kanbanfilterinfostore } from '@/stores/kanbanfilterinformationstore';
import { onMounted, ref, defineEmits } from 'vue';
import { getkpivalues } from '@/services/kanbandataapis';

import { Clock, ArrowUpBold, ArrowDownBold } from '@element-plus/icons-vue'


const emits = defineEmits(['switchbetweenkpifilters'])

function switchbetweenkpifilters(){
    emits('switchbetweenkpifilters')
}

const kanbanfilterinfooptions = kanbanfilterinfostore()

const filtersactive = ref(false)

const minleadtime = ref(0)
const maxleadtime = ref(0)
const avgleadtime = ref(0)

onMounted( async ()=>{
    filtersactive.value = kanbanfilterinfooptions.isfilteractive()
    const data = await getkpivalues()
    minleadtime.value = Number(data.minleadtime).toFixed(2)
    maxleadtime.value = Number(data.maxleadtime).toFixed(2)
    avgleadtime.value = Number(data.avgleadtime).toFixed(2)
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
    transform: translate(10px); 
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
    transform: translate(0px);
    transition: transform 0.3s ease;
}
.filtercardcontainer:hover .switchiconcontainer{
    opacity: 1;
    transition: opacity 0.3s ease;
}
.sorticon{
    transform: translate(3px, -2px) rotate(90deg) scaleX(-1);
}



.kpicardgrid {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 15px;
  margin: 20px 0;
  width: 100%;
}

.kpicard {
  flex: 1;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.kpicard:hover {
  transform: translateY(-5px);
}

.kpiicon {
  font-size: 28px;
  margin-bottom: 8px;
  color: #333;
}

.kpinumber {
  font-size: 26px;
  font-weight: bold;
}

.kpilabel {
  font-size: 14px;
  color: #555;
  margin-top: 4px;
}

.filterinfo {
  /* margin-top: 10px; */
  text-align: center;
  font-weight: 500;
  width: 100%;
}

</style>
