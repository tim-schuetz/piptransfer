<template>

  <div class="elcardalternative" style="width: 100%; height: 100%; padding: 10px; box-sizing: border-box;" ref="costchangeref">
      
    <div class="heading">
      <label>{{ title }}</label>
      <el-tooltip content="Compared to previous month">
        <el-icon class="infoicon"><InfoFilled /></el-icon>
      </el-tooltip>
    </div>

    <div style="cursor: pointer;">
      <div class="cardbackground">
        <div v-if="nodataforpreviousmonth">No data for previous month available</div>
        <div v-else class="kpielement" v-for="(element,index) in firsttrhee_methodcostmonhtlycomparison" :key="index">
          <div style="font-weight: 600;">{{ element.method }}</div>
          <div>{{ changeinpercent(element.costchange) }}</div>
        </div>
      </div>
    </div>

  </div>

</template>

<script setup>
import { fetchhistoric_Worstmethodsforspoolscrap } from '@/services/qualitydataapis';
import { onMounted, ref, watch } from 'vue';
import { ElLoading } from 'element-plus';
import { selectedmonthstore } from '@/stores/filterinformationstore';
import { InfoFilled } from '@element-plus/icons-vue';
import { renameinfostorage } from '@/stores/renameinfostore';

const renameinfoptions = renameinfostorage()

const title = ref('Change of Scrap per Method')

const selectedmonthinfo = selectedmonthstore()

watch(
  () => selectedmonthinfo.selectedmonthforvisualization, 
  async () =>{
  await loaddata()
})

const costchangeref = ref(null)
const methodcostmonhtlycomparison = ref([])
const firsttrhee_methodcostmonhtlycomparison = ref([])
const nodataforpreviousmonth = ref(false)

onMounted(async () =>{
  await loaddata()
  title.value = renameinfoptions.getcomponentrenaming('changeofscrappermethod')
})

async function loaddata(){
  const loader = ElLoading.service({
      target: costchangeref.value,
      text: 'Data is being loaded',
      background: 'rgba(255, 255, 255, 0.7)'
  })
  try{
      methodcostmonhtlycomparison.value = await fetchhistoric_Worstmethodsforspoolscrap(selectedmonthinfo.selectedmonthforvisualization)
      firsttrhee_methodcostmonhtlycomparison.value = methodcostmonhtlycomparison.value.slice(0,3)
      nodataforpreviousmonth.value = false;
      for(const element of firsttrhee_methodcostmonhtlycomparison.value){
        if(element.costchange == null){
          nodataforpreviousmonth.value = true;
        }
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
.cardbackground{
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  display: flex;
  justify-content: space-evenly;
  padding: 8px;
  gap: 15px;
  position: relative;
  margin-top: 15px;
  transition: background-color 0.3s ease;
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
</style> 


