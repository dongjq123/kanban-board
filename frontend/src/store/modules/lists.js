// Lists store module
// 需求：9.1, 9.3, 10.1
import api, { toast } from '@/services/api'

const state = {
  lists: [],
  loading: false,
  error: null
}

const mutations = {
  setLists(state, lists) {
    // 确保 lists 始终是数组
    state.lists = Array.isArray(lists) ? lists : []
  },
  
  addList(state, list) {
    state.lists.push(list)
  },
  
  updateList(state, updatedList) {
    const index = state.lists.findIndex(l => l.id === updatedList.id)
    if (index !== -1) {
      state.lists.splice(index, 1, updatedList)
    }
  },
  
  deleteList(state, listId) {
    state.lists = state.lists.filter(l => l.id !== listId)
  },
  
  updateListPosition(state, { listId, position }) {
    const list = state.lists.find(l => l.id === listId)
    if (list) {
      list.position = position
    }
  },
  
  setLoading(state, loading) {
    state.loading = loading
  },
  
  setError(state, error) {
    state.error = error
  }
}

const actions = {
  async fetchLists({ commit }, boardId) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.getLists(boardId)
      // 处理不同的响应格式
      // 后端可能返回 { lists: [...] } 或直接返回数组
      const lists = response.data.lists || response.data
      // 确保 lists 是数组
      const listsArray = Array.isArray(lists) ? lists : []
      commit('setLists', listsArray)
      return listsArray
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '获取列表失败'
      commit('setError', errorMessage)
      // 设置空数组以防止错误
      commit('setLists', [])
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async createList({ commit }, { boardId, data }) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.createList(boardId, data)
      commit('addList', response.data)
      
      // 显示成功 Toast 通知
      // 需求：9.1, 9.3
      try {
        toast.success('列表创建成功')
      } catch (error) {
        console.warn('Toast notification failed:', error)
      }
      
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '创建列表失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async updateList({ commit }, { id, data }) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.updateList(id, data)
      commit('updateList', response.data)
      
      // 显示成功 Toast 通知
      // 需求：9.1, 9.3
      try {
        toast.success('列表更新成功')
      } catch (error) {
        console.warn('Toast notification failed:', error)
      }
      
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '更新列表失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async deleteList({ commit }, listId) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      await api.deleteList(listId)
      commit('deleteList', listId)
      
      // 显示成功 Toast 通知
      // 需求：9.1, 9.3
      try {
        toast.success('列表删除成功')
      } catch (error) {
        console.warn('Toast notification failed:', error)
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '删除列表失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async updateListPosition({ commit }, { id, position }) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.updateListPosition(id, { position })
      commit('updateListPosition', { listId: id, position })
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '更新列表位置失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  }
}

const getters = {
  allLists: state => state.lists,
  isLoading: state => state.loading,
  error: state => state.error,
  getListById: state => id => state.lists.find(l => l.id === id)
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
