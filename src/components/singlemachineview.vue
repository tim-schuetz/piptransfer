<template>
    <div ref="scenecontainer"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

const scenecontainer = ref(null)

onMounted(()=>{
    getThreejs()
})

let scene, renderer, camera, controls

function getThreejs(){

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xECECEC);

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


    const axesHelper = new THREE.AxesHelper(20)
    scene.add(axesHelper)

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
    scene.add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
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
        });
    });
}

import { defineProps } from 'vue';
import MachineList from './MachineList.vue';

defineProps({angle: Number})

watch(
    () => angle,
    (newangle) =>{
        MachineList.rotation.x += newangle
    }
)

</script>

<style scoped>

</style>