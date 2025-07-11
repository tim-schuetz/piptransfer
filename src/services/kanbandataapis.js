import { environmentsettingsstore } from "@/stores/environmentsettingsstore"

// export async function fetchkanbaninfo(material, loop, sortfor){

//     const environmentsettingsoptions = environmentsettingsstore()

//     try{
//         const response = await fetch(environmentsettingsoptions.apimainpath + '/getkanbandata', {
//             method: 'POST',
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({
//                 material: material,
//                 loop: loop,
//                 sortfor: sortfor
//             }) 
//         })

//         const data = await response.json()

//         return [data.kanbaninfos, data.uniquematerialslist, data.uniqueloopslist, data.monthselectoptions, data.avgleadtime, data.minleadtime, data.maxleadtime, data.totalvalues]
//     } catch(error){
//         console.error(error)
//     }
// }

export async function getkanbanfilteroptions(){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getkanbanfilteroptions',{
            method: 'GET',
            headers: { 'Content-type': 'application/json' }
        })
        const data = await response.json()

        const { uniquematerialslist, uniqueloopslist, uniquemonths_as_int } = data
        return { uniquematerialslist, uniqueloopslist, uniquemonths_as_int }

    } catch(error) {
        console.error(error)
    }

}



export async function updatekanbandatabase(){

    const environmentsettingsoptions = environmentsettingsstore()

    try{
        await fetch(environmentsettingsoptions.apimainpath + '/updatekanbandatabase',{
            method: 'GET',
            headers: {'Content-type': 'application/json'}
        })
    } catch(error){
        console.error(error)
    }
}
