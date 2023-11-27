import { createRouter, createWebHistory } from 'vue-router';
import Home from './Pages/Home.vue'
import Timeline from './Pages/Timeline.vue'

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/timeline',
        component: Timeline
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
