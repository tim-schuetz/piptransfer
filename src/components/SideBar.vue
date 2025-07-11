<template>

    <div style="height: 100vh; display: flex; width: max-content; position: fixed; left:0px; z-index: 999;">
        <el-aside :class="sidebarUnfolded ? 'folded' : 'unfolded'" style="transition: left ease-in-out 0.3s;">
            <el-menu background-color="#2f3b52" text-color="#fff" active-text-color="#ffd04b" default-active="1">
                <router-link to="/icoperformanceview">
                    <el-menu-item index="1"><span>ICO Performance Dashboard</span></el-menu-item>
                </router-link>
                <router-link to="/kanbanview">
                    <el-menu-item index="2"><span>Kanban Leadtime Overview</span></el-menu-item>
                </router-link>
                <router-link to="/qualityview">
                    <el-menu-item index="3"><span>Quality Information</span></el-menu-item>
                </router-link>
            </el-menu>
            <div class="buttonHolder" @click="sidebarUnfolded = !sidebarUnfolded" :class="sidebarUnfolded ? 'buttonFolded' : 'buttonUnfolded'">
                <div v-if="!sidebarUnfolded" class="fold-button">x</div>
                <ArrowRight v-else width="20px" height="20px"/>
            </div>
        </el-aside>
    </div>

</template>

<script setup>
import { ArrowRight } from '@element-plus/icons-vue'
import { ref } from 'vue'

const sidebarUnfolded = ref(false)

</script>

<style scoped>
#app {
display: flex;
height: 100vh;
background-color: #f4f4f4;
overflow-x: hidden;
width: max-content;
}

a {
  text-decoration: none;
  color: inherit;
}

a:hover {
  color: inherit;
}

.el-aside {
background-color: #1f2a38;

}
.folded{
    position: fixed; 
    top:0px; 
    left:-250px; 
    width: max-content; 
    height: 100vh;
    z-index: 999;
}
.unfolded{
    position: fixed; 
    top:0px; 
    left:0px; 
    width: max-content; 
    height: 100vh;
    z-index: 998;
}
.buttonUnfolded{
    position: absolute; 
    top: 13px; 
    right: 15px; 
    color: #fff; 
    padding: 6px 10px; 
    border-radius: 5px; 
    z-index: 998;
    cursor: pointer;
    background-color: rgb(255, 255, 255, 0.2);;
}
.buttonFolded{
    position: fixed; 
    top: 13px; 
    left: 10px; 
    color: #000000; 
    padding: 4px 6px; 
    border-radius: 5px; 
    z-index: 998;
    background-color: rgb(24, 4, 109, 0.05);
    cursor: pointer;
}
.buttonFolded:hover{
    background-color: rgb(24, 4, 109, 0.3);
}
.buttonUnfolded:hover{
    background-color: rgb(255, 255, 255, 0.5);
}
</style>