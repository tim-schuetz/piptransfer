import { createRouter, createWebHistory } from "vue-router";

import IcoPerformanceOverview from "./views/IcoPerformanceOverview.vue";
import QualityDashboard from "./views/QualityDashboard.vue";
import KanbanDashboard from "./views/KanbanDashboard.vue";
import KanbanDatenAnsicht from "./views/KanbanDatenAnsicht.vue";

const routes = [
    {path: '/', redirect: '/icoperformanceview'},
    {path: '/icoperformanceview', component: IcoPerformanceOverview},
    {path: '/kanbanview', component: KanbanDashboard},
    {path: '/qualityview', component: QualityDashboard},
    {path: '/kanbanalt', component: KanbanDatenAnsicht}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router

