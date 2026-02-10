/**
 * BoardList 组件单元测试
 * 
 * 需求：1.1, 1.3, 1.5
 */
import { mount } from '@vue/test-utils'
import { createStore } from 'vuex'
import BoardList from '@/components/BoardList.vue'

describe('BoardList.vue', () => {
  let store
  let mockBoards

  beforeEach(() => {
    mockBoards = [
      { id: 1, name: 'Test Board 1', created_at: '2024-01-01' },
      { id: 2, name: 'Test Board 2', created_at: '2024-01-02' }
    ]

    store = createStore({
      modules: {
        boards: {
          namespaced: true,
          state: {
            boards: mockBoards,
            loading: false,
            error: null
          },
          getters: {
            allBoards: state => state.boards
          },
          actions: {
            fetchBoards: jest.fn(),
            createBoard: jest.fn(),
            deleteBoard: jest.fn()
          },
          mutations: {
            setCurrentBoard: jest.fn()
          }
        }
      }
    })
  })

  it('should render component', () => {
    const wrapper = mount(BoardList, {
      global: {
        plugins: [store]
      }
    })

    expect(wrapper.exists()).toBe(true)
  })
})
