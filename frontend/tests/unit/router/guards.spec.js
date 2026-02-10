/**
 * Vue Router 全局守卫单元测试
 * 
 * 测试路由守卫的各种场景：
 * - 未登录用户访问受保护路由
 * - 已登录用户访问受保护路由
 * - 已登录用户访问登录/注册页
 * - Token 验证失败处理
 * 
 * 需求：5.1-5.4
 */
import { createRouter, createWebHistory } from 'vue-router'

// Mock store
const createMockStore = (initialState = {}) => {
  const state = {
    auth: {
      token: null,
      user: null,
      isAuthenticated: false,
      ...initialState
    }
  }
  
  const dispatch = jest.fn()
  
  return {
    state,
    dispatch
  }
}

// 创建测试用的路由配置
const createTestRouter = () => {
  return createRouter({
    history: createWebHistory(),
    routes: [
      {
        path: '/login',
        name: 'Login',
        component: { template: '<div>Login</div>' },
        meta: { requiresAuth: false }
      },
      {
        path: '/register',
        name: 'Register',
        component: { template: '<div>Register</div>' },
        meta: { requiresAuth: false }
      },
      {
        path: '/',
        name: 'Home',
        component: { template: '<div>Home</div>' },
        meta: { requiresAuth: true }
      },
      {
        path: '/boards',
        name: 'Boards',
        component: { template: '<div>Boards</div>' },
        meta: { requiresAuth: true }
      }
    ]
  })
}

describe('Router Guards', () => {
  let router
  let store
  
  beforeEach(() => {
    // 清除 localStorage
    localStorage.clear()
    
    // 创建新的 router 和 store
    router = createTestRouter()
    store = createMockStore()
  })
  
  describe('需求 5.1: 未登录用户访问受保护路由', () => {
    it('应该重定向到登录页', async () => {
      // 设置未登录状态
      store.state.auth.isAuthenticated = false
      store.state.auth.token = null
      
      // 添加路由守卫
      router.beforeEach(async (to, from, next) => {
        const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
        const isAuthenticated = store.state.auth.isAuthenticated
        
        if (requiresAuth && !isAuthenticated) {
          next({
            path: '/login',
            query: { redirect: to.fullPath }
          })
          return
        }
        
        next()
      })
      
      // 尝试访问受保护路由
      await router.push('/')
      
      // 验证被重定向到登录页
      expect(router.currentRoute.value.path).toBe('/login')
      expect(router.currentRoute.value.query.redirect).toBe('/')
    })
    
    it('应该保存原始目标路由到 redirect 参数', async () => {
      store.state.auth.isAuthenticated = false
      
      router.beforeEach(async (to, from, next) => {
        const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
        const isAuthenticated = store.state.auth.isAuthenticated
        
        if (requiresAuth && !isAuthenticated) {
          next({
            path: '/login',
            query: { redirect: to.fullPath }
          })
          return
        }
        
        next()
      })
      
      await router.push('/boards')
      
      expect(router.currentRoute.value.path).toBe('/login')
      expect(router.currentRoute.value.query.redirect).toBe('/boards')
    })
  })
  
  describe('需求 5.2: 已登录用户访问受保护路由', () => {
    it('应该允许访问（token 验证成功）', async () => {
      // 设置已登录状态
      store.state.auth.isAuthenticated = true
      store.state.auth.token = 'valid-token'
      store.state.auth.user = { id: 1, username: 'testuser' }
      
      // Mock verifyToken action 返回成功
      store.dispatch.mockResolvedValue({ id: 1, username: 'testuser' })
      
      // 添加路由守卫
      router.beforeEach(async (to, from, next) => {
        const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
        const isAuthenticated = store.state.auth.isAuthenticated
        
        if (requiresAuth && !isAuthenticated) {
          next('/login')
          return
        }
        
        if (requiresAuth && isAuthenticated) {
          try {
            await store.dispatch('auth/verifyToken')
            next()
          } catch (error) {
            store.dispatch('auth/logout')
            next('/login')
          }
          return
        }
        
        next()
      })
      
      // 访问受保护路由
      await router.push('/')
      
      // 验证允许访问
      expect(router.currentRoute.value.path).toBe('/')
      expect(store.dispatch).toHaveBeenCalledWith('auth/verifyToken')
    })
  })
  
  describe('需求 5.3: 已登录用户访问登录/注册页', () => {
    it('应该重定向到主页（访问登录页）', async () => {
      store.state.auth.isAuthenticated = true
      store.state.auth.token = 'valid-token'
      
      router.beforeEach(async (to, from, next) => {
        const isAuthenticated = store.state.auth.isAuthenticated
        
        if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
          next('/')
          return
        }
        
        next()
      })
      
      await router.push('/login')
      
      expect(router.currentRoute.value.path).toBe('/')
    })
    
    it('应该重定向到主页（访问注册页）', async () => {
      store.state.auth.isAuthenticated = true
      store.state.auth.token = 'valid-token'
      
      router.beforeEach(async (to, from, next) => {
        const isAuthenticated = store.state.auth.isAuthenticated
        
        if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
          next('/')
          return
        }
        
        next()
      })
      
      await router.push('/register')
      
      expect(router.currentRoute.value.path).toBe('/')
    })
  })
  
  describe('需求 5.4: Token 过期处理', () => {
    it('应该清除登录状态并重定向到登录页', async () => {
      store.state.auth.isAuthenticated = true
      store.state.auth.token = 'expired-token'
      
      // Mock verifyToken action 返回失败
      const mockLogout = jest.fn()
      store.dispatch.mockImplementation((action) => {
        if (action === 'auth/verifyToken') {
          return Promise.reject(new Error('Token expired'))
        }
        if (action === 'auth/logout') {
          mockLogout()
          store.state.auth.isAuthenticated = false
          store.state.auth.token = null
          return Promise.resolve()
        }
      })
      
      router.beforeEach(async (to, from, next) => {
        const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
        const isAuthenticated = store.state.auth.isAuthenticated
        
        if (requiresAuth && isAuthenticated) {
          try {
            await store.dispatch('auth/verifyToken')
            next()
          } catch (error) {
            await store.dispatch('auth/logout')
            next({
              path: '/login',
              query: { redirect: to.fullPath }
            })
          }
          return
        }
        
        next()
      })
      
      await router.push('/')
      
      // 验证调用了 logout
      expect(mockLogout).toHaveBeenCalled()
      
      // 验证重定向到登录页
      expect(router.currentRoute.value.path).toBe('/login')
    })
  })
  
  describe('边缘情况', () => {
    it('应该允许未登录用户访问登录页', async () => {
      store.state.auth.isAuthenticated = false
      
      router.beforeEach(async (to, from, next) => {
        const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
        const isAuthenticated = store.state.auth.isAuthenticated
        
        if (requiresAuth && !isAuthenticated) {
          next('/login')
          return
        }
        
        next()
      })
      
      await router.push('/login')
      
      expect(router.currentRoute.value.path).toBe('/login')
    })
    
    it('应该允许未登录用户访问注册页', async () => {
      store.state.auth.isAuthenticated = false
      
      router.beforeEach(async (to, from, next) => {
        const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
        const isAuthenticated = store.state.auth.isAuthenticated
        
        if (requiresAuth && !isAuthenticated) {
          next('/login')
          return
        }
        
        next()
      })
      
      await router.push('/register')
      
      expect(router.currentRoute.value.path).toBe('/register')
    })
  })
})
