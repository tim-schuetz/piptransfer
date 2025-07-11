
const apiKeyCn = '138702f4-da0f-4404-8a52-5a76d6f78003'
const endpointCn = 'https://ews-esz-emea.api.bosch.com/manufacturing/production-order/RB9S-PEX_PRORD_SRV/PRP/v2/'

// const plant_cn = 'CN50'
// const material_cn = 'R988114969'
// const workcenter_cn = '523246N' / 530133N

// const api_key_cn_qrp = '240270ef-9b4f-473c-88f7-e56d13b8658b'
// const endpoint_cn_qrp = 'https://ews-esz-emea.api.bosch.com/manufacturing/production-order/RB9S-PEX_PRORD_SRV/QRP/v2/'

// const materialnummerinfos_url = "{endpoint_cn}A_ProductionOrder?$filter=ProductionPlant eq '{plant_cn}' and Material eq '{material_cn}'&$top=3"
// const nachbausfc015_url = "{endpoint_cn}A_ProductionOrderOperation?$filter=WorkCenter eq '{workcenter_cn}'&$top=3"


export async function fetchmaterialsfromsap(workCenterNumber) {

    const latestMatnrsURL = `${endpointCn}A_ProductionOrderOperation?` +
        `$filter=WorkCenter eq '${workCenterNumber}' and OpActualExecutionStartDate ge datetime'2024-01-01T00:00:00'&` +
        `$top=50`;

    const headers = {
        'KeyId': apiKeyCn,
        'Accept': 'application/json',
        'SAP-language': 'EN'
    };

    try {
        const response = await fetch(latestMatnrsURL, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            console.error(`Fehler bei SAP Abfrage: ${response.status} - ${await response.text()}`);
            return [];
        }

        const data = await response.json();

        if (!data?.d?.results || data.d.results.length === 0) {
            console.error("Empty response");
            return [];
        }

        const orders = data.d.results.map(entry => entry.ManufacturingOrder);

        const materialPromises = orders.map(async (order) => {
            const orderUrl = `${endpointCn}A_ProductionOrderItem?$filter=ManufacturingOrder eq '${order}'&$top=1`;

            const orderResponse = await fetch(orderUrl, {
                method: 'GET',
                headers: headers
            });

            const orderData = await orderResponse.json();
            return orderData?.d?.results?.[0]?.Material || null;
        });

        const materials = await Promise.all(materialPromises);
        const uniqueMaterialList = [...new Set(materials.filter(Boolean))];

        return uniqueMaterialList;

    } catch (error) {
        console.error("Fehler beim Abrufen der Materialien:", error);
        return [];
    }
}

export async function fetchcurrentorder(workCenterNumber) {

    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const todayAsString = `${year}-${month}-${day}`;

    const latestMatnrsURL = `${endpointCn}A_ProductionOrderOperation?` +
        `$filter=WorkCenter eq '${workCenterNumber}' and OpActualExecutionStartDate eq datetime'${todayAsString}T00:00:00'&` +
        `$orderby=OpErlstSchedldExecStrtTme&` +
        `$top=1`;

    const headers = {
        'KeyId': apiKeyCn,
        'Accept': 'application/json',
        'SAP-language': 'EN'
    };

    try {
        const response = await fetch(latestMatnrsURL, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            console.error(`Fehler bei SAP Abfrage: ${response.status} - ${await response.text()}`);
            return { ordernumber: '-', plannedduration: '-' };
        }

        const data = await response.json();
        const results = data?.d?.results;

        if (results && results.length > 0) {
            return {
                ordernumber: results[0].ManufacturingOrder,
                plannedduration: results[0].OpPlannedProcessingDurn
            };
        } else {
            return { ordernumber: '-', plannedduration: '-' };
        }

    } catch (error) {
        console.error("Fehler beim Abrufen des aktuellen Auftrags:", error);
        return { ordernumber: '-', plannedduration: '-' };
    }
}

export async function fetchtodaysoutput(workCenterNumber) {

    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const todayAsString = `${year}-${month}-${day}`;

    const todaysMatnrsURL = `${endpointCn}A_ProductionOrderOperation?` +
        `$filter=WorkCenter eq '${workCenterNumber}' and OpActualExecutionStartDate ge datetime'${todayAsString}T00:00:00'`;

    const headers = {
        'KeyId': apiKeyCn,
        'Accept': 'application/json',
        'SAP-language': 'EN'
    };

    try {
        const response = await fetch(todaysMatnrsURL, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            console.error(`Fehler bei SAP Abfrage: ${response.status} - ${await response.text()}`);
            return 0;
        }

        const data = await response.json();
        const contents = data?.d?.results || [];

        let amount = 0;
        for (const content of contents) {
            const qty = parseInt(content.OpTotalConfirmedYieldQty);
            if (!isNaN(qty)) {
                amount += qty;
            }
        }

        return amount;

    } catch (error) {
        console.error("Fehler beim Abrufen der Tagesausgabe:", error);
        return 0;
    }
}

export async function fetchrecentordersoverview(workCenterNumber) {

    // Gestern's Datum im Format YYYY-MM-DD
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const year = yesterday.getFullYear();
    const month = String(yesterday.getMonth() + 1).padStart(2, '0');
    const day = String(yesterday.getDate()).padStart(2, '0');
    const yesterdayAsString = `${year}-${month}-${day}`;

    const latestMatnrsURL = `${endpointCn}A_ProductionOrderOperation?` +
        `$filter=WorkCenter eq '${workCenterNumber}' and OpActualExecutionStartDate ge datetime'${yesterdayAsString}T00:00:00'&` +
        `$orderby=OpActualExecutionStartDate&` +
        `$top=30`;

    const headers = {
        'KeyId': apiKeyCn,
        'Accept': 'application/json',
        'SAP-language': 'EN'
    };

    try {
        const response = await fetch(latestMatnrsURL, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            console.error(`Fehler bei SAP Abfrage: ${response.status} - ${await response.text()}`);
            return [];
        }

        const data = await response.json();
        const contents = data?.d?.results || [];
        const mostRecentOrdersInfo = [];

        for (const content of contents) {
            const startRaw = content.OpActualExecutionStartTime; // z.B. "PT20H16M08S"
            const endRaw = content.OpActualExecutionEndTime;

            const startTimeObj = sapDurationToDate(startRaw);
            const endTimeObj = sapDurationToDate(endRaw);

            const actualDuration = startTimeObj && endTimeObj
                ? Number(((endTimeObj - startTimeObj) / 3600000).toFixed(2))
                : 0;

            mostRecentOrdersInfo.push({
                ordernumber: content.ManufacturingOrder,
                plannedprocesduration: content.OpPlannedProcessingDurn,
                actualduration: actualDuration,
                quantity: content.OpTotalConfirmedYieldQty,
                starttime: formatTime(startRaw),
                endtime: formatTime(endRaw)
            });
        }

        return mostRecentOrdersInfo;

    } catch (error) {
        console.error("Fehler beim Abrufen der Auftragsübersicht:", error);
        return [];
    }
}

// z.B. "PT20H16M08S" → Date-Objekt an einem Dummy-Tag
function sapDurationToDate(durationString) {
    if (!durationString || !durationString.startsWith("PT")) return null;
    const hours = parseInt(durationString.substring(2, 4)) || 0;
    const minutes = parseInt(durationString.substring(5, 7)) || 0;
    const seconds = parseInt(durationString.substring(8, 10)) || 0;
    return new Date(2000, 0, 1, hours, minutes, seconds);
}

// z.B. "PT20H16M08S" → "20:16:08"
function formatTime(durationString) {
    if (!durationString || !durationString.startsWith("PT")) return "--:--:--";
    const h = durationString.substring(2, 4);
    const m = durationString.substring(5, 7);
    const s = durationString.substring(8, 10);
    return `${h}:${m}:${s}`;
}


