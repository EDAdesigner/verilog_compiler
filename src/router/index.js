import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import CodeToImage from '../pages/CodeToImage.vue'
import CodeOptimization from '../pages/CodeOptimization.vue'
import About from '../pages/About.vue'
import ASAP from '../pages/ASAP.vue'
import ILP from '../pages/ILP.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/code-to-image',
    name: 'CodeToImage',
    component: CodeToImage
  },
  {
    path: '/code-optimization',
    name: 'CodeOptimization',
    component: CodeOptimization
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }, {
    path: '/asap',
    name: 'ASAP',
    component: ASAP
  }, {
    path: '/ilp',
    name: 'ilp',
    component: ILP
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router