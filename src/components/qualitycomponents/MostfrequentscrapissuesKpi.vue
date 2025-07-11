<template>

    <div class="elcardalternative" style="width: 100%; height: 100%; padding: 10px; box-sizing: border-box;" ref="costchangeref">

      <div class="heading" :style="{transform: dataavailable ? 'translateY(0px)' : 'translateY(5px)'}">
        <label>{{ title }}</label>
        <el-tooltip content="Compared to previous month">
          <el-icon class="infoicon"><InfoFilled /></el-icon>
        </el-tooltip>
      </div>
      
      <div class="cardbackground" :style="{transform: dataavailable ? 'translateY(0px)' : 'translateY(10px)'}">
        <div v-if="!dataavailable">No data for previous month available</div>          
        <div v-else class="kpielement" v-for="(element,index) in threemostfrequentscrapissuecauses" :key="index">
          <div style="font-weight: 600;">{{ element.issue }}</div>
          <div>{{ changeinpercent(element.costchange) }}</div>
        </div>
      </div>

    </div>
  
</template>

<script setup>
import { fetchmostfrequentscrapissuecauses } from '@/services/qualitydataapis';
import { onMounted, ref, watch } from 'vue';
import { ElLoading } from 'element-plus';
import { InfoFilled } from '@element-plus/icons-vue';
import { materialselectionstore, selectedmonthstore } from '@/stores/filterinformationstore';
import { renameinfostorage } from '@/stores/renameinfostore';

const renameinfooptions = renameinfostorage()

const title = ref('Trend of most expensive issues')

const materialselectionoptions = materialselectionstore()
const selectedmonthoptions = selectedmonthstore()

onMounted(async () =>{
  title.value = renameinfooptions.getcomponentrenaming('trendofmostexpensiveissues')
  await loaddata()
})

watch(
  () => [materialselectionoptions.selectedmaterials, selectedmonthoptions.selectedmonthforvisualization],
  async () =>{
    await loaddata()
})

const costchangeref = ref(null)
const mostfrequentscrapissuecauses = ref([])
const threemostfrequentscrapissuecauses = ref([])

const dataavailable = ref(true)

async function loaddata(){
  const loader = ElLoading.service({
      target: costchangeref.value,
      text: 'Data is being loaded',
      background: 'rgba(255, 255, 255, 0.7)'
  })
  try{
      mostfrequentscrapissuecauses.value = await fetchmostfrequentscrapissuecauses()
      dataavailable.value = true;
      for(let i = 0; i < 3; i++){
        threemostfrequentscrapissuecauses.value = mostfrequentscrapissuecauses.value.slice(0, 3).filter(el => el !== undefined)
      }
      if(threemostfrequentscrapissuecauses.value[0]?.costchange == null){
        dataavailable.value = false;
      }
  } catch(error){
      console.error(error)
  } finally{
      loader.close()
  }
}

function changeinpercent(value){
  if(value === null || isNaN(value)) return ' '
  return `${(value * 100).toFixed(2)}%`
}

</script>

<style scoped>
.cardbackground{
  border: 1px solid #ddd;
  background-color: white;
  display: flex;
  justify-content: space-evenly;
  padding: 8px;
  gap: 15px;
  position: relative;
  border-radius: 4px;
  transition: background-color 0.3s ease;
  cursor: pointer;
  margin-top: 5px;
}

.cardbackground:hover{
  background-color: #ddd;
}
.kpielement{
  border-radius: 4px;
  padding: 5px;
  width: 120px; 
  background-color: #5C7BD9;
  transform: scale(1);
  transition: transform 0.3s ease;
}
.kpielement:hover{
  transform: scale(1.05);
  transition: transform 0.3s ease;
}
.heading{
  /* font-size: 1.1em;
  font-weight: bold;
  color: #555;  */
  margin-top: 5px;
  font-weight: 600;
}
.infoicon{
  color: lightgray; 
  font-size: small;
  margin-left: 3px;
  transition: color 0.3s ease, transform 0.3s ease;
}
.infoicon:hover{
  color: darkgray;
  /* font-size: medium; */
  transform: scale(1.2);
  cursor: pointer;
}
</style> 


