import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/admin-login',
    name: 'admin-login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AdminLogin.vue')
  },
  {
    path: '/admin',
    name: 'admin',

    component: () => import(/* webpackChunkName: "about" */ '../views/AdminView.vue'),
    children: [
      {
        path: '/menu',
        name: 'menu',
    
        component: () => import(/* webpackChunkName: "about" */ '../views/MenuView.vue')
      },
      {
        path: '/order',
        name: 'order',
    
        component: () => import(/* webpackChunkName: "about" */ '../views/OrderView.vue')
      },
    ],
  },
  
]

const router = new VueRouter({
  routes
})

export default router
