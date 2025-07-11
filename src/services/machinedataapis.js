import { ElMessage } from "element-plus"
import { environmentsettingsstore } from "@/stores/environmentsettingsstore"

export async function getmachinelist(){

    const environmentsettingsoptions = environmentsettingsstore()

    try{

        const response = await fetch(environmentsettingsoptions.apimainpath + '/maschinenliste',{
            method: 'GET',
            headers:{
                'content-type': 'application/json'
            }
        })

        const data = await response.json()
        const verfuegbaremaschinen = data.verfuegbaremaschinen

        return verfuegbaremaschinen
    }
    catch(error){
        ElMessage.warning(`Fetch war erfolglos: ${error}`)
        return []
    }
}

export async function removeworkcenter(workcenter){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        await fetch(environmentsettingsoptions.apimainpath + '/deletemachine',{
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({
                workcenter: workcenter
            }) 
        })
    } catch(error) {
        console.error(error)
    }
}

export async function changemachineactivationstatus(machineworkcenter, newstatus){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        await fetch(environmentsettingsoptions.apimainpath + '/changemachineactivationstatus', {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({
                machineworkcenter: machineworkcenter,
                newstatus: newstatus
            })
        })
    }
    catch(error){
        ElMessage.warning(`Fehler: ${error}`)
    }
}

export async function addnewmachine(workcenter, name, materials){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        await fetch(environmentsettingsoptions.apimainpath + '/addnewmachine',{
            method: 'POST',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify({
                workcenter: workcenter,
                name: name,
                materials: materials
            })
        })
    }
    catch(error){
        ElMessage(`Fehler aufgetreten: ${error}`)
    }
}

export async function fetchmateriallist(){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/fetchmateriallist',{
            method: 'GET',
            headers:{
                'Content-type': 'application/json'
            }
        })

        const data = await response.json()
        const materials = data.materials
        return materials
    }
    catch(error){
        ElMessage.warning(`Fehler beim Abrufen der Materialnummern: ${error}`)
        return []
    }
}

export async function removematerial(materialnumber){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        await fetch(environmentsettingsoptions.apimainpath + '/removematerial',{
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify({
                materialnumber: materialnumber
            })
        })
    } catch(error){
        console.error(error)
    }
}

export async function fetchmaterialsfromdatabase(workcenternumber){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        const data = await fetch( environmentsettingsoptions.apimainpath + '/getmaterialsformachine', {
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify({
                workcenternumber: workcenternumber
            })
        })
        const response = await data.json()
        const matnumbers = response.matnumbers
        return matnumbers
    } catch(error){
        console.error(error)
        return []
    } 
}
