// Boards store tests
import { createStore } from 'vuex'
import boards from '@/store/modules/boards'
import api from '@/services/api'

// Mock the API module
jest.mock('@/services/api')

describe('boards store module', () => {
  let store

  beforeEach(() => {
    // Create a fresh store instance for each test
    store = createStore({
      modules: {
        boards: {
          ...boards,
          namespaced: true
        }
      }
    })
    // Clear all mocks
    jest.clearAllMocks()
  })

  describe('mutations', () => {
    it('setBoards should set the boards array', () => {
      const testBoards = [
        { id: 1, name: 'Board 1' },
        { id: 2, name: 'Board 2' }
      ]
      store.commit('boards/setBoards', testBoards)
      expect(store.state.boards.boards).toEqual(testBoards)
    })

    it('addBoard should add a board to the array', () => {
      // Clear any existing boards first
      store.commit('boards/setBoards', [])
      
      const newBoard = { id: 1, name: 'New Board' }
      store.commit('boards/addBoard', newBoard)
      expect(store.state.boards.boards).toContainEqual(newBoard)
      expect(store.state.boards.boards.length).toBe(1)
    })

    it('updateBoard should update an existing board', () => {
      const initialBoards = [
        { id: 1, name: 'Board 1' },
        { id: 2, name: 'Board 2' }
      ]
      store.commit('boards/setBoards', initialBoards)
      
      const updatedBoard = { id: 1, name: 'Updated Board 1' }
      store.commit('boards/updateBoard', updatedBoard)
      
      expect(store.state.boards.boards[0]).toEqual(updatedBoard)
      expect(store.state.boards.boards[1]).toEqual(initialBoards[1])
    })

    it('updateBoard should update currentBoard if it matches', () => {
      const board = { id: 1, name: 'Board 1' }
      store.commit('boards/setCurrentBoard', board)
      
      const updatedBoard = { id: 1, name: 'Updated Board 1' }
      store.commit('boards/updateBoard', updatedBoard)
      
      expect(store.state.boards.currentBoard).toEqual(updatedBoard)
    })

    it('deleteBoard should remove a board from the array', () => {
      const initialBoards = [
        { id: 1, name: 'Board 1' },
        { id: 2, name: 'Board 2' }
      ]
      store.commit('boards/setBoards', initialBoards)
      
      store.commit('boards/deleteBoard', 1)
      
      expect(store.state.boards.boards.length).toBe(1)
      expect(store.state.boards.boards[0].id).toBe(2)
    })

    it('deleteBoard should clear currentBoard if it matches', () => {
      const board = { id: 1, name: 'Board 1' }
      store.commit('boards/setCurrentBoard', board)
      
      store.commit('boards/deleteBoard', 1)
      
      expect(store.state.boards.currentBoard).toBeNull()
    })

    it('setCurrentBoard should set the current board', () => {
      const board = { id: 1, name: 'Board 1' }
      store.commit('boards/setCurrentBoard', board)
      expect(store.state.boards.currentBoard).toEqual(board)
    })

    it('setLoading should set the loading state', () => {
      store.commit('boards/setLoading', true)
      expect(store.state.boards.loading).toBe(true)
      
      store.commit('boards/setLoading', false)
      expect(store.state.boards.loading).toBe(false)
    })

    it('setError should set the error state', () => {
      const errorMessage = 'Test error'
      store.commit('boards/setError', errorMessage)
      expect(store.state.boards.error).toBe(errorMessage)
    })
  })

  describe('actions', () => {
    describe('fetchBoards', () => {
      it('should fetch boards successfully', async () => {
        const mockBoards = [
          { id: 1, name: 'Board 1' },
          { id: 2, name: 'Board 2' }
        ]
        // Backend returns { boards: [...] }
        api.getBoards.mockResolvedValue({ data: { boards: mockBoards } })

        await store.dispatch('boards/fetchBoards')

        expect(api.getBoards).toHaveBeenCalled()
        expect(store.state.boards.boards).toEqual(mockBoards)
        expect(store.state.boards.loading).toBe(false)
        expect(store.state.boards.error).toBeNull()
      })

      it('should handle fetch boards error', async () => {
        const errorMessage = '获取看板列表失败'
        api.getBoards.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('boards/fetchBoards')).rejects.toBeDefined()

        expect(store.state.boards.error).toBe(errorMessage)
        expect(store.state.boards.loading).toBe(false)
      })

      it('should use default error message when response has no error message', async () => {
        api.getBoards.mockRejectedValue(new Error('Network error'))

        await expect(store.dispatch('boards/fetchBoards')).rejects.toBeDefined()

        expect(store.state.boards.error).toBe('获取看板列表失败')
      })
    })

    describe('fetchBoard', () => {
      it('should fetch a single board successfully', async () => {
        const mockBoard = { id: 1, name: 'Board 1' }
        api.getBoard.mockResolvedValue({ data: mockBoard })

        await store.dispatch('boards/fetchBoard', 1)

        expect(api.getBoard).toHaveBeenCalledWith(1)
        expect(store.state.boards.currentBoard).toEqual(mockBoard)
        expect(store.state.boards.loading).toBe(false)
        expect(store.state.boards.error).toBeNull()
      })

      it('should handle fetch board error', async () => {
        const errorMessage = '获取看板详情失败'
        api.getBoard.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('boards/fetchBoard', 1)).rejects.toBeDefined()

        expect(store.state.boards.error).toBe(errorMessage)
        expect(store.state.boards.loading).toBe(false)
      })
    })

    describe('createBoard', () => {
      it('should create a board successfully', async () => {
        const newBoard = { id: 1, name: 'New Board' }
        api.createBoard.mockResolvedValue({ data: newBoard })

        const result = await store.dispatch('boards/createBoard', { name: 'New Board' })

        expect(api.createBoard).toHaveBeenCalledWith({ name: 'New Board' })
        expect(store.state.boards.boards).toContainEqual(newBoard)
        expect(result).toEqual(newBoard)
        expect(store.state.boards.loading).toBe(false)
        expect(store.state.boards.error).toBeNull()
      })

      it('should handle create board error', async () => {
        const errorMessage = '创建看板失败'
        api.createBoard.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('boards/createBoard', { name: 'New Board' })).rejects.toBeDefined()

        expect(store.state.boards.error).toBe(errorMessage)
        expect(store.state.boards.loading).toBe(false)
      })
    })

    describe('updateBoard', () => {
      it('should update a board successfully', async () => {
        const initialBoard = { id: 1, name: 'Board 1' }
        store.commit('boards/addBoard', initialBoard)

        const updatedBoard = { id: 1, name: 'Updated Board 1' }
        api.updateBoard.mockResolvedValue({ data: updatedBoard })

        const result = await store.dispatch('boards/updateBoard', {
          id: 1,
          data: { name: 'Updated Board 1' }
        })

        expect(api.updateBoard).toHaveBeenCalledWith(1, { name: 'Updated Board 1' })
        expect(store.state.boards.boards[0]).toEqual(updatedBoard)
        expect(result).toEqual(updatedBoard)
        expect(store.state.boards.loading).toBe(false)
        expect(store.state.boards.error).toBeNull()
      })

      it('should handle update board error', async () => {
        const errorMessage = '更新看板失败'
        api.updateBoard.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('boards/updateBoard', {
          id: 1,
          data: { name: 'Updated Board' }
        })).rejects.toBeDefined()

        expect(store.state.boards.error).toBe(errorMessage)
        expect(store.state.boards.loading).toBe(false)
      })
    })

    describe('deleteBoard', () => {
      it('should delete a board successfully', async () => {
        // Clear any existing boards and add a fresh one
        store.commit('boards/setBoards', [])
        const board = { id: 1, name: 'Board 1' }
        store.commit('boards/addBoard', board)

        api.deleteBoard.mockResolvedValue({})

        await store.dispatch('boards/deleteBoard', 1)

        expect(api.deleteBoard).toHaveBeenCalledWith(1)
        expect(store.state.boards.boards.length).toBe(0)
        expect(store.state.boards.loading).toBe(false)
        expect(store.state.boards.error).toBeNull()
      })

      it('should handle delete board error', async () => {
        const errorMessage = '删除看板失败'
        api.deleteBoard.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('boards/deleteBoard', 1)).rejects.toBeDefined()

        expect(store.state.boards.error).toBe(errorMessage)
        expect(store.state.boards.loading).toBe(false)
      })
    })
  })

  describe('getters', () => {
    it('allBoards should return all boards', () => {
      const testBoards = [
        { id: 1, name: 'Board 1' },
        { id: 2, name: 'Board 2' }
      ]
      store.commit('boards/setBoards', testBoards)
      
      expect(store.getters['boards/allBoards']).toEqual(testBoards)
    })

    it('currentBoard should return the current board', () => {
      const board = { id: 1, name: 'Board 1' }
      store.commit('boards/setCurrentBoard', board)
      
      expect(store.getters['boards/currentBoard']).toEqual(board)
    })

    it('isLoading should return the loading state', () => {
      store.commit('boards/setLoading', true)
      expect(store.getters['boards/isLoading']).toBe(true)
      
      store.commit('boards/setLoading', false)
      expect(store.getters['boards/isLoading']).toBe(false)
    })

    it('error should return the error state', () => {
      const errorMessage = 'Test error'
      store.commit('boards/setError', errorMessage)
      
      expect(store.getters['boards/error']).toBe(errorMessage)
    })
  })
})
