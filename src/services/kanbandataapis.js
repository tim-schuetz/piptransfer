import { environmentsettingsstore } from "@/stores/environmentsettingsstore"
import { kanbanfilterinfostore } from "@/stores/kanbanfilterinformationstore"

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
        return { uniquematerialslist: [], uniqueloopslist: [], uniquemonths_as_int: []}
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

export async function getkpivalues(){

    const environmentsettingsoptions = environmentsettingsstore()
    const kanbanfilterinfooptions = kanbanfilterinfostore()

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getkpivalues',{
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify({
                materials: kanbanfilterinfooptions.getmaterials,
                loop: kanbanfilterinfooptions.getselectedloop,
                monthasint: kanbanfilterinfooptions.getselectedmonth,
            })
        })
        const data = await response.json();
        const { minleadtime, maxleadtime, avgleadtime } = data
        return { minleadtime, maxleadtime, avgleadtime }
    } catch(error){
        console.error(error)
        return { minleadtime: [], maxleadtime: [], avgleadtime: [] }
    }
}

export async function getleadtimebymatnrs(){

    const environmentsettingsoptions = environmentsettingsstore()
    const kanbanfilterinfooptions = kanbanfilterinfostore()

    console.log("kanbanfilterinfooptions.getmaterials():", kanbanfilterinfooptions.getmaterials())
    console.log("kanbanfilterinfooptions.getselectedloop():", kanbanfilterinfooptions.getselectedloop())
    console.log("kanbanfilterinfooptions.getselectedmonth():", kanbanfilterinfooptions.getselectedmonth())
    console.log("kanbanfilterinfooptions.getxaxisparameter():", kanbanfilterinfooptions.getxaxisparameter())

    try{
        const response = await fetch(environmentsettingsoptions.apimainpath + '/getleadtimebymatnrs',{
            method: 'POST',
            headers: { 'Content-type': 'application/json'},
            body: JSON.stringify({
                materials: kanbanfilterinfooptions.getmaterials(),
                loop: kanbanfilterinfooptions.getselectedloop(),
                monthasint: kanbanfilterinfooptions.getselectedmonth(),
                xaxisparameter: kanbanfilterinfooptions.getxaxisparameter()
            })
        })
        const data = await response.json()
        const { materials, leadtimes } = data;
        return { materials, leadtimes }
        //nach dem Import: const { materials, leadtimes } = await getleadtimebymatnrs();
    } catch(error){
        console.error(error)
        return { materials: [], leadtimes: [] }
    }
}

export async function getleadtimebyordernumber(){
    
}

export async function getrawdatafromdatabase(){

}
