// Cards store tests
import { createStore } from 'vuex'
import cards from '@/store/modules/cards'
import api from '@/services/api'

// Mock the API module
jest.mock('@/services/api')

describe('cards store module', () => {
  let store

  beforeEach(() => {
    // Create a fresh store instance for each test
    store = createStore({
      modules: {
        cards: {
          ...cards,
          namespaced: true
        }
      }
    })
    // Clear all mocks
    jest.clearAllMocks()
  })

  describe('mutations', () => {
    it('setCards should set cards for a specific list', () => {
      const listId = 1
      const testCards = [
        { id: 1, list_id: 1, title: 'Card 1' },
        { id: 2, list_id: 1, title: 'Card 2' }
      ]
      store.commit('cards/setCards', { listId, cards: testCards })
      expect(store.state.cards.cards[listId]).toEqual(testCards)
    })

    it('setCards should preserve cards from other lists', () => {
      const list1Cards = [{ id: 1, list_id: 1, title: 'Card 1' }]
      const list2Cards = [{ id: 2, list_id: 2, title: 'Card 2' }]
      
      store.commit('cards/setCards', { listId: 1, cards: list1Cards })
      store.commit('cards/setCards', { listId: 2, cards: list2Cards })
      
      expect(store.state.cards.cards[1]).toEqual(list1Cards)
      expect(store.state.cards.cards[2]).toEqual(list2Cards)
    })

    it('addCard should add a card to the appropriate list', () => {
      // Initialize with empty cards for list 1
      store.commit('cards/setCards', { listId: 1, cards: [] })
      
      const newCard = { id: 1, list_id: 1, title: 'New Card' }
      store.commit('cards/addCard', newCard)
      
      expect(store.state.cards.cards[1]).toContainEqual(newCard)
      expect(store.state.cards.cards[1].length).toBe(1)
    })

    it('addCard should create list array if it does not exist', () => {
      const newCard = { id: 1, list_id: 5, title: 'New Card' }
      store.commit('cards/addCard', newCard)
      
      expect(store.state.cards.cards[5]).toBeDefined()
      expect(store.state.cards.cards[5]).toContainEqual(newCard)
    })

    it('updateCard should update an existing card', () => {
      const listId = 1
      const initialCards = [
        { id: 1, list_id: 1, title: 'Card 1' },
        { id: 2, list_id: 1, title: 'Card 2' }
      ]
      store.commit('cards/setCards', { listId, cards: initialCards })
      
      const updatedCard = { id: 1, list_id: 1, title: 'Updated Card 1', description: 'New description' }
      store.commit('cards/updateCard', updatedCard)
      
      expect(store.state.cards.cards[1][0]).toEqual(updatedCard)
      expect(store.state.cards.cards[1][1]).toEqual(initialCards[1])
    })

    it('updateCard should update currentCard if it matches', () => {
      const card = { id: 1, list_id: 1, title: 'Card 1' }
      store.commit('cards/setCurrentCard', card)
      
      const updatedCard = { id: 1, list_id: 1, title: 'Updated Card 1' }
      store.commit('cards/updateCard', updatedCard)
      
      expect(store.state.cards.currentCard).toEqual(updatedCard)
    })

    it('deleteCard should remove a card from the list', () => {
      const listId = 1
      const initialCards = [
        { id: 1, list_id: 1, title: 'Card 1' },
        { id: 2, list_id: 1, title: 'Card 2' }
      ]
      store.commit('cards/setCards', { listId, cards: initialCards })
      
      store.commit('cards/deleteCard', { cardId: 1, listId: 1 })
      
      expect(store.state.cards.cards[1].length).toBe(1)
      expect(store.state.cards.cards[1][0].id).toBe(2)
    })

    it('deleteCard should clear currentCard if it matches', () => {
      const card = { id: 1, list_id: 1, title: 'Card 1' }
      store.commit('cards/setCurrentCard', card)
      
      store.commit('cards/deleteCard', { cardId: 1, listId: 1 })
      
      expect(store.state.cards.currentCard).toBeNull()
    })

    it('moveCard should move card from one list to another', () => {
      const list1Cards = [
        { id: 1, list_id: 1, title: 'Card 1' },
        { id: 2, list_id: 1, title: 'Card 2' }
      ]
      const list2Cards = [
        { id: 3, list_id: 2, title: 'Card 3' }
      ]
      
      store.commit('cards/setCards', { listId: 1, cards: list1Cards })
      store.commit('cards/setCards', { listId: 2, cards: list2Cards })
      
      const movedCard = { id: 1, list_id: 2, title: 'Card 1', position: 1 }
      store.commit('cards/moveCard', {
        cardId: 1,
        oldListId: 1,
        newListId: 2,
        updatedCard: movedCard
      })
      
      // Card should be removed from old list
      expect(store.state.cards.cards[1].length).toBe(1)
      expect(store.state.cards.cards[1].find(c => c.id === 1)).toBeUndefined()
      
      // Card should be added to new list
      expect(store.state.cards.cards[2].length).toBe(2)
      expect(store.state.cards.cards[2].find(c => c.id === 1)).toEqual(movedCard)
    })

    it('moveCard should handle moving within the same list', () => {
      const listCards = [
        { id: 1, list_id: 1, title: 'Card 1', position: 0 },
        { id: 2, list_id: 1, title: 'Card 2', position: 1 }
      ]
      
      store.commit('cards/setCards', { listId: 1, cards: listCards })
      
      const movedCard = { id: 1, list_id: 1, title: 'Card 1', position: 1 }
      store.commit('cards/moveCard', {
        cardId: 1,
        oldListId: 1,
        newListId: 1,
        updatedCard: movedCard
      })
      
      // Card should still be in the list with updated position
      expect(store.state.cards.cards[1].length).toBe(2)
      const card = store.state.cards.cards[1].find(c => c.id === 1)
      expect(card).toEqual(movedCard)
    })

    it('moveCard should create new list array if it does not exist', () => {
      const list1Cards = [{ id: 1, list_id: 1, title: 'Card 1' }]
      store.commit('cards/setCards', { listId: 1, cards: list1Cards })
      
      const movedCard = { id: 1, list_id: 5, title: 'Card 1' }
      store.commit('cards/moveCard', {
        cardId: 1,
        oldListId: 1,
        newListId: 5,
        updatedCard: movedCard
      })
      
      expect(store.state.cards.cards[5]).toBeDefined()
      expect(store.state.cards.cards[5]).toContainEqual(movedCard)
    })

    it('moveCard should update currentCard if it matches', () => {
      const card = { id: 1, list_id: 1, title: 'Card 1' }
      store.commit('cards/setCurrentCard', card)
      
      const movedCard = { id: 1, list_id: 2, title: 'Card 1' }
      store.commit('cards/moveCard', {
        cardId: 1,
        oldListId: 1,
        newListId: 2,
        updatedCard: movedCard
      })
      
      expect(store.state.cards.currentCard).toEqual(movedCard)
    })

    it('setCurrentCard should set the current card', () => {
      const card = { id: 1, list_id: 1, title: 'Card 1' }
      store.commit('cards/setCurrentCard', card)
      expect(store.state.cards.currentCard).toEqual(card)
    })

    it('setLoading should set the loading state', () => {
      store.commit('cards/setLoading', true)
      expect(store.state.cards.loading).toBe(true)
      
      store.commit('cards/setLoading', false)
      expect(store.state.cards.loading).toBe(false)
    })

    it('setError should set the error state', () => {
      const errorMessage = 'Test error'
      store.commit('cards/setError', errorMessage)
      expect(store.state.cards.error).toBe(errorMessage)
    })
  })

  describe('actions', () => {
    describe('fetchCards', () => {
      it('should fetch cards successfully', async () => {
        const listId = 1
        const mockCards = [
          { id: 1, list_id: 1, title: 'Card 1' },
          { id: 2, list_id: 1, title: 'Card 2' }
        ]
        api.getCards.mockResolvedValue({ data: mockCards })

        await store.dispatch('cards/fetchCards', listId)

        expect(api.getCards).toHaveBeenCalledWith(listId)
        expect(store.state.cards.cards[listId]).toEqual(mockCards)
        expect(store.state.cards.loading).toBe(false)
        expect(store.state.cards.error).toBeNull()
      })

      it('should handle fetch cards error', async () => {
        const errorMessage = '获取卡片列表失败'
        api.getCards.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('cards/fetchCards', 1)).rejects.toBeDefined()

        expect(store.state.cards.error).toBe(errorMessage)
        expect(store.state.cards.loading).toBe(false)
      })

      it('should use default error message when response has no error message', async () => {
        api.getCards.mockRejectedValue(new Error('Network error'))

        await expect(store.dispatch('cards/fetchCards', 1)).rejects.toBeDefined()

        expect(store.state.cards.error).toBe('获取卡片列表失败')
      })
    })

    describe('fetchCard', () => {
      it('should fetch a single card successfully', async () => {
        const mockCard = { id: 1, list_id: 1, title: 'Card 1' }
        api.getCard.mockResolvedValue({ data: mockCard })

        await store.dispatch('cards/fetchCard', 1)

        expect(api.getCard).toHaveBeenCalledWith(1)
        expect(store.state.cards.currentCard).toEqual(mockCard)
        expect(store.state.cards.loading).toBe(false)
        expect(store.state.cards.error).toBeNull()
      })

      it('should handle fetch card error', async () => {
        const errorMessage = '获取卡片详情失败'
        api.getCard.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('cards/fetchCard', 1)).rejects.toBeDefined()

        expect(store.state.cards.error).toBe(errorMessage)
        expect(store.state.cards.loading).toBe(false)
      })
    })

    describe('createCard', () => {
      it('should create a card successfully', async () => {
        const listId = 1
        const newCard = { id: 1, list_id: 1, title: 'New Card' }
        api.createCard.mockResolvedValue({ data: newCard })

        const result = await store.dispatch('cards/createCard', {
          listId,
          data: { title: 'New Card' }
        })

        expect(api.createCard).toHaveBeenCalledWith(listId, { title: 'New Card' })
        expect(store.state.cards.cards[listId]).toContainEqual(newCard)
        expect(result).toEqual(newCard)
        expect(store.state.cards.loading).toBe(false)
        expect(store.state.cards.error).toBeNull()
      })

      it('should handle create card error', async () => {
        const errorMessage = '创建卡片失败'
        api.createCard.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('cards/createCard', {
          listId: 1,
          data: { title: 'New Card' }
        })).rejects.toBeDefined()

        expect(store.state.cards.error).toBe(errorMessage)
        expect(store.state.cards.loading).toBe(false)
      })
    })

    describe('updateCard', () => {
      it('should update a card successfully', async () => {
        const listId = 1
        const initialCard = { id: 1, list_id: 1, title: 'Card 1' }
        store.commit('cards/setCards', { listId, cards: [initialCard] })

        const updatedCard = { id: 1, list_id: 1, title: 'Updated Card 1', description: 'New description' }
        api.updateCard.mockResolvedValue({ data: updatedCard })

        const result = await store.dispatch('cards/updateCard', {
          id: 1,
          data: { title: 'Updated Card 1', description: 'New description' }
        })

        expect(api.updateCard).toHaveBeenCalledWith(1, {
          title: 'Updated Card 1',
          description: 'New description'
        })
        expect(store.state.cards.cards[listId][0]).toEqual(updatedCard)
        expect(result).toEqual(updatedCard)
        expect(store.state.cards.loading).toBe(false)
        expect(store.state.cards.error).toBeNull()
      })

      it('should handle update card error', async () => {
        const errorMessage = '更新卡片失败'
        api.updateCard.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('cards/updateCard', {
          id: 1,
          data: { title: 'Updated Card' }
        })).rejects.toBeDefined()

        expect(store.state.cards.error).toBe(errorMessage)
        expect(store.state.cards.loading).toBe(false)
      })
    })

    describe('deleteCard', () => {
      it('should delete a card successfully', async () => {
        const listId = 1
        const cards = [
          { id: 1, list_id: 1, title: 'Card 1' },
          { id: 2, list_id: 1, title: 'Card 2' }
        ]
        store.commit('cards/setCards', { listId, cards })

        api.deleteCard.mockResolvedValue({})

        await store.dispatch('cards/deleteCard', { cardId: 1, listId })

        expect(api.deleteCard).toHaveBeenCalledWith(1)
        expect(store.state.cards.cards[listId].length).toBe(1)
        expect(store.state.cards.cards[listId][0].id).toBe(2)
        expect(store.state.cards.loading).toBe(false)
        expect(store.state.cards.error).toBeNull()
      })

      it('should handle delete card error', async () => {
        const errorMessage = '删除卡片失败'
        api.deleteCard.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('cards/deleteCard', {
          cardId: 1,
          listId: 1
        })).rejects.toBeDefined()

        expect(store.state.cards.error).toBe(errorMessage)
        expect(store.state.cards.loading).toBe(false)
      })
    })

    describe('moveCard', () => {
      it('should move a card to a different list successfully', async () => {
        const list1Cards = [{ id: 1, list_id: 1, title: 'Card 1' }]
        const list2Cards = [{ id: 2, list_id: 2, title: 'Card 2' }]
        
        store.commit('cards/setCards', { listId: 1, cards: list1Cards })
        store.commit('cards/setCards', { listId: 2, cards: list2Cards })

        const movedCard = { id: 1, list_id: 2, title: 'Card 1', position: 1 }
        api.moveCard.mockResolvedValue({ data: movedCard })

        const result = await store.dispatch('cards/moveCard', {
          cardId: 1,
          oldListId: 1,
          newListId: 2,
          position: 1
        })

        expect(api.moveCard).toHaveBeenCalledWith(1, {
          list_id: 2,
          position: 1
        })
        expect(store.state.cards.cards[1].length).toBe(0)
        expect(store.state.cards.cards[2].length).toBe(2)
        expect(store.state.cards.cards[2].find(c => c.id === 1)).toEqual(movedCard)
        expect(result).toEqual(movedCard)
        expect(store.state.cards.loading).toBe(false)
        expect(store.state.cards.error).toBeNull()
      })

      it('should move a card within the same list successfully', async () => {
        const listCards = [
          { id: 1, list_id: 1, title: 'Card 1', position: 0 },
          { id: 2, list_id: 1, title: 'Card 2', position: 1 }
        ]
        
        store.commit('cards/setCards', { listId: 1, cards: listCards })

        const movedCard = { id: 1, list_id: 1, title: 'Card 1', position: 1 }
        api.moveCard.mockResolvedValue({ data: movedCard })

        await store.dispatch('cards/moveCard', {
          cardId: 1,
          oldListId: 1,
          newListId: 1,
          position: 1
        })

        expect(api.moveCard).toHaveBeenCalledWith(1, {
          list_id: 1,
          position: 1
        })
        expect(store.state.cards.cards[1].length).toBe(2)
        const card = store.state.cards.cards[1].find(c => c.id === 1)
        expect(card.position).toBe(1)
      })

      it('should handle move card error', async () => {
        const errorMessage = '移动卡片失败'
        api.moveCard.mockRejectedValue({
          response: {
            data: {
              error: { message: errorMessage }
            }
          }
        })

        await expect(store.dispatch('cards/moveCard', {
          cardId: 1,
          oldListId: 1,
          newListId: 2,
          position: 0
        })).rejects.toBeDefined()

        expect(store.state.cards.error).toBe(errorMessage)
        expect(store.state.cards.loading).toBe(false)
      })
    })
  })

  describe('getters', () => {
    it('getCardsByListId should return cards for a specific list', () => {
      const list1Cards = [
        { id: 1, list_id: 1, title: 'Card 1' },
        { id: 2, list_id: 1, title: 'Card 2' }
      ]
      const list2Cards = [
        { id: 3, list_id: 2, title: 'Card 3' }
      ]
      
      store.commit('cards/setCards', { listId: 1, cards: list1Cards })
      store.commit('cards/setCards', { listId: 2, cards: list2Cards })
      
      expect(store.getters['cards/getCardsByListId'](1)).toEqual(list1Cards)
      expect(store.getters['cards/getCardsByListId'](2)).toEqual(list2Cards)
    })

    it('getCardsByListId should return empty array for non-existent list', () => {
      expect(store.getters['cards/getCardsByListId'](999)).toEqual([])
    })

    it('currentCard should return the current card', () => {
      const card = { id: 1, list_id: 1, title: 'Card 1' }
      store.commit('cards/setCurrentCard', card)
      
      expect(store.getters['cards/currentCard']).toEqual(card)
    })

    it('isLoading should return the loading state', () => {
      store.commit('cards/setLoading', true)
      expect(store.getters['cards/isLoading']).toBe(true)
      
      store.commit('cards/setLoading', false)
      expect(store.getters['cards/isLoading']).toBe(false)
    })

    it('error should return the error state', () => {
      const errorMessage = 'Test error'
      store.commit('cards/setError', errorMessage)
      
      expect(store.getters['cards/error']).toBe(errorMessage)
    })

    it('getCardById should return a specific card from a list', () => {
      const listCards = [
        { id: 1, list_id: 1, title: 'Card 1' },
        { id: 2, list_id: 1, title: 'Card 2' }
      ]
      
      store.commit('cards/setCards', { listId: 1, cards: listCards })
      
      expect(store.getters['cards/getCardById'](1, 1)).toEqual(listCards[0])
      expect(store.getters['cards/getCardById'](1, 2)).toEqual(listCards[1])
    })

    it('getCardById should return undefined for non-existent card', () => {
      const listCards = [{ id: 1, list_id: 1, title: 'Card 1' }]
      store.commit('cards/setCards', { listId: 1, cards: listCards })
      
      expect(store.getters['cards/getCardById'](1, 999)).toBeUndefined()
    })

    it('getCardById should return undefined for non-existent list', () => {
      expect(store.getters['cards/getCardById'](999, 1)).toBeUndefined()
    })
  })
})
