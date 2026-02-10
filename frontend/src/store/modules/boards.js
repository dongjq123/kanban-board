// Boards store module
// 需求：9.1, 9.3, 10.1
import api, { toast } from '@/services/api'

const state = {
  boards: [],
  currentBoard: null,
  loading: false,
  error: null
}

const mutations = {
  setBoards(state, boards) {
    state.boards = boards
  },
  
  addBoard(state, board) {
    state.boards.push(board)
  },
  
  updateBoard(state, updatedBoard) {
    const index = state.boards.findIndex(b => b.id === updatedBoard.id)
    if (index !== -1) {
      state.boards.splice(index, 1, updatedBoard)
    }
    // Also update currentBoard if it's the one being updated
    if (state.currentBoard && state.currentBoard.id === updatedBoard.id) {
      state.currentBoard = updatedBoard
    }
  },
  
  deleteBoard(state, boardId) {
    state.boards = state.boards.filter(b => b.id !== boardId)
    // Clear currentBoard if it's the one being deleted
    if (state.currentBoard && state.currentBoard.id === boardId) {
      state.currentBoard = null
    }
  },
  
  setCurrentBoard(state, board) {
    state.currentBoard = board
  },
  
  setLoading(state, loading) {
    state.loading = loading
  },
  
  setError(state, error) {
    state.error = error
  }
}

const actions = {
  async fetchBoards({ commit }) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.getBoards()
      // Backend returns { boards: [...] }
      const boards = response.data.boards || response.data
      commit('setBoards', boards)
      return boards
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '获取看板列表失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async fetchBoard({ commit }, boardId) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.getBoard(boardId)
      commit('setCurrentBoard', response.data)
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '获取看板详情失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async createBoard({ commit }, boardData) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.createBoard(boardData)
      commit('addBoard', response.data)
      
      // 显示成功 Toast 通知
      // 需求：9.1, 9.3
      try {
        toast.success('看板创建成功')
      } catch (error) {
        console.warn('Toast notification failed:', error)
      }
      
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '创建看板失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async updateBoard({ commit }, { id, data }) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.updateBoard(id, data)
      commit('updateBoard', response.data)
      
      // 显示成功 Toast 通知
      // 需求：9.1, 9.3
      try {
        toast.success('看板更新成功')
      } catch (error) {
        console.warn('Toast notification failed:', error)
      }
      
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '更新看板失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async deleteBoard({ commit }, boardId) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      await api.deleteBoard(boardId)
      commit('deleteBoard', boardId)
      
      // 显示成功 Toast 通知
      // 需求：9.1, 9.3
      try {
        toast.success('看板删除成功')
      } catch (error) {
        console.warn('Toast notification failed:', error)
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '删除看板失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  }
}

const getters = {
  allBoards: state => state.boards,
  currentBoard: state => state.currentBoard,
  isLoading: state => state.loading,
  error: state => state.error
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
