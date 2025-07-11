import { ElMessage } from "element-plus"
import { materialselectionstore } from "@/stores/filterinformationstore"
import { spoolscrapfilteroptionsstore } from "@/stores/filterinformationstore"
import { selectedmonthstore } from "@/stores/filterinformationstore"
import { environmentsettingsstore } from "@/stores/environmentsettingsstore"

export async function removedataformonth(month){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        await fetch(environmentsettingsoptions.apimainpath + "/removedataformonth",{
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                month: month
            })
        })
    } catch(error){
        console.error(error)
    }
}

export async function getnewdatafromsource(month){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/readnewdatafromsource',{
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({
                month: month
            })
        })
        const data = await response.json()
        ElMessage(`${data.status}`)
    } catch(error){
        ElMessage(`Error with getnewdatafromsource: ${error}`)
    }
}

export async function fetchncrorigins(){

    const environmentsettingsoptions = environmentsettingsstore()

    const materialselection = materialselectionstore()
    const selectedmaterials = materialselection.selectedmaterials

    const selectedmonthinfo = selectedmonthstore()
    const month = selectedmonthinfo.selectedmonthforvisualization

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getncrorigins',{
            method: 'POST',
            headers: { 'Content-type': 'application/json'},
            body: JSON.stringify({
                matnrstofilter: selectedmaterials,
                month: month
            })
        })

        const data = await response.json()
        const elements = data.elements
        return elements
    } catch(error){
        ElMessage(`Error with fetchncrorigins: ${error}`)
        return []
    }
}

export async function fetchsupplierofcastings(){

    const environmentsettingsoptions = environmentsettingsstore()

    const materialselection = materialselectionstore()
    const selectedmaterials = materialselection.selectedmaterials

    const selectedmonthinfo = selectedmonthstore()
    const month = selectedmonthinfo.selectedmonthforvisualization

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getsupplierofcastings',{
            method: 'POST',
            headers: { 'Content-type': 'application/json'},
            body: JSON.stringify({
                matnrstofilter: selectedmaterials,
                month: month
            })
        })

        const data = await response.json()
        const elements = data.elements
        return elements
    } catch(error){
        ElMessage(`Error with fetchsupplierofcastingsandnonecastings: ${error}`)
        return []
    }
}

export async function fetchsupplierofnonecastings(){

    const environmentsettingsoptions = environmentsettingsstore()

    const materialselection = materialselectionstore()
    const selectedmaterials = materialselection.selectedmaterials

    const selectedmonthinfo = selectedmonthstore()
    const month = selectedmonthinfo.selectedmonthforvisualization

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getsupplierofnonecastings',{
            method: 'POST',
            headers: { 'Content-type': 'application/json'},
            body: JSON.stringify({
                matnrstofilter: selectedmaterials,
                month: month
            })
        })

        const data = await response.json()
        const elements = data.elements
        return elements
    } catch(error){
        ElMessage(`Error with fetchsupplierofcastingsandnonecastings: ${error}`)
        return []
    }
}

export async function fetchsuppliersinternal(){

    const environmentsettingsoptions = environmentsettingsstore()

    const materialselection = materialselectionstore()
    const selectedmaterials = materialselection.selectedmaterials

    const selectedmonthinfo = selectedmonthstore()
    const month = selectedmonthinfo.selectedmonthforvisualization

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getsuppliersinternal',{
            method: 'POST',
            headers: { 'Content-type': 'application/json'},
            body: JSON.stringify({
                matnrstofilter: selectedmaterials,
                month: month
            })
        })

        const data = await response.json()
        const elements = data.elements
        return elements
    } catch(error){
        ElMessage(`Error with fetchsupplierofcastingsandnonecastings: ${error}`)
        return []
    }
}

export async function fetchscrapissueorigins(){

    const environmentsettingsoptions = environmentsettingsstore()

    const materialselection = materialselectionstore()
    const selectedmaterials = materialselection.selectedmaterials

    const selectedmonthinfo = selectedmonthstore()
    const month = selectedmonthinfo.selectedmonthforvisualization

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getscrapissueorigins',{
            method: 'POST',
            headers: { 'Content-type': 'application/json'},
            body: JSON.stringify({
                matnrstofilter: selectedmaterials,
                month: month
            })
        })

        const data = await response.json()
        const elements = data.elements
        return elements
    } catch(error){
        ElMessage(`Error with fetchsupplierofcastingsandnonecastings: ${error}`)
        return []
    }
}

export async function fetchspoolscrapmethods(){

    const environmentsettingsoptions = environmentsettingsstore()

    const materialselection = materialselectionstore()
    const selectedmaterials = materialselection.selectedmaterials

    const selectedmonthinfo = selectedmonthstore()
    const month = selectedmonthinfo.selectedmonthforvisualization

    const spoolscrapfilteroptions = spoolscrapfilteroptionsstore()
    const prodcutstofilter = spoolscrapfilteroptions.selectedproductforspoolfilter

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getspoolscrapmethods',{
            method: 'POST',
            headers: { 'Content-type': 'application/json'},
            body: JSON.stringify({
                matnrstofilter: selectedmaterials,
                month: month,
                prodcutstofilter: prodcutstofilter
            })
        })

        const data = await response.json()
        const elements = data.elements
        return elements
    } catch(error){
        ElMessage(`Error with fetchsupplierofcastingsandnonecastings: ${error}`)
        return []
    }
}

export async function fetchpoolscrapreason(){

    const environmentsettingsoptions = environmentsettingsstore()

    const materialselection = materialselectionstore()
    const selectedmaterials = materialselection.selectedmaterials

    const selectedmonthinfo = selectedmonthstore()
    const month = selectedmonthinfo.selectedmonthforvisualization

    const spoolscrapfilteroptions = spoolscrapfilteroptionsstore()
    const prodcutstofilter = spoolscrapfilteroptions.selectedproductforspoolfilter

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getspoolscrapreason',{
            method: 'POST',
            headers: { 'Content-type': 'application/json'},
            body: JSON.stringify({
                matnrstofilter: selectedmaterials,
                month: month,
                prodcutstofilter: prodcutstofilter
            })
        })

        const data = await response.json()
        const elements = data.elements
        return elements
    } catch(error){
        ElMessage(`Error with fetchsupplierofcastingsandnonecastings: ${error}`)
        return []
    }
}

export async function fetchproductlistforspoolscrap(){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getproductlistforspoolscrap',{
            method: 'GET',
            headers: { 'content-Type': 'application/json'}
        })
        const data = await response.json()
        const uniqueproductlist = data.uniqueproductlist
        return uniqueproductlist
        
    } catch(error){
        console.error(error)
        return []
    }
}

export async function fetchmostfrequentscrapissuecauses(){

    const environmentsettingsoptions = environmentsettingsstore()

    const materialselection = materialselectionstore()
    const selectedmaterials = materialselection.selectedmaterials

    const selectedmonthinfo = selectedmonthstore()
    const month = selectedmonthinfo.selectedmonthforvisualization

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getmostfrequentscrapissuecauses',{
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify({
                month: month,
                selectedmaterials: selectedmaterials
            })
        })
        const data = await response.json()
        const constchangetopreviousmonthperissue = data.constchangetopreviousmonthperissue
        return constchangetopreviousmonthperissue
    } catch(error){
        console.error(error)
        return []
    }
}

export async function fetchhistoric_Worstmethodsforspoolscrap(month){

    const environmentsettingsoptions = environmentsettingsstore()
    
    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/gethistoric_Worstmethodsforspoolscrap',{
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify({
                month: month
            })
        })
        const data = await response.json()
        const methodcostmonhtlycomparison = data.methodcostmonhtlycomparison
        return methodcostmonhtlycomparison
    } catch(error){
        console.error(error)
    }
}


