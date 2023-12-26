import { createRouter, createWebHistory } from 'vue-router';
import Home from './Pages/Home.vue'
import Timeline from './Pages/Timeline.vue'

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/LB-X-LR-LITERALLY-US-TIMELINE',
        component: Timeline
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
