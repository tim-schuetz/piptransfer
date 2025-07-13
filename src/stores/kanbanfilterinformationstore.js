import { defineStore } from "pinia";
import { ref } from 'vue';

export const kanbanfilterinfostore = defineStore('kanbanfilterinfos', () => {
    
    const selectedMaterials = ref([]);
    const selectedLoop = ref('all');
    const selectedMonthasint = ref('all');
    const xaxisparameter = ref('ordernumber');

    function setselectedloop(newloop){
        selectedLoop.value = newloop
        console.log("selectedLoop.value:", selectedLoop.value)
    }

    function getselectedloop(){
        return selectedLoop.value
    }


    function addorremovematerialtoselection(material){
        if (selectedMaterials.value.includes(material)){
            selectedMaterials.value = selectedMaterials.value.filter(element => element !== material)
        } else {
            selectedMaterials.value.push(material)
        }
    }

    function deselectallmaterials(){
        selectedMaterials.value = [];
    }

    function setselectedmaterial(material){
        selectedMaterials.value = []
        selectedMaterials.value.push(material)

        console.log("selectedMaterials.value:", selectedMaterials.value)
    }

    function getmaterials(){
        return selectedMaterials.value
    }


    function setselectedmonth(monthasstring) {
        const monthmap = {
            'all': 'all',
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr': 4,
            'may': 5,
            'jun': 6,
            'jul': 7,
            'aug': 8,
            'sep': 9,
            'oct': 10,
            'nov': 11,
            'dec': 12
        };

        const shortmonth = monthasstring.toLowerCase().slice(0, 3); // z.B. "January" → "jan"
        const monthnumber = monthmap[shortmonth];

        if (monthnumber) {
            selectedMonthasint.value = monthnumber;
        } else {
            console.warn("Ungültiger Monatsname:", monthasstring);
            selectedMonthasint.value = null;
        }

        console.log("selectedMonthasint.value:", selectedMonthasint.value)
    }

    function getselectedmonth(){
        return selectedMonthasint.value
    }


    function setxaxisparameter(newxaxisparameter){
        xaxisparameter.value = newxaxisparameter
    }

    function getxaxisparameter(){
        return xaxisparameter.value
    }


    function resetallfilters(){
        selectedMaterials.value = [];
        selectedLoop.value = 'all';
        selectedMonthasint.value = 'all';
        xaxisparameter.value = 'ordernumber';
    }

    function isfilteractive(){
        if (selectedMaterials.value.length === 0 && !selectedLoop.value && !selectedMonthasint.value && !xaxisparameter.value) {
            return false
        } else {
            return true
        }
    }

    return {
        selectedMaterials,
        selectedLoop,
        selectedMonthasint,
        setselectedloop,
        getselectedloop,
        addorremovematerialtoselection,
        deselectallmaterials,
        setselectedmaterial,
        getmaterials,
        setselectedmonth,
        getselectedmonth,
        setxaxisparameter,
        getxaxisparameter,
        resetallfilters,
        isfilteractive
    }

})

export const currentlydisplayedchartstore = defineStore('currentselectedchart', () =>{
    //Ist deshalb wichtig, um dann bei FilterOptions auch noch die Visualspezifischen Filter anzuzeigen, die zum aktuellen Visual gehören

    const currentchart = ref('leadtimebymaterials')

    function getcurrentchart(){
        return currentchart.value;
    }

    function setcurrentchart(chart){
        currentchart.value = chart
    }

    return{
        currentchart,
        getcurrentchart,
        setcurrentchart
    }

})


