<template>
  <div class="box" ref="box"></div>
</template>
<script>
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

export default {
  name: "ThreeJs",
  methods: {
    getThreeJs() {
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x8cc7de); //0x8cc7de

      const box = this.$refs.box;
      const width = box.clientWidth;
      const height = box.clientHeight;

      const camera = new THREE.PerspectiveCamera(
        45,
        // window.innerWidth / window.innerHeight,
        width / height,
        0.1,
        100
      );
      camera.position.set(5, 1, 12);
      // camera.lookAt(0, 0, 0); // 设置相机看向原点

      const renderer = new THREE.WebGLRenderer();
      // renderer.setSize(829, 550);
      renderer.setSize(width, height)
      box.appendChild(renderer.domElement); // 将渲染结果添加到目标元素

      // 添加辅助坐标
      const axesHelper = new THREE.AxesHelper(20);
      scene.add(axesHelper);

       // 添加环境光（均匀照亮场景）
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambientLight);

      // 添加方向光（模拟太阳光）
      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(5, 10, 7); // 调整光源位置
      directionalLight.castShadow = true; // 启用阴影投射
      
      // 配置阴影
      directionalLight.shadow.mapSize.width = 1024;
      directionalLight.shadow.mapSize.height = 1024;
      directionalLight.shadow.camera.near = 0.5;
      directionalLight.shadow.camera.far = 500;
      
      scene.add(directionalLight);

      // 添加半球光（模拟天空和地面反射）
      const hemisphereLight = new THREE.HemisphereLight(0xffffbb, 0x080820, 0.7);
      scene.add(hemisphereLight);

      // 添加轨道控制器
      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.rotateSpeed = 0.5;

      // 添加地面平面（用于显示阴影）
      const planeGeometry = new THREE.PlaneGeometry(100, 100);
      const planeMaterial = new THREE.MeshStandardMaterial({
        color: 0xcccccc,
        roughness: 0.8,
        metalness: 0.2,
        side: THREE.DoubleSide
      });
      const plane = new THREE.Mesh(planeGeometry, planeMaterial);
      plane.rotation.x = -Math.PI / 2;
      plane.position.y = -1;
      plane.receiveShadow = true; // 接收阴影
      scene.add(plane);
      
      controls.update();

      // 创建几何体
      // const geometry = new THREE.BoxGeometry(2, 2, 2);
      // const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
      // const cube = new THREE.Mesh(geometry, material);
      // scene.add(cube);

      const gltfLoader = new GLTFLoader();
      gltfLoader.load(
        "/models/workshop_moeico_dist1.glb",
        (gltf) => {
          const root = gltf.scene;
          scene.add(root);
        }
      );

      // 声明渲染函数
      function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
      }
      animate();
    },
  },
  mounted() {
    this.getThreeJs(); // 执行three的相关代码
  },
};
</script>
<style scoped>
.box {
  width: 90%;
  height: 90%;
}
</style>