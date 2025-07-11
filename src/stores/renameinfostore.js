import { ElMessage } from "element-plus";
import { defineStore } from "pinia";
import { ref } from 'vue';

export const renameinfostorage = defineStore('renameinfo', () => {

    const componentrenamings = ref({
        ncr: {originalname: "NCR", givenname: ""},
        changeofscrappermethod: {originalname: "Change of Scrap per method", givenname: ""},
        spoolscrapaccordingtocause: {originalname: "Spool scrap according to cause", givenname: ""},
        spoolscrapaccordingtomethod: {originalname: "Spool scrap according to method", givenname: ""},
        causeofscrapissue: {originalname: "Cause of scrap issue", givenname: ""},
        trendofmostexpensiveissues: {originalname: "Trend of most expensive issues", givenname: ""},
        spoolscrapfilteroptions: {originalname: "Spool scrap filter options", givenname: ""},
        pppartcasting: {originalname: "PP part - Casting", givenname: ""},
        pppartnotcasting: {originalname: "PP part - Not Casting", givenname: ""},
        p2ppart: {originalname: "P2P Part", givenname: ""},
    });

    const supplierrenamings = ref({
        hodgen: {shortname: "HIT", fullname: "Hodgen"},
        jiangsu: {shortname: "HJ", fullname: "Jiangsu"},
        king: {shortname: "KKHT", fullname: "Hodgen"},
        liaoning: {shortname: "SW", fullname: "Suzhou"},
        suzhou: {shortname: "CMS", fullname: "Suzhou"},
        india: {shortname: "Bosch India", fullname: "Bosch India"},
        xieyou: {shortname: "CZ Xieyou", fullname: "Changzhou xieyou packaging"},
        henggong: {shortname: "Henggong", fullname: "Hebei Henggong Precision"},
        würth: {shortname: "Würth", fullname: "Würth Industry Service"},
    });

    const materialrenamings = ref([
        ["NG10 Housing", "NG10 H."],
        ["NG10 Spool", "NG10 S."],
        ["NG16-1X Housing", "NG16-1X H."],
        ["NG6", "NG6"],
        ["NG6 Housing", "NG6 H."],
        ["NG6 Spool", "NG6 S."],
        ["PV", "PV"],
        ["PV Housing", "PV H."],
        ["SED6 Housing", "SED6 H."],
        ["SEW6", "SEW6"],
        ["WRKE16 Housing", "WRKE16 H."],
        ["WRKE27 Housing", "WRKE27 H."],
        ["WRZE10", "WRZE10"],
        ["WRZE10 Housing", "WRZE10 H."],
        ["WRZE16", "WRZE16"]
    ]);

    function addmaterialrenaming(materialname, newmaterialname) {
        materialrenamings.value.push([materialname, newmaterialname]);
    }

    function changematerialrenaming(materialname, newmaterialname) {
        for (const material of materialrenamings.value) {
            if (material[0] === materialname) {
                material[1] = newmaterialname;
            }
        }
    }

    function getmaterialrenaming(materialname) {
        for (const material of materialrenamings.value) {
            if (material[0] === materialname) {
                return material[1];
            }
        }
        return materialname;
    }

    function changecomponentname(originalname, givenname) {
        const key = Object.keys(componentrenamings.value).find(
            k => componentrenamings.value[k].originalname === originalname
        );
        if (!key) {
            console.warn("Kein Eintrag mit originalname", originalname, "gefunden");
            return;
        }
        componentrenamings.value[key].givenname = givenname;
        ElMessage.success(`Component name was changed from ${componentrenamings.value[key].originalname} to ${componentrenamings.value[key].givenname}`);
    }

    function getcomponentrenaming(componentname) {
        const entry = componentrenamings.value[componentname];
        if (!entry) {
            console.warn(`Kein Eintrag gefunden für componentname: ${componentname}`);
            return componentname; // fallback
        }

        return entry.givenname !== "" ? entry.givenname : entry.originalname;
    }

    function addsuppliershortname(originalname, newshortname) {
        if (originalname in supplierrenamings.value) {
            supplierrenamings.value[originalname].shortname = newshortname;
        }
    }

    function changesuppliershortname(originalname, newshortname) {
        if (originalname in supplierrenamings.value) {
            supplierrenamings.value[originalname].shortname = newshortname;
            ElMessage.success(`Supplier shortname changed to ${newshortname}`);
        } else {
            ElMessage.warning(`No supplier entry found for ${originalname}`);
        }
    }

    function getsuppliershortname(name) {
        for (const key in supplierrenamings.value) {
            if (name.toLowerCase().includes(key)) {
                return supplierrenamings.value[key].shortname;
            }
        }
        return name;
    }

    return {
        componentrenamings,
        supplierrenamings,
        materialrenamings,
        addsuppliershortname,
        changesuppliershortname,
        getsuppliershortname,
        addmaterialrenaming,
        changematerialrenaming,
        getmaterialrenaming,
        changecomponentname,
        getcomponentrenaming
    };

}, {
    persist: {
        storage: localStorage
    }
});


