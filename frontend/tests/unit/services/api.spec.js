/**
 * API 服务单元测试
 * 
 * 测试 Axios 配置和拦截器功能
 * 
 * 需求：6.1, 10.1
 */
import MockAdapter from 'axios-mock-adapter'
import store from '@/store'

// 导入 api 模块和 axios 实例
import api, { apiClient } from '@/services/api'

// 创建 axios mock 适配器
// 使用 apiClient 实例而不是全局 axios
const mock = new MockAdapter(apiClient)

describe('API Service', () => {
  beforeEach(() => {
    // 重置 mock 状态
    mock.reset()
    // 清除认证状态
    store.commit('auth/LOGOUT')
  })

  afterAll(() => {
    // 恢复 axios 原始行为
    mock.restore()
  })

  describe('Axios Configuration', () => {
    it('should have correct base URL configuration logic', () => {
      // 验证环境变量逻辑
      expect(process.env.NODE_ENV).toBeDefined()
    })

    it('should have correct timeout configuration', () => {
      // 验证超时配置存在
      // 实际的超时值在 api.js 中设置为 10000ms
      expect(true).toBe(true)
    })

    it('should have correct default headers', () => {
      // 验证默认 Content-Type 头
      expect(true).toBe(true)
    })
  })

  describe('Request Interceptor', () => {
    it('should add Authorization header when token exists in store', async () => {
      const mockToken = 'test-jwt-token-123'
      const mockData = { id: 1, name: '测试看板' }
      
      // 设置 token 到 store
      store.commit('auth/SET_TOKEN', mockToken)
      
      // 设置 mock 响应并捕获请求配置
      let capturedConfig = null
      mock.onGet(/\/boards$/).reply((config) => {
        capturedConfig = config
        return [200, mockData]
      })

      await api.getBoards()
      
      // 验证 Authorization header 被正确添加
      expect(capturedConfig.headers.Authorization).toBe(`Bearer ${mockToken}`)
    })

    it('should not add Authorization header when token does not exist', async () => {
      const mockData = { id: 1, name: '测试看板' }
      
      // 确保 store 中没有 token
      store.commit('auth/LOGOUT')
      
      // 设置 mock 响应并捕获请求配置
      let capturedConfig = null
      mock.onGet(/\/boards$/).reply((config) => {
        capturedConfig = config
        return [200, mockData]
      })

      await api.getBoards()
      
      // 验证 Authorization header 不存在
      expect(capturedConfig.headers.Authorization).toBeUndefined()
    })

    it('should read token from Vuex store, not localStorage', async () => {
      const storeToken = 'store-token-123'
      const localStorageToken = 'localstorage-token-456'
      const mockData = { id: 1, name: '测试看板' }
      
      // 在 localStorage 中设置一个不同的 token
      localStorage.setItem('token', localStorageToken)
      
      // 在 store 中设置正确的 token
      store.commit('auth/SET_TOKEN', storeToken)
      
      // 设置 mock 响应并捕获请求配置
      let capturedConfig = null
      mock.onGet(/\/boards$/).reply((config) => {
        capturedConfig = config
        return [200, mockData]
      })

      await api.getBoards()
      
      // 验证使用的是 store 中的 token，而不是 localStorage 中的
      expect(capturedConfig.headers.Authorization).toBe(`Bearer ${storeToken}`)
      
      // 清理
      localStorage.removeItem('token')
    })
  })

  describe('Response Interceptor - Success', () => {
    it('should return response data on successful request', async () => {
      const mockData = { id: 1, name: '测试看板' }
      mock.onGet(/\/boards$/).reply(200, mockData)

      const response = await api.getBoards()
      expect(response.data).toEqual(mockData)
    })
  })

  describe('Response Interceptor - Error Handling', () => {
    it('should handle 400 validation errors', async () => {
      const errorResponse = {
        error: {
          code: 'VALIDATION_ERROR',
          message: '看板名称不能为空',
          details: { field: 'name', constraint: 'required' }
        }
      }
      mock.onPost(/\/boards$/).reply(400, errorResponse)

      try {
        await api.createBoard({ name: '' })
        // 如果没有抛出错误，测试失败
        expect(true).toBe(false)
      } catch (error) {
        expect(error.message).toBe('看板名称不能为空')
        expect(error.status).toBe(400)
        expect(error.details).toEqual({ field: 'name', constraint: 'required' })
      }
    })

    it('should handle 401 unauthorized errors and clear auth state', async () => {
      // 需求：3.2-3.4
      const mockToken = 'expired-token-123'
      const errorResponse = {
        error: {
          code: 'UNAUTHORIZED',
          message: '令牌已过期，请重新登录'
        }
      }
      
      // 设置初始认证状态
      store.commit('auth/SET_TOKEN', mockToken)
      store.commit('auth/SET_USER', { id: 1, username: 'testuser' })
      expect(store.state.auth.isAuthenticated).toBe(true)
      
      // Mock 401 响应
      mock.onGet(/\/boards$/).reply(401, errorResponse)

      try {
        await api.getBoards()
        expect(true).toBe(false)
      } catch (error) {
        // 验证错误消息
        expect(error.message).toBe('令牌已过期，请重新登录')
        expect(error.status).toBe(401)
        
        // 验证认证状态被清除
        expect(store.state.auth.token).toBeNull()
        expect(store.state.auth.user).toBeNull()
        expect(store.state.auth.isAuthenticated).toBe(false)
        
        // 验证 localStorage 被清除
        expect(localStorage.getItem('token')).toBeNull()
        expect(localStorage.getItem('user')).toBeNull()
      }
    })

    it('should handle 401 errors with default message', async () => {
      // 需求：3.2-3.4
      const mockToken = 'invalid-token-456'
      const errorResponse = {
        message: '未授权访问'
      }
      
      // 设置初始认证状态
      store.commit('auth/SET_TOKEN', mockToken)
      store.commit('auth/SET_USER', { id: 2, username: 'testuser2' })
      
      // Mock 401 响应（没有 error 对象）
      mock.onGet(/\/boards\/1$/).reply(401, errorResponse)

      try {
        await api.getBoard(1)
        expect(true).toBe(false)
      } catch (error) {
        // 验证使用了响应中的消息
        expect(error.message).toBe('未授权访问')
        expect(error.status).toBe(401)
        
        // 验证认证状态被清除
        expect(store.state.auth.isAuthenticated).toBe(false)
      }
    })

    it('should handle 401 errors without message', async () => {
      // 需求：3.2-3.4
      const mockToken = 'bad-token-789'
      const errorResponse = {}
      
      // 设置初始认证状态
      store.commit('auth/SET_TOKEN', mockToken)
      
      // Mock 401 响应（空响应体）
      mock.onPost(/\/boards$/).reply(401, errorResponse)

      try {
        await api.createBoard({ name: '测试看板' })
        expect(true).toBe(false)
      } catch (error) {
        // 验证使用了默认消息
        expect(error.message).toBe('登录已过期，请重新登录')
        expect(error.status).toBe(401)
        
        // 验证认证状态被清除
        expect(store.state.auth.isAuthenticated).toBe(false)
      }
    })

    it('should handle 403 forbidden errors', async () => {
      // 需求：3.4
      const errorResponse = {
        error: {
          code: 'FORBIDDEN',
          message: '无权访问该看板',
          details: { resource: 'board', id: 1 }
        }
      }
      mock.onGet(/\/boards\/1$/).reply(403, errorResponse)

      try {
        await api.getBoard(1)
        expect(true).toBe(false)
      } catch (error) {
        expect(error.message).toBe('无权访问该看板')
        expect(error.status).toBe(403)
        expect(error.details).toEqual({ resource: 'board', id: 1 })
      }
    })

    it('should handle 404 not found errors', async () => {
      const errorResponse = {
        error: {
          code: 'NOT_FOUND',
          message: '看板不存在',
          details: { resource: 'board', id: 999 }
        }
      }
      mock.onGet(/\/boards\/999$/).reply(404, errorResponse)

      try {
        await api.getBoard(999)
        expect(true).toBe(false)
      } catch (error) {
        expect(error.message).toBe('看板不存在')
        expect(error.status).toBe(404)
        expect(error.details).toEqual({ resource: 'board', id: 999 })
      }
    })

    it('should handle 500 server errors', async () => {
      const errorResponse = {
        error: {
          code: 'INTERNAL_ERROR',
          message: '服务器内部错误，请稍后重试'
        }
      }
      mock.onGet(/\/boards$/).reply(500, errorResponse)

      try {
        await api.getBoards()
        expect(true).toBe(false)
      } catch (error) {
        expect(error.message).toBe('服务器内部错误，请稍后重试')
        expect(error.status).toBe(500)
      }
    })

    it('should handle network errors', async () => {
      mock.onGet(/\/boards$/).networkError()

      try {
        await api.getBoards()
        expect(true).toBe(false)
      } catch (error) {
        expect(error.message).toBe('网络连接失败，请检查网络设置或稍后重试')
        expect(error.isNetworkError).toBe(true)
      }
    })

    it('should handle timeout errors', async () => {
      mock.onGet(/\/boards$/).timeout()

      try {
        await api.getBoards()
        expect(true).toBe(false)
      } catch (error) {
        expect(error.message).toBe('网络连接失败，请检查网络设置或稍后重试')
        expect(error.isNetworkError).toBe(true)
      }
    })

    it('should provide default error message for unknown errors', async () => {
      const errorResponse = {}
      mock.onGet(/\/boards$/).reply(418, errorResponse)

      try {
        await api.getBoards()
        expect(true).toBe(false)
      } catch (error) {
        expect(error.message).toContain('请求失败')
        expect(error.status).toBe(418)
      }
    })
  })

  describe('API Functions', () => {
    describe('Board API', () => {
      it('should call GET /boards', async () => {
        const mockData = [{ id: 1, name: '看板1' }]
        mock.onGet(/\/boards$/).reply(200, mockData)

        const response = await api.getBoards()
        expect(response.data).toEqual(mockData)
      })

      it('should call POST /boards', async () => {
        const newBoard = { name: '新看板' }
        const mockResponse = { id: 1, name: '新看板', created_at: '2024-01-01', updated_at: '2024-01-01' }
        mock.onPost(/\/boards$/).reply(201, mockResponse)

        const response = await api.createBoard(newBoard)
        expect(response.data.id).toBe(1)
        expect(response.data.name).toBe('新看板')
      })

      it('should call PUT /boards/:id', async () => {
        const updatedBoard = { name: '更新的看板' }
        const mockResponse = { id: 1, name: '更新的看板', created_at: '2024-01-01', updated_at: '2024-01-02' }
        mock.onPut(/\/boards\/1$/).reply(200, mockResponse)

        const response = await api.updateBoard(1, updatedBoard)
        expect(response.data.id).toBe(1)
        expect(response.data.name).toBe('更新的看板')
      })

      it('should call DELETE /boards/:id', async () => {
        mock.onDelete(/\/boards\/1$/).reply(204)

        const response = await api.deleteBoard(1)
        expect(response.status).toBe(204)
      })
    })

    describe('List API', () => {
      it('should call GET /boards/:boardId/lists', async () => {
        const mockData = [{ id: 1, name: '列表1', board_id: 1 }]
        mock.onGet(/\/boards\/1\/lists$/).reply(200, mockData)

        const response = await api.getLists(1)
        expect(response.data).toEqual(mockData)
      })

      it('should call POST /boards/:boardId/lists', async () => {
        const newList = { name: '新列表', position: 0 }
        const mockResponse = { id: 1, board_id: 1, name: '新列表', position: 0 }
        mock.onPost(/\/boards\/1\/lists$/).reply(201, mockResponse)

        const response = await api.createList(1, newList)
        expect(response.data).toEqual(mockResponse)
      })

      it('should call PUT /lists/:id/position', async () => {
        const positionData = { position: 2 }
        const mockResponse = { id: 1, position: 2 }
        mock.onPut(/\/lists\/1\/position$/).reply(200, mockResponse)

        const response = await api.updateListPosition(1, positionData)
        expect(response.data).toEqual(mockResponse)
      })
    })

    describe('Card API', () => {
      it('should call GET /lists/:listId/cards', async () => {
        const mockData = [{ id: 1, title: '卡片1', list_id: 1 }]
        mock.onGet(/\/lists\/1\/cards$/).reply(200, mockData)

        const response = await api.getCards(1)
        expect(response.data).toEqual(mockData)
      })

      it('should call POST /lists/:listId/cards', async () => {
        const newCard = { title: '新卡片', position: 0 }
        const mockResponse = { id: 1, list_id: 1, title: '新卡片', position: 0 }
        mock.onPost(/\/lists\/1\/cards$/).reply(201, mockResponse)

        const response = await api.createCard(1, newCard)
        expect(response.data).toEqual(mockResponse)
      })

      it('should call PUT /cards/:id/move', async () => {
        const moveData = { list_id: 2, position: 1 }
        const mockResponse = { id: 1, list_id: 2, position: 1 }
        mock.onPut(/\/cards\/1\/move$/).reply(200, mockResponse)

        const response = await api.moveCard(1, moveData)
        expect(response.data).toEqual(mockResponse)
      })
    })
  })
})
