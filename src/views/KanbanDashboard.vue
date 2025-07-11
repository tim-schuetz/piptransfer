<template>

    <div class="header" style="position: fixed; top:0px; left:0px; background-color: aquamarine; height: 60px; width: 100vw; display: flex; justify-content: center; align-items: center;">
        <h1>Kanban Lead Time Analysis Dashboard</h1>
        <div class="uploadicon" @click="renewkanbandatafromsource">
            <el-tooltip content="renew data from source">
                <el-icon style="z-index: 4;">
                    <Upload />
                </el-icon>
            </el-tooltip>
        </div>
    </div>

    <div class="maincontainer">
        <div class="parameterandkpisidebar">

        </div>
        <div class="visualscontainer">

            <div class="visuals">

                <div class="mainvisual visual">
                    <el-icon class="iconhover expandicon"><FullScreen /></el-icon>
                    <label>Hier ein Bar Chart mit Durchlaufzeit nach Materialnummern im Durchschnitt</label>
                </div>
                <div class="sidevisualcontainer">
                    <div class="sidevisual sidevisualone visual">
                        <label>Bar Chart mit Durchlaufzeit einzelner Aufträge</label>
                    </div>
                    <div class="sidevisual sidevisualtwo visual">
                        <label>Balkendiagramm mit Balken in verschiedenen Höhen und Grün- bzw. Rottönen je nach Durchlaufzeit. Entsprechend der vom Nutzer vorgegebenen kritischen Durchlaufzeit</label>
                    </div>
                    <div class="sidevisual sidevisualthree visual">
                        <label>Vertikales Diagramm in denen die einzelnn Tage übereinander zu sehen mit ihrer durchschnittlichen Durchlaufzeit und entsprechenden Länge der Balken</label>
                    </div>
                </div>

            </div>

        </div>
    </div>

</template>

<script setup>
import { updatekanbandatabase } from '@/services/kanbandataapis';
import { FullScreen } from '@element-plus/icons-vue'

function renewkanbandatafromsource(){
    updatekanbandatabase()
}

// bei dem Visual wo man die einzelnen Aufträge in Durchlaufzeit als Barchart sieht, noch einen Pfeil nach rechts oder so als Button und wenn man den klickt, dann sieht man den Durchlauf des Teils an den Maschinen grafisch durch den Workshop anhand der Komponente mit dem Model. Dazu eine Animation mit Kameraführung machen und bei jeder betroffnenen Maschine so ein weißes Kärtchen schwebend dran, wo Leadtime:  (100%) steht. Bai Jie dann sagen, dass hier genaue Daten dann halt erst möglich sind, wenn dei Maschinen angebunden sind und die Rückmeldungen aus dem SAP ausgelesen werden können.

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

</style>
