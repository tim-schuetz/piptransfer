<template>

    <div class="header" style="position: fixed; top:0px; left:0px; background-color: aquamarine; height: 60px; width: 100vw; display: flex; justify-content: center; align-items: center;">
        <h1>Kanban Lead Time Analysis Dashboard</h1>
        <div class="uploadicon" @click="renewkanbandatafromsource">
            <el-tooltip content="renew data from source">
                <el-icon class="iconhover">
                    <Refresh />
                </el-icon>
            </el-tooltip>
        </div>
    </div>

    <div class="maincontainer">

        <div class="parameterandkpisidebar">
            <div class="leftcol" style="width: 250px; padding: 10px; background-color: #f8f9fa; border-right: 1px solid #ddd; overflow-y: auto;"> <!--width: 220px-->
                <div v-if="!showkpioverview"><FilterOptions @switchbetweenkpifilters="executeswitchbetweenkpifilters" /></div>
                <div v-else><KpiOverview @switchbetweenkpifilters="executeswitchbetweenkpifilters" /></div>
            </div>
        </div>

        <div class="visualscontainer">

            <div class="visuals">

                <div class="visual" :class="showmainvisualfullscreen ? 'mainvisualexpanded' : 'mainvisual'" style="border: none;">
                    <LeadtimeByMaterialBarChart :key="showmainvisualfullscreen" />
                    <el-icon v-if="!showmainvisualfullscreen" class="iconhover expandicon" @click="showmainvisualfullscreen=true"><FullScreen /></el-icon>
                    <el-icon v-else class="iconhover expandicon" style="color: black;" @click="showmainvisualfullscreen=false"><Close /></el-icon>
                </div>
                <div class="sidevisualcontainer">
                    <div class="sidevisual sidevisualone visual">
                        <label>Bar Chart mit Durchlaufzeit einzelner Aufträge. Nach Dauer der Durchlaufzeit absteigend sortiert</label>
                        <label>Dort soll es dann einen Button geben (links oben im Visual), wo man die Aufträge als Rohformat ansehen kann</label>
                    </div>
                    <div class="sidevisual sidevisualtwo visual">
                        <label>Balkendiagramm vertikal mit Balken in verschiedenen Höhen und Grün- bzw. Rottönen je nach Durchlaufzeit. Entsprechend der vom Nutzer vorgegebenen kritischen Durchlaufzeit. Zeitlich sortiert mit dem neuesten Auftrag oben</label>
                    </div>
                    <div class="sidevisual sidevisualthree visual">
                        <label>Vertikales Diagramm in denen die einzelnn Tage/Monate, je nach Nutzerwunsch übereinander zu sehen mit ihrer durchschnittlichen Durchlaufzeit und entsprechenden Länge der Balken</label>
                    </div>
                </div>

                <!-- <div>Irgendwo noch ein Feld einbauen, bei dem man eine Auftragsnummer in der Suchleiste eingeben kann und dann alle Infos zu diesem Auftrag (alles was in Tabelle und ggf. auch noch Daten von Odata) als neues Fenster sieht. Außerdem soll im aktuell ausgewählten Visual dieser Auftrag farblich hervorgehoben werden</div> -->

            </div>

        </div>
    </div>

</template>

<script setup>
import { updatekanbandatabase } from '@/services/kanbandataapis';
import { FullScreen, Refresh, Close } from '@element-plus/icons-vue'
// import { Upload } from '@element-plus/icons-vue'
import LeadtimeByMaterialBarChart from '@/components/kanbancomponents/LeadtimeByMaterialBarChart.vue';
import { ref } from 'vue'
import FilterOptions from '@/components/kanbancomponents/FilterOptions.vue';
import KpiOverview from './KpiOverview.vue';

const showkpioverview = ref(false)

function executeswitchbetweenkpifilters(){
    showkpioverview.value = !showkpioverview.value
}

const showmainvisualfullscreen = ref(false)

function renewkanbandatafromsource(){
    updatekanbandatabase()
}

// bei dem Visual wo man die einzelnen Aufträge in Durchlaufzeit als Barchart sieht, noch einen Pfeil nach rechts oder so als Button und wenn man den klickt, dann sieht man den Durchlauf des Teils an den Maschinen grafisch durch den Workshop anhand der Komponente mit dem Model. Dazu eine Animation mit Kameraführung machen und bei jeder betroffnenen Maschine so ein weißes Kärtchen schwebend dran, wo Leadtime:  (100%) steht. Bai Jie dann sagen, dass hier genaue Daten dann halt erst möglich sind, wenn dei Maschinen angebunden sind und die Rückmeldungen aus dem SAP ausgelesen werden können.

// änderung: Beim ersten Barchart soll man nach Materialnummer, nach Kanbanidnummer oder nach Ordernummer wählen können danach wird das dann angezeigt. Die Rohdaten nochmal als eigenes Fenster auslagern

</script>

<style scoped>
.maincontainer{
    position: fixed;
    top: 60px;
    height: calc(100vh - 60px);
    left: 0px;
    width: 100vw;
    display: flex;
    background-color: aliceblue;
}
.parameterandkpisidebar{
    width: 18%;
    height: 100%;
    display: flex;
    flex-direction: column;
    border-right: 1px solid #ddd;
}
.visualscontainer{
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.visuals{
    height: 80%;
    width: 95%;
    display: flex;
    gap: 15px;
}
.mainvisual{
    width: 75%;
    height: 100%;
    border-radius: 10px;
    border: 2px solid #ddd;
    position: relative;
}
.mainvisualexpanded{
    position: fixed;
    left: 10px;
    top: 10px; 
    width: calc(100vw - 20px);
    height: calc(100vh - 20px);
}
.sidevisualcontainer{
    width: 25%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.sidevisual{
    width: 100%;
    height: 30%;
    border-radius: 10px;
    border: 2px solid #ddd;
}


.visual{
    cursor: pointer;
    transition: transform 0.3s ease;
}
.visual:hover{
    transform: scale(1.01);
}

.expandicon{
    position: absolute; 
    top: 5px; 
    right: 5px; 
    font-size: large; 
    color: grey;
    transition: color 0.3s ease, opacity 0.3s ease;
    opacity: 0;
}
.expandicon:hover{
    color: rgb(0, 157, 255);
    transition: color 0.3s ease;
}
.mainvisual:hover .expandicon{
    opacity: 1;
    transition:  opacity 0.3s ease;
}
.mainvisualexpanded:hover .expandicon{
    opacity: 1;
    transition:  opacity 0.3s ease;
}

.uploadicon{
    position: absolute;
    right: 30px;
    top: 15px;
    font-size: 24pt;
}

</style>
