<template>
    <div class="scenecontainer" ref="scenecontainer"></div>
    
    <div class="machineinfopanel" :class="selectedobjectname ? 'infopanelvisible' : 'infopanelinvisible'">
        <div style="position: absolute; top: 8px; left: 15px">CP1908239</div>
        <div style="height: 20px;"></div>
        <div class="machineinfoitem">
            <label>设备状态</label>
            <label style="color: green;">运行中</label>
        </div>
        <div class="machineinfoitem">
            <label>任务单号</label>
            <label style="color: #A0D8F1;" ref="orderlabelref">{{ currentordernumber }}</label>
        </div>
        <div class="machineinfoitem">
            <label>预期的任务长短</label>
            <label style="color: #A0D8F1;" ref="orderlabelref">{{ currentorderplannedduration }} min</label>
        </div>
        <div class="machineinfoitem">
            <label>今日加工数量</label>
            <label style="color: #A0D8F1;" ref="todaysoutputlabelref">{{ todaysoutput }}</label>
        </div>
        <div class="machineinfoitem">
            <label>利用率</label>
            <label style="color: #A0D8F1;">75%</label>
        </div>
        <div class="machineinfoitem">
            <label>相关物料号</label>
            <label class="iconhover machinematerialslabel" @click="unhidemachinematerials">扩展</label>
        </div>
        <el-button @click="getrecentordersinfo(); selectedobjectname=false" style="margin-top: 5px;">Expand more detailed data</el-button>
        <div style="position: absolute; top:5px; right: 5px" @click="unfocusobject"><el-icon class="iconhover"><Close /></el-icon></div>
    </div>
    <div style="position: absolute; top: 10px; left: 50%; transform: translateX(-50%); background: rgba(0, 0, 0, 0.6); color: white; font-weight: bold; font-size: 1.2rem; padding: 12px 24px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.7); pointer-events: none; user-select: none; z-index: 1000;
        clip-path: polygon(
        0 15%,   /* links unten */
        0% 100%, /* links unten */
        100% 100%, /* rechts unten */
        100% 15%, /* rechts oben */
        85% 0%, /* schräge oben rechts */
        15% 0%  /* schräge oben links */
        );">
        <label v-if="!selectedobjectname">MOE-ICO 车间概览</label>
        <label v-else>{{ listedmachines[selectedobjectname].name }}</label>
    </div>

    <div class="machinematerialslist" :class="showmachinematerials ? 'materiallistvisible' : 'materiallistinvisible'">
        <div style="margin-bottom: 8px;">设备可加工物料号</div>
        <div v-if="!nomatchingmaterialsfound" style="padding-left: 20px; box-sizing: border-box; display: flex; flex-direction: column; height: 100vh; min-width: 100%; overflow-y: scroll; gap: 5px" ref="materialslistref">
            <div class="elcardalternative" style="color: black; padding: 10px; transform: translateX(-10px); cursor: pointer; z-index: 999;" v-for="(material, index) in selectedmachinematerialnumbers" :key="index">{{ material.materialnumber }}</div>
        </div>
        <div v-else style="margin-top: 30px;">No matching materialnumbers found</div>
        <div style="position: absolute; top: 5px; right: 5px" @click="showmachinematerials=false"><el-icon class="iconhover"><Close /></el-icon></div>
    </div>

    <div v-if="showmostrecentordersinfo" style="position: absolute; left: 50vw; top: 50vh; transform: translate(-50%, -50%); min-width: 70vw; min-height: 60vh; display: flex; align-items: center; justify-content: center; background-color: white; border-radius: 5px; z-index: 999;">
        <div ref="mostrecentordersinforef" style="height: 100%; width: 100%; min-width: 100%; display: flex; flex-direction: column; gap: 5px; overflow-y: auto; background-color: white; ">
            <!-- <div class="orderinfoelement" v-for="(element, index) in mostrecentordersinfo" :key="index">{{ element.ordernumber }} - {{ element.plannedprocesduration }} - {{ element.actualduration }} - {{ element.quantity }} - {{ element.starttime }} - {{ element.endtime}}</div> -->

            <el-card>

                <el-table :data="mostrecentordersinfo" style="width: 100%">
                    <el-table-column prop="ordernumber" label="Order Number" width="150" />
                    <el-table-column prop="plannedprocesduration" label="Planned Duration" width="150" />
                    <el-table-column prop="actualduration" label="Actual Duration" width="150" />
                    <el-table-column prop="quantity" label="Quantity" width="100" />
                    <el-table-column prop="starttime" label="Start Time" width="150" />
                    <el-table-column prop="endtime" label="End Time" width="150" />
                </el-table>

            </el-card>

            <div style="position: absolute; top: 5px; right: 5px;" @click="showmostrecentordersinfo=false; showInfoCard(currentselectedobject)"><el-icon class="iconhover"><Close /></el-icon></div> 

        </div>
    </div>

</template>

<script setup>
import * as THREE from 'three'
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { onMounted, ref, onBeforeUnmount } from 'vue'
import { gsap } from 'gsap'

// Grundgerüst -----------------------

// Variablen:

const listedmachines = {
    matec_2: {name: "matec-30 S", cpnumber: "530133N", angle: null, animations: ['matec_openleftdoor', 'matec_openrightdoor']},
    senhongxing_1: {name: '森红星', cpnumber: '523246N', angle: null, animations: []},
    sugino_1: {name: "Sugino", cpnumber: '533797N', angle: null, animations: ['sugino_openleftdoor', 'sugino_openrightdoor']},
    basketsupermarket_1: {name: "Washing basket supermarket", cpnumber:'-', angle: null, animations: []},
    toolsupermarket_1: {name: "tool supermarket", cpnumber: '-', angle: null, animations: []}
}

//onMounted + onBeforeUnmounted:

onMounted(()=>{
    getThreejs()
    window.addEventListener('resize', handleResize)
    window.addEventListener('keydown', handleKeyDown)
    scenecontainer.value.addEventListener('mousedown', onMouseDown)
    scenecontainer.value.addEventListener('mouseup', onMouseUp)
})

onBeforeUnmount(() =>{
    window.removeEventListener('resize', handleResize)
    window.removeEventListener('keydown', handleKeyDown)
    if(scenecontainer.value){
        scenecontainer.value.removeEventListener('mousedown', onMouseDown)
        scenecontainer.value.removeEventListener('mouseup', onMouseUp)
    }
})

//Initialisierung der Szene:

const scenecontainer = ref(null)
let scene, renderer, camera, controls

//Animation --
let mixer; const clock = new THREE.Clock(); let animationen = {};
// --

function getThreejs(){

    scene = new THREE.Scene();
    // scene.background = new THREE.Color(0xECECEC);
    scene.background = new THREE.Color(0x0A0E14);

    const width = scenecontainer.value.clientWidth;
    const height = scenecontainer.value.clientHeight;
    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100)
    camera.position.set(5, 1, 12)

    renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(width, height)
    scenecontainer.value.appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.rotateSpeed = 0.5
    controls.update()


    // const axesHelper = new THREE.AxesHelper(20)
    // scene.add(axesHelper)

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
    scene.add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 5);
    directionalLight.position.set(5, 10, 7);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 1024;
    directionalLight.shadow.mapSize.height = 1024;
    directionalLight.shadow.camera.near = 0.5;
    directionalLight.shadow.camera.far = 500;
    scene.add(directionalLight);

    const hemisphereLight = new THREE.HemisphereLight(0xfffbb, 0x080820, 0.7)
    scene.add(hemisphereLight)


    const gltfLoader = new GLTFLoader();

    const models = [
        { path: "/models/workshopmodel.glb", position: new THREE.Vector3(0, 0, 0)}
    ]

    models.forEach(model => {
        gltfLoader.load(model.path, (gltf) => {
        const root = gltf.scene;
        scene.add(root);

        root.traverse((child) => {
        if (child.isMesh && child.name.includes('Cube088')) {
            child.material.roughness = 0; // weniger matt
            child.material.metalness = 0.5; // leichter Glanz
            child.material.needsUpdate = true;
        }
        if (child.isMesh && child.name.toLowerCase().includes('glas')) {
            if (Array.isArray(child.material)) {
            // Falls mehrere Materialien
            child.material.forEach(mat => {
                mat.transparent = true;
                mat.opacity = 0.3; // gewünschte Transparenz
            });
            } else {
            child.material.transparent = true;
            child.material.opacity = 0.3;
            }
        }
        });

        //Animation--
        mixer = new THREE.AnimationMixer(root);
        gltf.animations.forEach((clip, i) => {
            animationen[clip.name || `anim${i}`] = mixer.clipAction(clip);
        });
        // activeAction = animationen[gltf.animations[0].name || 'anim0'];
        //--

        });
    });

    function animate() {
        requestAnimationFrame(animate);

        //Animation--
        const delta = clock.getDelta();      
        if (mixer) mixer.update(delta);
        //--

        controls.update();
        renderer.render(scene, camera)

        updateInfoCardPosition()

    }
    animate()
}

function playAnimations(animations){
    //openleftdoor, openrightdoor, wagenanimation
    for (const animation of animations){
        const currentanimation = animationen[animation]
        if( currentanimation ){
            currentanimation.reset();
            currentanimation.setLoop(THREE.LoopOnce, 1);
            currentanimation.setEffectiveTimeScale(1.3)
            currentanimation.clampWhenFinished = true;
            currentanimation.play();
        }
        console.error(`Animation ${animation} could not be found`);
    }
}

function stopAnimations(animations){
    // for (const animation of animations){
    //     currentanimation = animationen[animation]
    //     if( currentanimation ){
    //         currentanimation.stop()
    //     }
    //     console.error(`Animation ${animation} could not be found`)
    // }
    for (const animation of animations){
        const currentanimation = animationen[animation]
        if( currentanimation ){
            currentanimation.reset();
            currentanimation.time = currentanimation.getClip().duration
            // currentanimation.setLoop(THREE.LoopOnce, 1);
            currentanimation.clampWhenFinished = true;
            currentanimation.setEffectiveTimeScale(-1.3)
            currentanimation.play();
        }
        console.error(`Animation ${animation} could not be found`);
    }
}

// // Animation abspielen:

// function playAnimation(name) {
//   if (!actions[name]) {
//     console.warn(`Animation ${name} existiert nicht!`);
//     return;
//   }
  
//   if (activeAction === actions[name]) return; // Schon aktiv

//   // Neue Animation einblenden
//   const newAction = actions[name];
//   newAction.reset();
//   newAction.play();
//   newAction.enabled = true;
  
//   // Alte Animation ausblenden (fade out)
//   if (activeAction) {
//     activeAction.crossFadeTo(newAction, 0.5, false);
//   }
  
//   activeAction = newAction;
// }
// //--

// Resizing:

const handleResize = () => {
    if (!scenecontainer.value || !renderer || !camera) return;
    const width = scenecontainer.value.clientWidth;
    const height = scenecontainer.value.clientHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix()
}

// Key-and Click-event variables ---------------------

const currentobjpos = ref(0, 0, 0)
const currentcamerapos = ref(0, 0, 0)
const currentselectedobject = ref(null)

// KeyDownEvents -------------------------------------

// KeyDownHandler:

function handleKeyDown(event){
    if(event.key === 'Escape'){
        unfocusobject()
        hideInfoCard()
    }
}

// KeyDownResult

function unfocusobject(){

    gsap.to(camera.position, {
      x: 10,
      y: 10,
      z: currentcamerapos.value.z,
      duration: 1.0,
      ease: "power3.out",
    });

    gsap.to(controls.target, { // Animiert controls.target
        x: currentobjpos.value.x,
        y: 0,
        z: currentcamerapos.value.z,
        duration: 1.0,
        ease: "power3.out",
        onUpdate: () => { // Wichtig: Update die Controls in der Animation
        controls.update();
        },
    });

    if (selectedobjectname.value){
        stopAnimations(listedmachines[selectedobjectname.value].animations)
    }

    selectedobjectname.value = null

    if (currentselectedobject.value) { // Überprüfe, ob ein Objekt ausgewählt wurde
      resetHighlight(currentselectedobject.value);
    }

    currentselectedobject.value = null;

    //Anstatt controls.target.set(10, 10, 0) und controls.update() besser controls auch mit gsap setzen, weil 
    //damit der Übergang flüssiger und es sonst passieren kann, dass die Kamera "rückwärts" schaut

}



// Klick Events --------------------------------

// Click Handler:

let mouseDownPos = null;
let mouseDownTime = null;

function onMouseDown(event){
    mouseDownPos = { x: event.clientX, y: event.clientY};
    mouseDownTime = Date.now();
}

function onMouseUp(event) {
  if (!mouseDownPos || !mouseDownTime) return;

  const dx = event.clientX - mouseDownPos.x;
  const dy = event.clientY - mouseDownPos.y;
  const dist = Math.sqrt(dx * dx + dy * dy);
  const clickDuration = Date.now() - mouseDownTime;

  const maxDist = 5;       // maximale Mausbewegung in Pixel für Klick
  const maxDuration = 300; // maximale Zeit in ms für Klick

  if (dist <= maxDist && clickDuration <= maxDuration) {
    onClick(event);  // Nur echtes Klick-Event aufrufen
  }

  mouseDownPos = null;
  mouseDownTime = null;
}

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onClick(event){
    
    if (!scenecontainer.value) return;

    const rect = scenecontainer.value.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = - ((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);

    if (intersects.length > 0) {
        const clickedObject = intersects[0].object;
        processclick(clickedObject)
    }
}

// Click result:

const selectedobjectname = ref(null)

function processclick(clickedObject){
    // const objectname = clickedObject.name 
    // const objectid = clickedObject.id

    if (Object.keys(listedmachines).includes(clickedObject.name)){

        const { targetPos, newCameraPos } = focusonobject(clickedObject)

        currentobjpos.value = targetPos
        currentcamerapos.value = newCameraPos
        selectedobjectname.value = clickedObject.name;
        currentselectedobject.value = clickedObject

        highlightObject(clickedObject)
        showInfoCard(clickedObject);
        playAnimations(listedmachines[clickedObject.name].animations)
        getcurrentorder()
        gettodaysoutput()
    }

}

function focusonobject(clickedObject){

    const targetPos = new THREE.Vector3();
    clickedObject.getWorldPosition(targetPos);
    const newCameraPos = targetPos.clone().add(new THREE.Vector3(7, 5, 0));

    gsap.to(camera.position, {
    x: newCameraPos.x,
    y: newCameraPos.y,
    z: newCameraPos.z,
    duration: 1.0,
    ease: "power3.out",
    });

    gsap.to(controls.target, { // Animiert controls.target
        x: targetPos.x,
        y: targetPos.y,
        z: targetPos.z,
        duration: 1.0,
        ease: "power3.out",
        onUpdate: () => { // Wichtig: Update die Controls in der Animation
        controls.update();
        },
    });

    return { targetPos, newCameraPos }

}

function highlightObject(object) {
  if (object.material) {
    if (!object.userData.originalEmissive) {
      object.userData.originalEmissive = object.material.emissive.clone();
    }
    object.material.emissive.set(0xaaaaaa);
  }
}
 
function resetHighlight(object) {
  if (object.material && object.userData.originalEmissive) {
    object.material.emissive.copy(object.userData.originalEmissive);
  }
}

function showInfoCard(object) {

    let infoCard = document.getElementById("threejs-info-card");

    const machinename = object.name
    const displayname = listedmachines[machinename] ? listedmachines[machinename].name : 'unknown'

    if (!infoCard) {
        infoCard = document.createElement("div");
        infoCard.id = "threejs-info-card";
        document.body.appendChild(infoCard);

        infoCard.style.cssText = `
            position: absolute;
            background: rgba(255, 255, 255, 0.85);
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            padding: 12px 16px;
            max-width: 240px;
            font-family: Arial, sans-serif;
            font-size: 14px;
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.9);
            transition: opacity 0.3s ease, transform 0.3s ease;
            pointer-events: none;
            z-index: 1000;
        `;
    }

    infoCard.innerHTML = `
        <h3 style="margin: 0 0 8px; color: #333;">${
        displayname || "未命名对象"
        }</h3>
        <div style="color: #666; margin-bottom: 6px; position: relative; padding-left: 20px;">
            状态:
            <span style="position: absolute; left: 0; top: 50%; transform: translateY(-50%);">
                <span class="status-dot" style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: #4CAF50; margin-right: 6px;"></span>
            </span>
            运行中
        </div>
        <div style="color: #666;">
            实时累计产出: 100
        </div>
        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #eee; color: #888;">
            点击空白处返回
        </div>
    `;
 
    const position = new THREE.Vector3();
    object.getWorldPosition(position);
    position.project(camera);

    const canvas = renderer.domElement;
    const x = (position.x * 0.5 + 0.5) * canvas.clientWidth;
    const y = (-position.y * 0.5 + 0.5) * canvas.clientHeight;

    infoCard.style.left = `${x + 150}px`;
    infoCard.style.top = `${y}px`;
    infoCard.style.opacity = "1";
    infoCard.style.transform = "translate(0, -50%) scale(1)";
}

function hideInfoCard() {
  const infoCard = document.getElementById("threejs-info-card");
  if (infoCard) {
    infoCard.style.opacity = "0";
    infoCard.style.transform = "translate(0, -50%) scale(0.9)";
  }
}

function updateInfoCardPosition() {
  if (currentselectedobject.value && document.getElementById("threejs-info-card")) {
    const position = new THREE.Vector3();
    currentselectedobject.value.getWorldPosition(position);
    position.project(camera);
 
    const canvas = renderer.domElement;
    const x = (position.x * 0.5 + 0.5) * canvas.clientWidth;
    const y = (-position.y * 0.5 + 0.5) * canvas.clientHeight;
 
    const infoCard = document.getElementById("threejs-info-card");
    infoCard.style.left = `${x + 150}px`;
    infoCard.style.top = `${y}px`;
  }
}



// Externe Logik (kein three.js) -----------------

import { Close } from '@element-plus/icons-vue'
import { fetchmateriallist } from "@/services/machinedataapis";
import { fetchcurrentorder, fetchtodaysoutput, fetchrecentordersoverview } from "@/services/odataapis";
import { ElLoading } from 'element-plus'

//任务单号
const currentordernumber = ref('')
const currentorderplannedduration = ref('')
const orderlabelref = ref(false)

async function getcurrentorder(){
    const loading = ElLoading.service({
        target: orderlabelref.value,
        background: 'rgba(255, 255, 255, 0)'
    })
    try{
        const currentorderinfo = await fetchcurrentorder(listedmachines[selectedobjectname.value].cpnumber)
        currentordernumber.value = currentorderinfo.ordernumber
        currentorderplannedduration.value = currentorderinfo.plannedduration
    } catch(error){
        console.error(error)
    } finally{
        loading.close()
    }
}

//今日加工数量
const todaysoutput = ref(0)
const todaysoutputlabelref = ref(null)

async function gettodaysoutput(){
    const loading = ElLoading.service({
        target: todaysoutputlabelref.value,
        background: 'rgba(255, 255, 255, 0)'
    })
    try{
        todaysoutput.value = await fetchtodaysoutput(listedmachines[selectedobjectname.value].cpnumber)
    } catch(error){
        console.error(error)
    } finally{
        loading.close()
    }
}

//Materialliste:

const showmachinematerials = ref(false)
const selectedmachinematerialnumbers = ref([])
const materialslistref = ref(null)
const nomatchingmaterialsfound = ref(false)

async function unhidemachinematerials(){
    showmachinematerials.value = true
    const loading = ElLoading.service({
        target: materialslistref.value,
        text: "Fetching materials for selected machine",
        background: 'rgba(255, 255, 255, 0.7)'
    })
    try{
        selectedmachinematerialnumbers.value = await fetchmateriallist(selectedobjectname.value)
        if (selectedmachinematerialnumbers.value.length === 0){
            nomatchingmaterialsfound.value = true
        } else{
            nomatchingmaterialsfound.value = false
        }
    } catch(error){
        console.error(error)
    } finally{
        loading.close()
    }
}

//detailtierte Orderinfo:
const showmostrecentordersinfo = ref(false)
const mostrecentordersinforef = ref(null)
const mostrecentordersinfo = ref([])

async function getrecentordersinfo(){
    showmostrecentordersinfo.value = true
    hideInfoCard()
    const loading = ElLoading.service({
        target: mostrecentordersinforef.value,
        text: "Fetching data. Please wait",
        background: 'rgba(255, 255, 255, 0)'
    }) 
    try{
        mostrecentordersinfo.value = await fetchrecentordersoverview(selectedobjectname.value)
    } catch(error){
        console.error(error)
    } finally{
        loading.close()
    }
}

</script>

<style scoped>
.scenecontainer{
    width: 100%;
    height: 100%;
}

.machineinfopanel{
    z-index: 998;
    position: absolute; 
    top: 0px; 
    left: 0px;
    transform: translateX(-20px);
    background-color: rgba(0, 0, 0, 0.7); 
    display: flex; 
    flex-direction: column; 
    gap: 5px; 
    min-width: 200px; 
    justify-content: center; 
    padding: 15px; 
    /* border-radius: 12px; */
    height: 100vh;
    border-right: 1px solid white;
    transition: left 0.3s ease;
    color: white;
    font-weight: 600;
}
.infopanelinvisible{
    left:-250px;
}
.infopanelvisible{
    left: 15px
}
.machineinfoitem{
    display: flex; 
    justify-content: space-between;
    align-items: baseline; 
    border-bottom: 1px dotted white;
    font-weight: 400;
}
.machinematerialslist{
    position: absolute;  
    top: 0px;
    padding-top: 12px;
    padding-bottom: 12px;
    padding-left: 22px;
    padding-right: 28px;
    /* box-sizing: border-box; */
    background-color: rgba(0, 0, 0, 0.7);
    /* min-width: 100px; 
    min-height: 100px;  */
    color: white;
    display: flex; 
    flex-direction: column;
    transition: right 0.3s ease;
}
.materiallistvisible{
    right: 0px;
}
.materiallistinvisible{
    right: -200px;
}
.machinematerialslabel{
    color: #A0D8F1;
    transition: color 0.3s ease;
}
.machinematerialslabel:hover{
    color: #0071a5;
}
.machineinfopanel{
    --el-loading-spinner-size: 14px;
}
.orderinfoelement{
    padding: 10px;
    background-color: rgba(0, 0, 0, 0.8);
    transition: background-color 0.3s ease
}
.orderinfoelement:hover{
    background-color: rgba(0, 0, 0, 0.7);
}
</style>
