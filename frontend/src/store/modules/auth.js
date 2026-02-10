/**
 * Auth Vuex 模块
 * 
 * 管理用户认证状态，包括：
 * - 用户登录/注册
 * - JWT 令牌管理
 * - localStorage 持久化
 * - 用户信息存储
 * 
 * 需求：2.1-2.6, 3.5
 */
import api from '@/services/api'

/**
 * State
 * 
 * 认证状态包括：
 * - token: JWT 令牌（从 localStorage 恢复）
 * - user: 用户信息对象（从 localStorage 恢复）
 * - isAuthenticated: 是否已认证（根据 token 是否存在计算）
 */
const state = {
  token: localStorage.getItem('token') || null,
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  isAuthenticated: !!localStorage.getItem('token')
}

/**
 * Mutations
 * 
 * 同步修改状态的方法
 */
const mutations = {
  /**
   * 设置 JWT 令牌
   * 
   * @param {Object} state - Vuex state
   * @param {string|null} token - JWT 令牌，null 表示清除
   * 
   * 行为：
   * - 更新 state.token
   * - 更新 state.isAuthenticated
   * - 同步到 localStorage（存储或删除）
   * 
   * 需求：2.1, 2.5, 3.5
   */
  SET_TOKEN(state, token) {
    state.token = token
    state.isAuthenticated = !!token
    
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  },
  
  /**
   * 设置用户信息
   * 
   * @param {Object} state - Vuex state
   * @param {Object|null} user - 用户信息对象，null 表示清除
   * 
   * 行为：
   * - 更新 state.user
   * - 同步到 localStorage（存储或删除）
   * 
   * 需求：2.1, 3.5
   */
  SET_USER(state, user) {
    state.user = user
    
    if (user) {
      localStorage.setItem('user', JSON.stringify(user))
    } else {
      localStorage.removeItem('user')
    }
  },
  
  /**
   * 登出（清除所有认证信息）
   * 
   * @param {Object} state - Vuex state
   * 
   * 行为：
   * - 清除 state.token
   * - 清除 state.user
   * - 设置 state.isAuthenticated 为 false
   * - 从 localStorage 删除所有认证信息
   * 
   * 需求：3.5
   */
  LOGOUT(state) {
    state.token = null
    state.user = null
    state.isAuthenticated = false
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
}

/**
 * Actions
 * 
 * 异步操作和业务逻辑
 */
const actions = {
  /**
   * 用户注册
   * 
   * @param {Object} context - Vuex action context
   * @param {Object} payload - 注册信息
   * @param {string} payload.username - 用户名（3-50 字符）
   * @param {string} payload.email - 邮箱地址
   * @param {string} payload.password - 密码（至少 8 字符）
   * @returns {Promise<Object>} 创建的用户信息
   * @throws {Error} 验证失败或服务器错误
   * 
   * 行为：
   * - 调用 POST /api/auth/register
   * - 返回用户信息（不自动登录）
   * - 抛出错误如果注册失败
   * 
   * 需求：1.1-1.6
   */
  async register(context, { username, email, password }) {
    const response = await api.post('/auth/register', {
      username,
      email,
      password
    })
    
    // 注册成功，返回用户信息
    // 注意：不自动登录，用户需要手动登录
    return response.data.user
  },
  
  /**
   * 用户登录
   * 
   * @param {Object} context - Vuex action context
   * @param {Object} payload - 登录信息
   * @param {string} payload.identifier - 邮箱或用户名
   * @param {string} payload.password - 密码
   * @returns {Promise<Object>} 用户信息和令牌
   * @throws {Error} 认证失败或服务器错误
   * 
   * 行为：
   * - 调用 POST /api/auth/login
   * - 保存 token 到 state 和 localStorage
   * - 保存 user 到 state 和 localStorage
   * - 设置 isAuthenticated 为 true
   * 
   * 需求：2.1-2.6
   */
  async login({ commit }, { identifier, password }) {
    const response = await api.post('/auth/login', {
      identifier,
      password
    })
    
    const { token, user } = response.data
    
    // 保存认证信息到 state 和 localStorage
    commit('SET_TOKEN', token)
    commit('SET_USER', user)
    
    return { token, user }
  },
  
  /**
   * 验证令牌有效性
   * 
   * @param {Object} context - Vuex action context
   * @returns {Promise<Object>} 用户信息
   * @throws {Error} 令牌无效或过期
   * 
   * 行为：
   * - 调用 GET /api/auth/verify（需要 Authorization header）
   * - 如果令牌有效，更新用户信息
   * - 如果令牌无效，清除认证状态
   * 
   * 需求：3.1-3.4
   */
  async verifyToken({ commit, state }) {
    // 如果没有 token，直接返回失败
    if (!state.token) {
      commit('LOGOUT')
      throw new Error('未登录')
    }
    
    try {
      const response = await api.get('/auth/verify')
      
      const { user } = response.data
      
      // 更新用户信息（token 不变）
      commit('SET_USER', user)
      
      return user
    } catch (error) {
      // 令牌无效或过期，清除认证状态
      commit('LOGOUT')
      throw error
    }
  },
  
  /**
   * 用户登出
   * 
   * @param {Object} context - Vuex action context
   * 
   * 行为：
   * - 清除 token 和 user
   * - 清除 localStorage
   * - 设置 isAuthenticated 为 false
   * 
   * 需求：3.5
   */
  logout({ commit }) {
    commit('LOGOUT')
  }
}

/**
 * Getters
 * 
 * 计算属性和状态访问器
 */
const getters = {
  /**
   * 获取当前用户信息
   */
  currentUser: state => state.user,
  
  /**
   * 获取认证状态
   */
  isAuthenticated: state => state.isAuthenticated,
  
  /**
   * 获取 JWT 令牌
   */
  token: state => state.token,
  
  /**
   * 获取用户 ID（如果已登录）
   */
  userId: state => state.user?.id || null,
  
  /**
   * 获取用户名（如果已登录）
   */
  username: state => state.user?.username || null
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
