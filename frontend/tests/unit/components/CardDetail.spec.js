/**
 * CardDetail 组件单元测试
 * 
 * 测试内容：
 * - 组件渲染
 * - 编辑卡片标题
 * - 编辑卡片描述
 * - 添加/编辑截止日期
 * - 添加/移除标签
 * - 删除卡片
 * - 模态框关闭
 * 
 * 需求：3.4, 3.5, 3.7, 3.8, 3.9
 */
import { mount } from '@vue/test-utils'
import { createStore } from 'vuex'
import CardDetail from '@/components/CardDetail.vue'

// 创建模拟的 Vuex store
const createMockStore = (mockActions = {}) => {
  const defaultActions = {
    updateCard: jest.fn(() => Promise.resolve({ data: {} })),
    deleteCard: jest.fn(() => Promise.resolve())
  }
  
  const actions = { ...defaultActions, ...mockActions }
  
  return createStore({
    modules: {
      cards: {
        namespaced: true,
        state: {
          loading: false,
          error: null
        },
        actions
      }
    }
  })
}

describe('CardDetail.vue', () => {
  let wrapper
  let store
  
  const mockCard = {
    id: 1,
    list_id: 1,
    title: '测试卡片',
    description: '这是一个测试描述',
    due_date: '2024-12-31',
    tags: ['标签1', '标签2'],
    position: 0
  }
  
  beforeEach(() => {
    store = createMockStore()
  })
  
  afterEach(() => {
    if (wrapper) {
      wrapper.unmount()
    }
  })
  
  /**
   * 测试组件渲染
   */
  describe('组件渲染', () => {
    it('当 visible 为 false 时不显示模态框', () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: false,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      expect(wrapper.find('.modal-overlay').exists()).toBe(false)
    })
    
    it('当 visible 为 true 时显示模态框', () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      expect(wrapper.find('.modal-overlay').exists()).toBe(true)
    })
    
    it('显示卡片标题', () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      expect(wrapper.find('.card-title').text()).toBe('测试卡片')
    })
    
    it('显示列表名称', () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      expect(wrapper.find('.list-name').text()).toBe('测试列表')
    })
    
    it('显示卡片描述', () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      expect(wrapper.find('.description-text').text()).toBe('这是一个测试描述')
    })
    
    it('显示截止日期', () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      expect(wrapper.find('.date-input').element.value).toBe('2024-12-31')
    })
    
    it('显示标签列表', () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      const tags = wrapper.findAll('.tag')
      expect(tags).toHaveLength(2)
      expect(tags[0].text()).toContain('标签1')
      expect(tags[1].text()).toContain('标签2')
    })
  })
  
  /**
   * 测试编辑卡片标题
   * 需求：3.4
   */
  describe('编辑卡片标题', () => {
    it('点击标题进入编辑模式', async () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.card-title').trigger('click')
      
      expect(wrapper.find('.title-input').exists()).toBe(true)
      expect(wrapper.find('.title-input').element.value).toBe('测试卡片')
    })
    
    it('保存新标题时调用 updateCard action', async () => {
      const updateCardMock = jest.fn(() => Promise.resolve({ data: {} }))
      store = createMockStore({ updateCard: updateCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      // 进入编辑模式
      await wrapper.find('.card-title').trigger('click')
      
      // 修改标题
      const input = wrapper.find('.title-input')
      await input.setValue('新标题')
      
      // 触发保存（失焦）
      await input.trigger('blur')
      await wrapper.vm.$nextTick()
      
      // 验证 action 被调用
      expect(updateCardMock).toHaveBeenCalledWith(
        expect.anything(),
        {
          id: 1,
          data: { title: '新标题' }
        }
      )
    })
    
    it('按 Enter 键保存标题', async () => {
      const updateCardMock = jest.fn(() => Promise.resolve({ data: {} }))
      store = createMockStore({ updateCard: updateCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.card-title').trigger('click')
      const input = wrapper.find('.title-input')
      await input.setValue('新标题')
      await input.trigger('keyup.enter')
      await wrapper.vm.$nextTick()
      
      expect(updateCardMock).toHaveBeenCalled()
    })
    
    it('按 Esc 键取消编辑', async () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.card-title').trigger('click')
      const input = wrapper.find('.title-input')
      await input.setValue('新标题')
      await input.trigger('keyup.esc')
      
      // 应该退出编辑模式
      expect(wrapper.find('.title-input').exists()).toBe(false)
      expect(wrapper.find('.card-title').exists()).toBe(true)
    })
  })
  
  /**
   * 测试编辑卡片描述
   * 需求：3.7
   */
  describe('编辑卡片描述', () => {
    it('点击"编辑"按钮进入编辑模式', async () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.btn-edit').trigger('click')
      
      expect(wrapper.find('.description-input').exists()).toBe(true)
      expect(wrapper.find('.description-input').element.value).toBe('这是一个测试描述')
    })
    
    it('点击"添加更详细的描述"按钮进入编辑模式（无描述时）', async () => {
      const cardWithoutDescription = { ...mockCard, description: null }
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: cardWithoutDescription,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.btn-add-description').trigger('click')
      
      expect(wrapper.find('.description-input').exists()).toBe(true)
    })
    
    it('保存描述时调用 updateCard action', async () => {
      const updateCardMock = jest.fn(() => Promise.resolve({ data: {} }))
      store = createMockStore({ updateCard: updateCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.btn-edit').trigger('click')
      const textarea = wrapper.find('.description-input')
      await textarea.setValue('新的描述内容')
      await wrapper.find('.btn-save').trigger('click')
      await wrapper.vm.$nextTick()
      
      expect(updateCardMock).toHaveBeenCalledWith(
        expect.anything(),
        {
          id: 1,
          data: { description: '新的描述内容' }
        }
      )
    })
    
    it('点击"取消"按钮退出编辑模式', async () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.btn-edit').trigger('click')
      await wrapper.find('.btn-cancel').trigger('click')
      
      expect(wrapper.find('.description-input').exists()).toBe(false)
      expect(wrapper.find('.description-display').exists()).toBe(true)
    })
  })
  
  /**
   * 测试截止日期
   * 需求：3.8
   */
  describe('截止日期', () => {
    it('修改截止日期时调用 updateCard action', async () => {
      const updateCardMock = jest.fn(() => Promise.resolve({ data: {} }))
      store = createMockStore({ updateCard: updateCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      const dateInput = wrapper.find('.date-input')
      await dateInput.setValue('2025-01-15')
      await dateInput.trigger('change')
      await wrapper.vm.$nextTick()
      
      expect(updateCardMock).toHaveBeenCalledWith(
        expect.anything(),
        {
          id: 1,
          data: { due_date: '2025-01-15' }
        }
      )
    })
    
    it('点击"清除"按钮清除截止日期', async () => {
      const updateCardMock = jest.fn(() => Promise.resolve({ data: {} }))
      store = createMockStore({ updateCard: updateCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.btn-clear-date').trigger('click')
      await wrapper.vm.$nextTick()
      
      expect(updateCardMock).toHaveBeenCalledWith(
        expect.anything(),
        {
          id: 1,
          data: { due_date: null }
        }
      )
    })
  })
  
  /**
   * 测试标签
   * 需求：3.9
   */
  describe('标签', () => {
    it('添加新标签时调用 updateCard action', async () => {
      const updateCardMock = jest.fn(() => Promise.resolve({ data: {} }))
      store = createMockStore({ updateCard: updateCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      const tagInput = wrapper.find('.tag-input')
      await tagInput.setValue('新标签')
      await wrapper.find('.btn-add-tag').trigger('click')
      await wrapper.vm.$nextTick()
      
      expect(updateCardMock).toHaveBeenCalledWith(
        expect.anything(),
        {
          id: 1,
          data: { tags: ['标签1', '标签2', '新标签'] }
        }
      )
    })
    
    it('按 Enter 键添加标签', async () => {
      const updateCardMock = jest.fn(() => Promise.resolve({ data: {} }))
      store = createMockStore({ updateCard: updateCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      const tagInput = wrapper.find('.tag-input')
      await tagInput.setValue('新标签')
      await tagInput.trigger('keyup.enter')
      await wrapper.vm.$nextTick()
      
      expect(updateCardMock).toHaveBeenCalled()
    })
    
    it('移除标签时调用 updateCard action', async () => {
      const updateCardMock = jest.fn(() => Promise.resolve({ data: {} }))
      store = createMockStore({ updateCard: updateCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      const removeButtons = wrapper.findAll('.btn-remove-tag')
      await removeButtons[0].trigger('click')
      await wrapper.vm.$nextTick()
      
      expect(updateCardMock).toHaveBeenCalledWith(
        expect.anything(),
        {
          id: 1,
          data: { tags: ['标签2'] }
        }
      )
    })
    
    it('不允许添加重复标签', async () => {
      // Mock window.alert
      global.alert = jest.fn()
      
      const updateCardMock = jest.fn(() => Promise.resolve({ data: {} }))
      store = createMockStore({ updateCard: updateCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      const tagInput = wrapper.find('.tag-input')
      await tagInput.setValue('标签1')
      await wrapper.find('.btn-add-tag').trigger('click')
      await wrapper.vm.$nextTick()
      
      expect(global.alert).toHaveBeenCalledWith('该标签已存在')
      expect(updateCardMock).not.toHaveBeenCalled()
    })
  })
  
  /**
   * 测试删除卡片
   * 需求：3.5
   */
  describe('删除卡片', () => {
    it('点击删除按钮显示确认对话框', async () => {
      // Mock window.confirm
      global.confirm = jest.fn(() => false)
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.btn-delete-card').trigger('click')
      
      expect(global.confirm).toHaveBeenCalledWith(
        expect.stringContaining('确定要删除卡片"测试卡片"吗？')
      )
    })
    
    it('确认删除时调用 deleteCard action', async () => {
      global.confirm = jest.fn(() => true)
      
      const deleteCardMock = jest.fn(() => Promise.resolve())
      store = createMockStore({ deleteCard: deleteCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.btn-delete-card').trigger('click')
      await wrapper.vm.$nextTick()
      
      expect(deleteCardMock).toHaveBeenCalledWith(
        expect.anything(),
        {
          cardId: 1,
          listId: 1
        }
      )
    })
    
    it('取消删除时不调用 deleteCard action', async () => {
      global.confirm = jest.fn(() => false)
      
      const deleteCardMock = jest.fn(() => Promise.resolve())
      store = createMockStore({ deleteCard: deleteCardMock })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.btn-delete-card').trigger('click')
      await wrapper.vm.$nextTick()
      
      expect(deleteCardMock).not.toHaveBeenCalled()
    })
  })
  
  /**
   * 测试模态框关闭
   */
  describe('模态框关闭', () => {
    it('点击关闭按钮触发 close 事件', async () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.btn-close').trigger('click')
      
      expect(wrapper.emitted('close')).toBeTruthy()
    })
    
    it('点击遮罩层触发 close 事件', async () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      await wrapper.find('.modal-overlay').trigger('click')
      
      expect(wrapper.emitted('close')).toBeTruthy()
    })
    
    it('关闭时重置编辑状态', async () => {
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [store]
        }
      })
      
      // 进入标题编辑模式
      await wrapper.find('.card-title').trigger('click')
      expect(wrapper.find('.title-input').exists()).toBe(true)
      
      // 关闭模态框
      await wrapper.find('.btn-close').trigger('click')
      
      // 重新打开
      await wrapper.setProps({ visible: false })
      await wrapper.setProps({ visible: true })
      
      // 应该不在编辑模式
      expect(wrapper.find('.title-input').exists()).toBe(false)
    })
  })
  
  /**
   * 测试加载状态
   */
  describe('加载状态', () => {
    it('加载时显示加载指示器', async () => {
      const loadingStore = createStore({
        modules: {
          cards: {
            namespaced: true,
            state: {
              loading: true,
              error: null
            },
            actions: {
              updateCard: jest.fn(() => Promise.resolve({ data: {} })),
              deleteCard: jest.fn(() => Promise.resolve())
            }
          }
        }
      })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [loadingStore]
        }
      })
      
      expect(wrapper.find('.loading-overlay').exists()).toBe(true)
      expect(wrapper.find('.spinner').exists()).toBe(true)
    })
    
    it('加载时禁用所有按钮', async () => {
      const loadingStore = createStore({
        modules: {
          cards: {
            namespaced: true,
            state: {
              loading: true,
              error: null
            },
            actions: {
              updateCard: jest.fn(() => Promise.resolve({ data: {} })),
              deleteCard: jest.fn(() => Promise.resolve())
            }
          }
        }
      })
      
      wrapper = mount(CardDetail, {
        props: {
          visible: true,
          card: mockCard,
          listName: '测试列表'
        },
        global: {
          plugins: [loadingStore]
        }
      })
      
      expect(wrapper.find('.btn-close').element.disabled).toBe(true)
      expect(wrapper.find('.btn-edit').element.disabled).toBe(true)
      expect(wrapper.find('.btn-delete-card').element.disabled).toBe(true)
    })
  })
})
