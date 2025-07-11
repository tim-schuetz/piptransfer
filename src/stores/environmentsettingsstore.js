import { defineStore } from "pinia";
import { ref } from 'vue';

const defaultApiPath = window.location.hostname.includes('localhost') 
    ? "http://localhost:5000"
    : "http://wujvm00120.apac.bosch.com:443/";

export const environmentsettingsstore = defineStore('environmentsettings', () =>{
    const apimainpath = ref(defaultApiPath)
    return {
        apimainpath
    }
})

