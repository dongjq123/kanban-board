// Lists store tests - Basic smoke test for task 9.2
import { createStore } from 'vuex'
import lists from '@/store/modules/lists'
import api from '@/services/api'

// Mock the API module
jest.mock('@/services/api')

describe('lists store module', () => {
  let store

  beforeEach(() => {
    // Create a fresh store instance for each test
    store = createStore({
      modules: {
        lists: {
          ...lists,
          namespaced: true
        }
      }
    })
    // Clear all mocks
    jest.clearAllMocks()
  })

  describe('mutations', () => {
    it('setLists should set the lists array', () => {
      const testLists = [
        { id: 1, name: 'List 1', board_id: 1, position: 0 },
        { id: 2, name: 'List 2', board_id: 1, position: 1 }
      ]
      store.commit('lists/setLists', testLists)
      expect(store.state.lists.lists).toEqual(testLists)
    })

    it('addList should add a list to the array', () => {
      store.commit('lists/setLists', [])
      
      const newList = { id: 1, name: 'New List', board_id: 1, position: 0 }
      store.commit('lists/addList', newList)
      expect(store.state.lists.lists).toContainEqual(newList)
      expect(store.state.lists.lists.length).toBe(1)
    })

    it('updateList should update an existing list', () => {
      const initialLists = [
        { id: 1, name: 'List 1', board_id: 1, position: 0 },
        { id: 2, name: 'List 2', board_id: 1, position: 1 }
      ]
      store.commit('lists/setLists', initialLists)
      
      const updatedList = { id: 1, name: 'Updated List 1', board_id: 1, position: 0 }
      store.commit('lists/updateList', updatedList)
      
      expect(store.state.lists.lists[0]).toEqual(updatedList)
      expect(store.state.lists.lists[1]).toEqual(initialLists[1])
    })

    it('deleteList should remove a list from the array', () => {
      const initialLists = [
        { id: 1, name: 'List 1', board_id: 1, position: 0 },
        { id: 2, name: 'List 2', board_id: 1, position: 1 }
      ]
      store.commit('lists/setLists', initialLists)
      
      store.commit('lists/deleteList', 1)
      
      expect(store.state.lists.lists.length).toBe(1)
      expect(store.state.lists.lists[0].id).toBe(2)
    })

    it('updateListPosition should update the position of a list', () => {
      const initialLists = [
        { id: 1, name: 'List 1', board_id: 1, position: 0 }
      ]
      store.commit('lists/setLists', initialLists)
      
      store.commit('lists/updateListPosition', { listId: 1, position: 2 })
      
      expect(store.state.lists.lists[0].position).toBe(2)
    })

    it('setLoading should set the loading state', () => {
      store.commit('lists/setLoading', true)
      expect(store.state.lists.loading).toBe(true)
      
      store.commit('lists/setLoading', false)
      expect(store.state.lists.loading).toBe(false)
    })

    it('setError should set the error state', () => {
      const errorMessage = 'Test error'
      store.commit('lists/setError', errorMessage)
      expect(store.state.lists.error).toBe(errorMessage)
    })
  })

  describe('actions', () => {
    describe('fetchLists', () => {
      it('should fetch lists successfully', async () => {
        const mockLists = [
          { id: 1, name: 'List 1', board_id: 1, position: 0 },
          { id: 2, name: 'List 2', board_id: 1, position: 1 }
        ]
        api.getLists.mockResolvedValue({ data: mockLists })

        await store.dispatch('lists/fetchLists', 1)

        expect(api.getLists).toHaveBeenCalledWith(1)
        expect(store.state.lists.lists).toEqual(mockLists)
        expect(store.state.lists.loading).toBe(false)
        expect(store.state.lists.error).toBeNull()
      })

      it('should handle fetch lists error', async () => {
        const errorMessage = '获取列表失败'
        api.getLists.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('lists/fetchLists', 1)).rejects.toBeDefined()

        expect(store.state.lists.error).toBe(errorMessage)
        expect(store.state.lists.loading).toBe(false)
      })
    })

    describe('createList', () => {
      it('should create a list successfully', async () => {
        const newList = { id: 1, name: 'New List', board_id: 1, position: 0 }
        api.createList.mockResolvedValue({ data: newList })

        const result = await store.dispatch('lists/createList', {
          boardId: 1,
          data: { name: 'New List', position: 0 }
        })

        expect(api.createList).toHaveBeenCalledWith(1, { name: 'New List', position: 0 })
        expect(store.state.lists.lists).toContainEqual(newList)
        expect(result).toEqual(newList)
        expect(store.state.lists.loading).toBe(false)
        expect(store.state.lists.error).toBeNull()
      })

      it('should handle create list error', async () => {
        const errorMessage = '创建列表失败'
        api.createList.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('lists/createList', {
          boardId: 1,
          data: { name: 'New List' }
        })).rejects.toBeDefined()

        expect(store.state.lists.error).toBe(errorMessage)
        expect(store.state.lists.loading).toBe(false)
      })
    })

    describe('updateList', () => {
      it('should update a list successfully', async () => {
        const initialList = { id: 1, name: 'List 1', board_id: 1, position: 0 }
        store.commit('lists/addList', initialList)

        const updatedList = { id: 1, name: 'Updated List 1', board_id: 1, position: 0 }
        api.updateList.mockResolvedValue({ data: updatedList })

        const result = await store.dispatch('lists/updateList', {
          id: 1,
          data: { name: 'Updated List 1' }
        })

        expect(api.updateList).toHaveBeenCalledWith(1, { name: 'Updated List 1' })
        expect(store.state.lists.lists[0]).toEqual(updatedList)
        expect(result).toEqual(updatedList)
        expect(store.state.lists.loading).toBe(false)
        expect(store.state.lists.error).toBeNull()
      })

      it('should handle update list error', async () => {
        const errorMessage = '更新列表失败'
        api.updateList.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('lists/updateList', {
          id: 1,
          data: { name: 'Updated List' }
        })).rejects.toBeDefined()

        expect(store.state.lists.error).toBe(errorMessage)
        expect(store.state.lists.loading).toBe(false)
      })
    })

    describe('deleteList', () => {
      it('should delete a list successfully', async () => {
        store.commit('lists/setLists', [])
        const list = { id: 1, name: 'List 1', board_id: 1, position: 0 }
        store.commit('lists/addList', list)

        api.deleteList.mockResolvedValue({})

        await store.dispatch('lists/deleteList', 1)

        expect(api.deleteList).toHaveBeenCalledWith(1)
        expect(store.state.lists.lists.length).toBe(0)
        expect(store.state.lists.loading).toBe(false)
        expect(store.state.lists.error).toBeNull()
      })

      it('should handle delete list error', async () => {
        const errorMessage = '删除列表失败'
        api.deleteList.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('lists/deleteList', 1)).rejects.toBeDefined()

        expect(store.state.lists.error).toBe(errorMessage)
        expect(store.state.lists.loading).toBe(false)
      })
    })

    describe('updateListPosition', () => {
      it('should update list position successfully', async () => {
        const list = { id: 1, name: 'List 1', board_id: 1, position: 0 }
        store.commit('lists/addList', list)

        const updatedList = { id: 1, name: 'List 1', board_id: 1, position: 2 }
        api.updateListPosition.mockResolvedValue({ data: updatedList })

        const result = await store.dispatch('lists/updateListPosition', {
          id: 1,
          position: 2
        })

        expect(api.updateListPosition).toHaveBeenCalledWith(1, { position: 2 })
        expect(store.state.lists.lists[0].position).toBe(2)
        expect(result).toEqual(updatedList)
        expect(store.state.lists.loading).toBe(false)
        expect(store.state.lists.error).toBeNull()
      })

      it('should handle update list position error', async () => {
        const errorMessage = '更新列表位置失败'
        api.updateListPosition.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('lists/updateListPosition', {
          id: 1,
          position: 2
        })).rejects.toBeDefined()

        expect(store.state.lists.error).toBe(errorMessage)
        expect(store.state.lists.loading).toBe(false)
      })
    })
  })

  describe('getters', () => {
    it('allLists should return all lists', () => {
      const testLists = [
        { id: 1, name: 'List 1', board_id: 1, position: 0 },
        { id: 2, name: 'List 2', board_id: 1, position: 1 }
      ]
      store.commit('lists/setLists', testLists)
      
      expect(store.getters['lists/allLists']).toEqual(testLists)
    })

    it('isLoading should return the loading state', () => {
      store.commit('lists/setLoading', true)
      expect(store.getters['lists/isLoading']).toBe(true)
      
      store.commit('lists/setLoading', false)
      expect(store.getters['lists/isLoading']).toBe(false)
    })

    it('error should return the error state', () => {
      const errorMessage = 'Test error'
      store.commit('lists/setError', errorMessage)
      
      expect(store.getters['lists/error']).toBe(errorMessage)
    })

    it('getListById should return a list by id', () => {
      const testLists = [
        { id: 1, name: 'List 1', board_id: 1, position: 0 },
        { id: 2, name: 'List 2', board_id: 1, position: 1 }
      ]
      store.commit('lists/setLists', testLists)
      
      expect(store.getters['lists/getListById'](1)).toEqual(testLists[0])
      expect(store.getters['lists/getListById'](2)).toEqual(testLists[1])
      expect(store.getters['lists/getListById'](999)).toBeUndefined()
    })
  })
})
