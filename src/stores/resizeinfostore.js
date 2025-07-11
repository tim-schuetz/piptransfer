import { defineStore } from "pinia";
import { ref } from 'vue';

export const resizeinfostore = defineStore('defineinfo', () => {

    const windowsizechanged = ref(false);

    function triggerwindowsizechange(){
        windowsizechanged.value = !windowsizechanged.value;
    }

    return {
        windowsizechanged,
        triggerwindowsizechange
    }

})


