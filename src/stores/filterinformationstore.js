import { defineStore } from "pinia";
import { ref } from 'vue'

export const materialselectionstore = defineStore('materialselection', () =>{
    
        const selectedmaterials = ref([])

        function changeselectedmaterial(material){
            if(!selectedmaterials.value.includes(material)){
                selectedmaterials.value.push(material)
            } else{
                const index = selectedmaterials.value.indexOf(material)
                selectedmaterials.value.splice(index, 1)
            }
        }

        function removeentireselection(){
            selectedmaterials.value = []
        }

        const applychangetrigger = ref(false)

        return{
            selectedmaterials,
            changeselectedmaterial,
            removeentireselection,
            applychangetrigger
        }
    },
    {
        persist: {
            storage: sessionStorage
        }
    }
)

export const selectedmonthstore = defineStore('selectedmonthinfo', () =>{

        const selectedmonthforvisualization = ref('jan')

        return{
            selectedmonthforvisualization
        }
    },
    {
        persist: {
            store: sessionStorage
        }
    }
)

export const spoolscrapfilteroptionsstore = defineStore('spoolscrapfilteroptions', () =>{

        const selectedproductforspoolfilter = ref('')

        return{
            selectedproductforspoolfilter
        }
    },
    {
        persist: {
            storage: sessionStorage
        }
    }
)
