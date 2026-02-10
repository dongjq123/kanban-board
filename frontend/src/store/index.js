// Vuex store configuration - to be implemented in task 9
import { createStore } from 'vuex'
import boards from './modules/boards'
import lists from './modules/lists'
import cards from './modules/cards'
import auth from './modules/auth'

export default createStore({
  modules: {
    boards,
    lists,
    cards,
    auth
  }
})
