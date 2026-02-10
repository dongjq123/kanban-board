// Cards store module
// 需求：9.1, 9.3, 10.1
import api, { toast } from '@/services/api'

const state = {
  cards: {},
  currentCard: null,
  loading: false,
  error: null
}

const mutations = {
  setCards(state, { listId, cards }) {
    // 确保 cards 是数组
    const cardsArray = Array.isArray(cards) ? cards : []
    state.cards = {
      ...state.cards,
      [listId]: cardsArray
    }
  },
  
  addCard(state, card) {
    const listId = card.list_id
    if (!state.cards[listId]) {
      state.cards[listId] = []
    }
    state.cards[listId].push(card)
  },
  
  updateCard(state, updatedCard) {
    const listId = updatedCard.list_id
    if (state.cards[listId]) {
      const index = state.cards[listId].findIndex(c => c.id === updatedCard.id)
      if (index !== -1) {
        state.cards[listId].splice(index, 1, updatedCard)
      }
    }
    // Also update currentCard if it's the one being updated
    if (state.currentCard && state.currentCard.id === updatedCard.id) {
      state.currentCard = updatedCard
    }
  },
  
  deleteCard(state, { cardId, listId }) {
    if (state.cards[listId]) {
      state.cards[listId] = state.cards[listId].filter(c => c.id !== cardId)
    }
    // Clear currentCard if it's the one being deleted
    if (state.currentCard && state.currentCard.id === cardId) {
      state.currentCard = null
    }
  },
  
  moveCard(state, { cardId, oldListId, newListId, updatedCard }) {
    // Remove card from old list
    if (state.cards[oldListId]) {
      state.cards[oldListId] = state.cards[oldListId].filter(c => c.id !== cardId)
    }
    
    // Add card to new list
    if (!state.cards[newListId]) {
      state.cards[newListId] = []
    }
    
    // Check if card already exists in new list (in case of same list move)
    const existingIndex = state.cards[newListId].findIndex(c => c.id === cardId)
    if (existingIndex !== -1) {
      state.cards[newListId].splice(existingIndex, 1, updatedCard)
    } else {
      state.cards[newListId].push(updatedCard)
    }
    
    // Update currentCard if it's the one being moved
    if (state.currentCard && state.currentCard.id === cardId) {
      state.currentCard = updatedCard
    }
  },
  
  setCurrentCard(state, card) {
    state.currentCard = card
  },
  
  setLoading(state, loading) {
    state.loading = loading
  },
  
  setError(state, error) {
    state.error = error
  }
}

const actions = {
  async fetchCards({ commit }, listId) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.getCards(listId)
      // 处理不同的响应格式
      // 后端可能返回 { cards: [...] } 或直接返回数组
      const cards = response.data.cards || response.data
      // 确保 cards 是数组
      const cardsArray = Array.isArray(cards) ? cards : []
      commit('setCards', { listId, cards: cardsArray })
      return cardsArray
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '获取卡片列表失败'
      commit('setError', errorMessage)
      // 设置空数组以防止错误
      commit('setCards', { listId, cards: [] })
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async fetchCard({ commit }, cardId) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.getCard(cardId)
      commit('setCurrentCard', response.data)
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '获取卡片详情失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async createCard({ commit }, { listId, data }) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.createCard(listId, data)
      commit('addCard', response.data)
      
      // 显示成功 Toast 通知
      // 需求：9.1, 9.3
      try {
        toast.success('卡片创建成功')
      } catch (error) {
        console.warn('Toast notification failed:', error)
      }
      
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '创建卡片失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async updateCard({ commit }, { id, data }) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.updateCard(id, data)
      commit('updateCard', response.data)
      
      // 显示成功 Toast 通知
      // 需求：9.1, 9.3
      try {
        toast.success('卡片更新成功')
      } catch (error) {
        console.warn('Toast notification failed:', error)
      }
      
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '更新卡片失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async deleteCard({ commit }, { cardId, listId }) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      await api.deleteCard(cardId)
      commit('deleteCard', { cardId, listId })
      
      // 显示成功 Toast 通知
      // 需求：9.1, 9.3
      try {
        toast.success('卡片删除成功')
      } catch (error) {
        console.warn('Toast notification failed:', error)
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '删除卡片失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  },
  
  async moveCard({ commit }, { cardId, oldListId, newListId, position }) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      const response = await api.moveCard(cardId, {
        list_id: newListId,
        position
      })
      commit('moveCard', {
        cardId,
        oldListId,
        newListId,
        updatedCard: response.data
      })
      
      // 显示成功 Toast 通知
      // 需求：9.1, 9.3
      try {
        toast.success('卡片移动成功')
      } catch (error) {
        console.warn('Toast notification failed:', error)
      }
      
      return response.data
    } catch (error) {
      const errorMessage = error.response?.data?.error?.message || '移动卡片失败'
      commit('setError', errorMessage)
      throw error
    } finally {
      commit('setLoading', false)
    }
  }
}

const getters = {
  getCardsByListId: state => listId => {
    const cards = state.cards[listId]
    // 确保返回数组
    return Array.isArray(cards) ? cards : []
  },
  currentCard: state => state.currentCard,
  isLoading: state => state.loading,
  error: state => state.error,
  getCardById: state => (listId, cardId) => {
    const cards = state.cards[listId] || []
    return cards.find(c => c.id === cardId)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}
