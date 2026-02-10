/**
 * Vue Router 配置
 * 
 * 定义应用程序的路由和导航守卫
 * 
 * 需求：5.1-5.4
 */
import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

/**
 * 路由定义
 * 
 * meta.requiresAuth: true 表示该路由需要认证才能访问
 */
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/boards',
    name: 'Boards',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/boards/:id',
    name: 'BoardDetail',
    component: () => import('@/views/BoardDetail.vue'),
    meta: { requiresAuth: true }
  }
]

/**
 * 创建路由实例
 */
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

/**
 * 全局前置守卫
 * 
 * 实现以下功能：
 * 1. 检查路由是否需要认证（meta.requiresAuth）
 * 2. 未登录用户访问受保护路由时重定向到登录页
 * 3. 已登录用户访问登录/注册页时重定向到主页
 * 4. 验证 token 有效性
 * 
 * 需求：5.1-5.4
 */
router.beforeEach(async (to, from, next) => {
  // 检查路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  // 获取当前认证状态
  const isAuthenticated = store.state.auth.isAuthenticated
  
  // 场景 1：访问受保护的路由但未登录
  // 需求：5.1 - 未登录用户尝试访问受保护的路由 THEN 前端路由守卫 SHALL 重定向用户到登录页面
  if (requiresAuth && !isAuthenticated) {
    console.log('[Router Guard] 未登录用户尝试访问受保护路由，重定向到登录页')
    next({
      path: '/login',
      query: { redirect: to.fullPath } // 保存原始目标路由，登录后可以跳转回去
    })
    return
  }
  
  // 场景 2：已登录用户访问登录或注册页
  // 需求：5.3 - 已登录用户访问登录或注册页面 THEN 前端路由守卫 SHALL 重定向用户到主页
  if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    console.log('[Router Guard] 已登录用户访问登录/注册页，重定向到主页')
    next('/')
    return
  }
  
  // 场景 3：已登录用户访问受保护路由，验证 token 有效性
  // 需求：5.2 - 已登录用户访问受保护的路由 THEN 前端路由守卫 SHALL 允许访问
  // 需求：5.4 - 用户的会话令牌过期 THEN 前端路由守卫 SHALL 清除本地存储并重定向到登录页面
  if (requiresAuth && isAuthenticated) {
    try {
      // 验证 token 是否仍然有效
      await store.dispatch('auth/verifyToken')
      console.log('[Router Guard] Token 验证成功，允许访问')
      next()
    } catch (error) {
      // Token 无效或过期
      console.log('[Router Guard] Token 验证失败，清除登录状态并重定向到登录页')
      
      // 清除本地存储和认证状态
      store.dispatch('auth/logout')
      
      // 重定向到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }
    return
  }
  
  // 场景 4：访问不需要认证的路由（如登录、注册页）
  next()
})

export default router
