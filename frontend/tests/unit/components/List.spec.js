/**
 * List 组件单元测试
 * 
 * 测试内容：
 * - 组件渲染
 * - 列表名称编辑功能
 * - 列表删除功能
 * - 卡片显示
 * - 添加卡片功能
 * 
 * 需求：2.3, 2.4, 2.8, 3.2, 4.1, 4.3
 */
import { mount } from '@vue/test-utils'
import { createStore } from 'vuex'
import List from '@/components/List.vue'
import Card from '@/components/Card.vue'

describe('List.vue', () => {
  let store
  let listsModule
  let cardsModule
  
  // 测试数据
  const mockList = {
    id: 1,
    board_id: 1,
    name: '待办事项',
    position: 0
  }
  
  const mockCards = [
    {
      id: 1,
      list_id: 1,
      title: '任务1',
      description: '描述1',
      position: 0,
      tags: ['标签1']
    },
    {
      id: 2,
      list_id: 1,
      title: '任务2',
      description: null,
      position: 1,
      tags: []
    }
  ]
  
  beforeEach(() => {
    // 创建 mock store modules
    listsModule = {
      namespaced: true,
      state: {
        lists: [mockList],
        loading: false,
        error: null
      },
      mutations: {
        setLists: jest.fn(),
        updateList: jest.fn(),
        deleteList: jest.fn()
      },
      actions: {
        updateList: jest.fn(),
        deleteList: jest.fn()
      }
    }
    
    cardsModule = {
      namespaced: true,
      state: {
        cards: {
          1: mockCards
        },
        loading: false,
        error: null
      },
      mutations: {
        setCards: jest.fn(),
        addCard: jest.fn(),
        moveCard: jest.fn(),
        setCurrentCard: jest.fn()
      },
      actions: {
        fetchCards: jest.fn(),
        createCard: jest.fn(),
        moveCard: jest.fn()
      },
      getters: {
        getCardsByListId: (state) => (listId) => state.cards[listId] || []
      }
    }
    
    store = createStore({
      modules: {
        lists: listsModule,
        cards: cardsModule
      }
    })
  })
  
  /**
   * 测试组件渲染
   * 需求：2.3
   */
  describe('组件渲染', () => {
    it('应该正确渲染列表名称', () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      expect(wrapper.find('.list-title').text()).toBe('待办事项')
    })
    
    it('应该显示删除按钮', () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      expect(wrapper.find('.btn-delete').exists()).toBe(true)
    })
    
    it('应该显示添加卡片按钮', () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      expect(wrapper.find('.btn-add-card').exists()).toBe(true)
    })
    
    it('应该设置 data-list-id 属性', () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      expect(wrapper.find('.list').attributes('data-list-id')).toBe('1')
    })
  })
  
  /**
   * 测试列表名称编辑功能
   * 需求：2.3
   */
  describe('列表名称编辑', () => {
    it('点击列表名称应该进入编辑模式', async () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.list-title').trigger('click')
      
      expect(wrapper.vm.isEditingName).toBe(true)
      expect(wrapper.find('.list-title-input').exists()).toBe(true)
    })
    
    it('编辑模式下应该显示输入框', async () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        },
        attachTo: document.body
      })
      
      await wrapper.find('.list-title').trigger('click')
      await wrapper.vm.$nextTick()
      
      const input = wrapper.find('.list-title-input')
      expect(input.exists()).toBe(true)
      expect(input.element.value).toBe('待办事项')
      
      wrapper.unmount()
    })
    
    it('保存新名称应该调用 updateList action', async () => {
      const updateListSpy = jest.fn().mockResolvedValue({})
      listsModule.actions.updateList = updateListSpy
      
      store = createStore({
        modules: {
          lists: listsModule,
          cards: cardsModule
        }
      })
      
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.list-title').trigger('click')
      
      const input = wrapper.find('.list-title-input')
      await input.setValue('新列表名称')
      await input.trigger('blur')
      
      expect(updateListSpy).toHaveBeenCalledWith(
        expect.any(Object),
        {
          id: 1,
          data: { name: '新列表名称' }
        }
      )
    })
    
    it('按 Esc 键应该取消编辑', async () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.list-title').trigger('click')
      expect(wrapper.vm.isEditingName).toBe(true)
      
      const input = wrapper.find('.list-title-input')
      await input.trigger('keyup.esc')
      
      expect(wrapper.vm.isEditingName).toBe(false)
    })
    
    it('空名称不应该保存', async () => {
      const updateListSpy = jest.fn()
      listsModule.actions.updateList = updateListSpy
      
      store = createStore({
        modules: {
          lists: listsModule,
          cards: cardsModule
        }
      })
      
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.list-title').trigger('click')
      
      const input = wrapper.find('.list-title-input')
      await input.setValue('   ')
      await input.trigger('blur')
      
      expect(updateListSpy).not.toHaveBeenCalled()
      expect(wrapper.vm.isEditingName).toBe(false)
    })
  })
  
  /**
   * 测试列表删除功能
   * 需求：2.4
   */
  describe('列表删除', () => {
    it('点击删除按钮应该显示确认对话框', async () => {
      window.confirm = jest.fn(() => false)
      
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.btn-delete').trigger('click')
      
      expect(window.confirm).toHaveBeenCalledWith(
        expect.stringContaining('确定要删除列表"待办事项"吗？')
      )
    })
    
    it('确认删除应该调用 deleteList action', async () => {
      window.confirm = jest.fn(() => true)
      const deleteListSpy = jest.fn().mockResolvedValue({})
      listsModule.actions.deleteList = deleteListSpy
      
      store = createStore({
        modules: {
          lists: listsModule,
          cards: cardsModule
        }
      })
      
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.btn-delete').trigger('click')
      
      expect(deleteListSpy).toHaveBeenCalledWith(
        expect.any(Object),
        1
      )
    })
    
    it('取消删除不应该调用 deleteList action', async () => {
      window.confirm = jest.fn(() => false)
      const deleteListSpy = jest.fn()
      listsModule.actions.deleteList = deleteListSpy
      
      store = createStore({
        modules: {
          lists: listsModule,
          cards: cardsModule
        }
      })
      
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.btn-delete').trigger('click')
      
      expect(deleteListSpy).not.toHaveBeenCalled()
    })
  })
  
  /**
   * 测试卡片显示
   * 需求：3.1
   */
  describe('卡片显示', () => {
    it('应该显示列表中的所有卡片', () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store]
        },
        props: {
          list: mockList
        }
      })
      
      const cards = wrapper.findAllComponents(Card)
      expect(cards.length).toBe(2)
    })
    
    it('应该按位置排序显示卡片', () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      expect(wrapper.vm.sortedCards[0].title).toBe('任务1')
      expect(wrapper.vm.sortedCards[1].title).toBe('任务2')
    })
    
    it('组件挂载时应该获取卡片', () => {
      const fetchCardsSpy = jest.fn()
      cardsModule.actions.fetchCards = fetchCardsSpy
      
      store = createStore({
        modules: {
          lists: listsModule,
          cards: cardsModule
        }
      })
      
      mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      expect(fetchCardsSpy).toHaveBeenCalledWith(
        expect.any(Object),
        1
      )
    })
  })
  
  /**
   * 测试添加卡片功能
   * 需求：3.2
   */
  describe('添加卡片', () => {
    it('点击添加卡片按钮应该显示表单', async () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.btn-add-card').trigger('click')
      
      expect(wrapper.vm.showAddCardForm).toBe(true)
      expect(wrapper.find('.add-card-form').exists()).toBe(true)
    })
    
    it('提交表单应该调用 createCard action', async () => {
      const createCardSpy = jest.fn().mockResolvedValue({})
      cardsModule.actions.createCard = createCardSpy
      
      store = createStore({
        modules: {
          lists: listsModule,
          cards: cardsModule
        }
      })
      
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.btn-add-card').trigger('click')
      
      const input = wrapper.find('.card-title-input')
      await input.setValue('新卡片')
      
      await wrapper.find('.btn-submit').trigger('click')
      
      expect(createCardSpy).toHaveBeenCalledWith(
        expect.any(Object),
        {
          listId: 1,
          data: {
            title: '新卡片',
            position: 2
          }
        }
      )
    })
    
    it('空标题不应该创建卡片', async () => {
      const createCardSpy = jest.fn()
      cardsModule.actions.createCard = createCardSpy
      
      store = createStore({
        modules: {
          lists: listsModule,
          cards: cardsModule
        }
      })
      
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.btn-add-card').trigger('click')
      
      const input = wrapper.find('.card-title-input')
      await input.setValue('   ')
      
      await wrapper.find('.btn-submit').trigger('click')
      
      expect(createCardSpy).not.toHaveBeenCalled()
    })
    
    it('点击取消按钮应该隐藏表单', async () => {
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      await wrapper.find('.btn-add-card').trigger('click')
      expect(wrapper.vm.showAddCardForm).toBe(true)
      
      await wrapper.find('.btn-cancel').trigger('click')
      expect(wrapper.vm.showAddCardForm).toBe(false)
    })
  })
  
  /**
   * 测试卡片点击
   * 需求：3.6
   */
  describe('卡片点击', () => {
    it('点击卡片应该设置当前卡片', async () => {
      // Create a spy for the mutation
      const setCurrentCardSpy = jest.fn()
      cardsModule.mutations.setCurrentCard = setCurrentCardSpy
      
      store = createStore({
        modules: {
          lists: listsModule,
          cards: cardsModule
        }
      })
      
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            CardDetail: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      // Trigger the card click handler directly
      await wrapper.vm.handleCardClick(mockCards[0])
      
      expect(setCurrentCardSpy).toHaveBeenCalledWith(expect.any(Object), mockCards[0])
      expect(wrapper.vm.showCardDetail).toBe(true)
      expect(wrapper.vm.selectedCard).toEqual(mockCards[0])
    })
  })
  
  /**
   * 测试加载状态
   */
  describe('加载状态', () => {
    it('加载时应该禁用按钮', async () => {
      listsModule.state.loading = true
      
      store = createStore({
        modules: {
          lists: listsModule,
          cards: cardsModule
        }
      })
      
      const wrapper = mount(List, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true,
            Card: true
          }
        },
        props: {
          list: mockList
        }
      })
      
      expect(wrapper.find('.btn-delete').attributes('disabled')).toBeDefined()
      expect(wrapper.find('.btn-add-card').attributes('disabled')).toBeDefined()
    })
  })
})
