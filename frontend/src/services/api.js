/**
 * API 服务模块
 * 
 * 提供前端与后端 API 通信的封装，包括：
 * - Axios 配置和实例创建
 * - 请求拦截器
 * - 响应拦截器和错误处理
 * - Toast 通知集成
 * - 所有 API 端点的调用函数
 * 
 * 需求：6.1, 9.1, 9.3, 10.1
 */
import axios from 'axios'
import toast from './toast'
import store from '@/store'

/**
 * Axios 实例配置
 * 
 * 配置说明：
 * - baseURL: API 基础 URL，开发环境指向本地后端服务器
 * - timeout: 请求超时时间（毫秒）
 * - headers: 默认请求头
 */
const apiClient = axios.create({
  // 开发环境：后端运行在 http://localhost:5000
  // 生产环境：通过 Nginx 代理，使用相对路径 /api
  baseURL: process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:5000/api',
  timeout: 10000, // 10 秒超时
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * 请求拦截器
 * 
 * 在请求发送前执行，可以：
 * - 添加认证令牌（如果需要）
 * - 修改请求配置
 * - 记录请求日志
 * 
 * 需求：3.1
 */
apiClient.interceptors.request.use(
  (config) => {
    // 在开发环境下记录请求信息
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Request] ${config.method.toUpperCase()} ${config.url}`, config.data)
    }
    
    // 添加认证令牌到请求头
    // 从 Vuex store 读取 token
    // 需求：3.1
    const token = store.state.auth.token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    // 请求配置错误
    console.error('[API Request Error]', error)
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 * 
 * 在响应返回后执行，可以：
 * - 统一处理响应数据格式
 * - 统一处理错误响应
 * - 显示 Toast 错误通知
 * - 处理 401 未授权错误（清除登录状态）
 * - 记录响应日志
 * 
 * 错误处理策略：
 * - 网络错误：显示网络连接失败提示
 * - 400 错误：显示验证错误信息
 * - 401 错误：清除登录状态，显示未授权提示
 * - 403 错误：显示无权访问提示
 * - 404 错误：显示资源不存在提示
 * - 500 错误：显示服务器错误提示
 * 
 * 需求：3.2-3.4, 9.2
 */
apiClient.interceptors.response.use(
  (response) => {
    // 在开发环境下记录响应信息
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Response] ${response.config.method.toUpperCase()} ${response.config.url}`, response.data)
    }
    
    // 直接返回响应对象，让调用者处理数据
    return response
  },
  (error) => {
    // 错误响应处理
    let errorMessage = '未知错误'
    let errorDetails = null
    
    if (!error.response) {
      // 网络错误：无法连接到服务器
      errorMessage = '网络连接失败，请检查网络设置或稍后重试'
      console.error('[API Network Error]', error.message)
    } else {
      // HTTP 错误响应
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          // 验证错误
          errorMessage = data.error?.message || data.message || '请求参数错误'
          errorDetails = data.error?.details
          console.error('[API Validation Error]', errorMessage, errorDetails)
          break
        
        case 401:
          // 未授权错误：令牌无效、过期或缺失
          // 需求：3.2-3.4
          errorMessage = data.error?.message || data.message || '登录已过期，请重新登录'
          console.error('[API Unauthorized Error]', errorMessage)
          
          // 清除登录状态
          // 需求：3.2
          store.dispatch('auth/logout')
          
          // TODO: 重定向到登录页面（需要等待 router 实现 - 任务 10.1）
          // 需求：3.2
          // router.push('/login')
          
          // 临时方案：在控制台提示需要重新登录
          console.warn('[Auth] User logged out due to 401 error. Redirect to login page when router is available.')
          break
        
        case 403:
          // 无权访问
          errorMessage = data.error?.message || data.message || '无权访问该资源'
          errorDetails = data.error?.details
          console.error('[API Forbidden Error]', errorMessage, errorDetails)
          break
          
        case 404:
          // 资源不存在
          errorMessage = data.error?.message || data.message || '请求的资源不存在'
          errorDetails = data.error?.details
          console.error('[API Not Found Error]', errorMessage, errorDetails)
          break
          
        case 500:
          // 服务器内部错误
          errorMessage = data.error?.message || data.message || '服务器错误，请稍后重试'
          console.error('[API Server Error]', errorMessage)
          break
          
        default:
          // 其他错误
          errorMessage = data.error?.message || data.message || `请求失败 (${status})`
          console.error('[API Error]', status, errorMessage)
      }
    }
    
    // 显示错误 Toast 通知
    // 需求：3.4, 9.2
    try {
      toast.error(errorMessage)
    } catch (toastError) {
      // Toast 初始化失败时的后备方案
      console.error('Failed to show toast notification:', toastError)
    }
    
    // 创建增强的错误对象
    const enhancedError = new Error(errorMessage)
    enhancedError.originalError = error
    enhancedError.status = error.response?.status
    enhancedError.details = errorDetails
    enhancedError.isNetworkError = !error.response
    
    return Promise.reject(enhancedError)
  }
)

/**
 * API 调用函数
 * 
 * 提供所有后端 API 端点的调用函数
 * 所有函数返回 Promise，包含 Axios 响应对象
 * 
 * 需求：1.1, 1.3, 1.4, 1.5, 2.1, 2.3, 2.4, 2.6, 3.1, 3.2, 3.4, 3.5, 4.1, 4.3
 */
const api = {
  // Auth API
  // 需求：1.1-1.6, 2.1-2.6, 3.1-3.4
  post(url, data) {
    return apiClient.post(url, data)
  },
  
  get(url) {
    return apiClient.get(url)
  },
  
  // Board API
  getBoards() {
    return apiClient.get('/boards')
  },
  
  getBoard(id) {
    return apiClient.get(`/boards/${id}`)
  },
  
  createBoard(data) {
    return apiClient.post('/boards', data)
  },
  
  updateBoard(id, data) {
    return apiClient.put(`/boards/${id}`, data)
  },
  
  deleteBoard(id) {
    return apiClient.delete(`/boards/${id}`)
  },
  
  // List API
  getLists(boardId) {
    return apiClient.get(`/boards/${boardId}/lists`)
  },
  
  getList(id) {
    return apiClient.get(`/lists/${id}`)
  },
  
  createList(boardId, data) {
    return apiClient.post(`/boards/${boardId}/lists`, data)
  },
  
  updateList(id, data) {
    return apiClient.put(`/lists/${id}`, data)
  },
  
  deleteList(id) {
    return apiClient.delete(`/lists/${id}`)
  },
  
  updateListPosition(id, data) {
    return apiClient.put(`/lists/${id}/position`, data)
  },
  
  // Card API
  getCards(listId) {
    return apiClient.get(`/lists/${listId}/cards`)
  },
  
  getCard(id) {
    return apiClient.get(`/cards/${id}`)
  },
  
  createCard(listId, data) {
    return apiClient.post(`/lists/${listId}/cards`, data)
  },
  
  updateCard(id, data) {
    return apiClient.put(`/cards/${id}`, data)
  },
  
  deleteCard(id) {
    return apiClient.delete(`/cards/${id}`)
  },
  
  moveCard(id, data) {
    return apiClient.put(`/cards/${id}/move`, data)
  }
}

// 导出 API 和 Toast 服务
export default api
export { toast, apiClient }
