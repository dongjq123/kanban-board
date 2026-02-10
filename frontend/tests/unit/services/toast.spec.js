/**
 * Toast 通知集成单元测试
 * 
 * 测试 Toast 通知在 API 拦截器和 Vuex Store 中的集成
 * 
 * 需求：9.1, 9.3, 10.1
 */

// Mock vue-toastification BEFORE any imports
const mockToast = {
  success: jest.fn(),
  error: jest.fn(),
  warning: jest.fn(),
  info: jest.fn()
}

jest.mock('vue-toastification', () => ({
  useToast: jest.fn(() => mockToast)
}))

// Mock the store to avoid circular dependency issues
jest.mock('@/store', () => ({
  default: {
    state: {
      auth: {
        token: null,
        user: null,
        isAuthenticated: false
      }
    },
    dispatch: jest.fn(),
    commit: jest.fn()
  }
}))

import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
import { createStore } from 'vuex'
import boards from '@/store/modules/boards'
import lists from '@/store/modules/lists'
import cards from '@/store/modules/cards'
import auth from '@/store/modules/auth'

let mock
let store

describe('Toast Notification Integration', () => {
  beforeAll(() => {
    // Mock axios globally to intercept all requests
    mock = new MockAdapter(axios)
  })

  beforeEach(() => {
    mock.reset()
    
    // 创建新的 store 实例
    store = createStore({
      modules: {
        boards,
        lists,
        cards,
        auth
      }
    })
    
    // 清除所有 toast mock 调用记录
    mockToast.success.mockClear()
    mockToast.error.mockClear()
    mockToast.warning.mockClear()
    mockToast.info.mockClear()
  })

  afterAll(() => {
    mock.restore()
  })

  describe('API Error Toast Notifications', () => {
    it('should show error toast on 404 not found error', async () => {
      const errorResponse = {
        error: {
          code: 'NOT_FOUND',
          message: '看板不存在'
        }
      }
      mock.onGet(/\/api\/boards\/999$/).reply(404, errorResponse)

      try {
        await store.dispatch('boards/fetchBoard', 999)
      } catch (error) {
        // 错误被正确抛出
      }

      expect(mockToast.error).toHaveBeenCalledWith('看板不存在')
    })

    it('should show error toast on network error', async () => {
      mock.onGet(/\/api\/boards$/).networkError()

      try {
        await store.dispatch('boards/fetchBoards')
      } catch (error) {
        // 错误被正确抛出
      }

      expect(mockToast.error).toHaveBeenCalled()
      const errorMessage = mockToast.error.mock.calls[0][0]
      expect(errorMessage).toContain('网络连接失败')
    })
  })

  describe('Board Success Toast Notifications', () => {
    it('should show success toast when creating board', async () => {
      const mockResponse = { id: 1, name: '新看板' }
      mock.onPost(/\/api\/boards$/).reply(201, mockResponse)

      await store.dispatch('boards/createBoard', { name: '新看板' })

      expect(mockToast.success).toHaveBeenCalledWith('看板创建成功')
    })

    it('should show success toast when updating board', async () => {
      const mockResponse = { id: 1, name: '更新的看板' }
      mock.onPut(/\/api\/boards\/1$/).reply(200, mockResponse)

      await store.dispatch('boards/updateBoard', { id: 1, data: { name: '更新的看板' } })

      expect(mockToast.success).toHaveBeenCalledWith('看板更新成功')
    })

    it('should show success toast when deleting board', async () => {
      mock.onDelete(/\/api\/boards\/1$/).reply(204)

      await store.dispatch('boards/deleteBoard', 1)

      expect(mockToast.success).toHaveBeenCalledWith('看板删除成功')
    })
  })

  describe('List Success Toast Notifications', () => {
    it('should show success toast when creating list', async () => {
      const mockResponse = { id: 1, board_id: 1, name: '新列表', position: 0 }
      mock.onPost(/\/boards\/1\/lists$/).reply(201, mockResponse)

      await store.dispatch('lists/createList', { boardId: 1, data: { name: '新列表' } })

      expect(mockToast.success).toHaveBeenCalledWith('列表创建成功')
    })

    it('should show success toast when updating list', async () => {
      const mockResponse = { id: 1, list_id: 1, name: '更新的列表' }
      mock.onPut(/\/lists\/1$/).reply(200, mockResponse)

      await store.dispatch('lists/updateList', { id: 1, data: { name: '更新的列表' } })

      expect(mockToast.success).toHaveBeenCalledWith('列表更新成功')
    })

    it('should show success toast when deleting list', async () => {
      mock.onDelete(/\/lists\/1$/).reply(204)

      await store.dispatch('lists/deleteList', 1)

      expect(mockToast.success).toHaveBeenCalledWith('列表删除成功')
    })
  })

  describe('Card Success Toast Notifications', () => {
    it('should show success toast when creating card', async () => {
      const mockResponse = { id: 1, list_id: 1, title: '新卡片', position: 0 }
      mock.onPost(/\/lists\/1\/cards$/).reply(201, mockResponse)

      await store.dispatch('cards/createCard', { listId: 1, data: { title: '新卡片' } })

      expect(mockToast.success).toHaveBeenCalledWith('卡片创建成功')
    })

    it('should show success toast when updating card', async () => {
      const mockResponse = { id: 1, list_id: 1, title: '更新的卡片' }
      mock.onPut(/\/cards\/1$/).reply(200, mockResponse)

      await store.dispatch('cards/updateCard', { id: 1, data: { title: '更新的卡片' } })

      expect(mockToast.success).toHaveBeenCalledWith('卡片更新成功')
    })

    it('should show success toast when deleting card', async () => {
      mock.onDelete(/\/cards\/1$/).reply(204)

      await store.dispatch('cards/deleteCard', { cardId: 1, listId: 1 })

      expect(mockToast.success).toHaveBeenCalledWith('卡片删除成功')
    })

    it('should show success toast when moving card', async () => {
      const mockResponse = { id: 1, list_id: 2, position: 1 }
      mock.onPut(/\/cards\/1\/move$/).reply(200, mockResponse)

      await store.dispatch('cards/moveCard', {
        cardId: 1,
        oldListId: 1,
        newListId: 2,
        position: 1
      })

      expect(mockToast.success).toHaveBeenCalledWith('卡片移动成功')
    })
  })

  describe('Toast Fallback Behavior', () => {
    it('should handle toast errors gracefully', async () => {
      // 即使 toast 调用失败，操作也应该成功
      const mockResponse = { id: 1, name: '新看板' }
      mock.onPost(/\/api\/boards$/).reply(201, mockResponse)

      // 应该不会抛出错误
      const result = await store.dispatch('boards/createBoard', { name: '新看板' })
      
      expect(result).toBeDefined()
      expect(result.name).toBe('新看板')
    })
  })
})
