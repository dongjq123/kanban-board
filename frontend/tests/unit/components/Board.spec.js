/**
 * Board 组件单元测试
 * 
 * 测试内容：
 * - 组件渲染
 * - 看板名称编辑功能
 * - 添加新列表功能
 * - 列表拖拽排序功能
 * - 错误处理
 * 
 * 需求：1.4, 2.1, 2.6
 */
import { mount, flushPromises } from '@vue/test-utils'
import { createStore } from 'vuex'
import Board from '@/components/Board.vue'
import List from '@/components/List.vue'
import draggable from 'vuedraggable'

// Mock List component
jest.mock('@/components/List.vue', () => ({
  name: 'List',
  template: '<div class="list-mock">{{ list.name }}</div>',
  props: ['list']
}))

describe('Board.vue', () => {
  let store
  let mockBoards
  let mockLists
  
  beforeEach(() => {
    // 创建 mock store
    mockBoards = {
      namespaced: true,
      state: {
        currentBoard: {
          id: 1,
          name: '测试看板',
          created_at: '2024-01-15T10:00:00Z'
        },
        loading: false,
        error: null
      },
      mutations: {
        setCurrentBoard: jest.fn(),
        setError: jest.fn()
      },
      actions: {
        updateBoard: jest.fn()
      }
    }
    
    mockLists = {
      namespaced: true,
      state: {
        lists: [
          { id: 1, board_id: 1, name: '待办', position: 0 },
          { id: 2, board_id: 1, name: '进行中', position: 1 },
          { id: 3, board_id: 1, name: '完成', position: 2 }
        ],
        loading: false,
        error: null
      },
      mutations: {
        setLists: jest.fn()
      },
      actions: {
        fetchLists: jest.fn(),
        createList: jest.fn(),
        updateListPosition: jest.fn()
      }
    }
    
    store = createStore({
      modules: {
        boards: mockBoards,
        lists: mockLists
      }
    })
  })
  
  /**
   * 测试组件渲染
   */
  describe('组件渲染', () => {
    it('应该正确渲染看板名称', () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      expect(wrapper.find('.board-title').text()).toBe('测试看板')
    })
    
    it('应该渲染所有列表', () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: false // Don't stub draggable so we can find List components
          }
        }
      })
      
      const lists = wrapper.findAllComponents({ name: 'List' })
      expect(lists).toHaveLength(3)
    })
    
    it('应该显示添加列表按钮', () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      expect(wrapper.find('.btn-add-list').exists()).toBe(true)
      expect(wrapper.find('.btn-add-list').text()).toBe('+ 添加列表')
    })
    
    it('应该显示返回按钮', () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      expect(wrapper.find('.btn-back').exists()).toBe(true)
    })
  })
  
  /**
   * 测试看板名称编辑功能
   * 需求：1.4
   */
  describe('看板名称编辑', () => {
    it('点击看板名称应该显示编辑输入框', async () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      await wrapper.find('.board-title').trigger('click')
      await wrapper.vm.$nextTick()
      
      expect(wrapper.find('.board-title-input').exists()).toBe(true)
      expect(wrapper.find('.board-title-input').element.value).toBe('测试看板')
    })
    
    it('按 Enter 键应该保存看板名称', async () => {
      mockBoards.actions.updateBoard.mockResolvedValue({
        data: { id: 1, name: '新看板名称' }
      })
      
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      // 开始编辑
      await wrapper.find('.board-title').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 修改名称
      const input = wrapper.find('.board-title-input')
      await input.setValue('新看板名称')
      await input.trigger('keyup.enter')
      await flushPromises()
      
      // 验证调用了 updateBoard action
      expect(mockBoards.actions.updateBoard).toHaveBeenCalledWith(
        expect.any(Object),
        {
          id: 1,
          data: { name: '新看板名称' }
        }
      )
    })
    
    it('按 Esc 键应该取消编辑', async () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      // 开始编辑
      await wrapper.find('.board-title').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 修改名称
      const input = wrapper.find('.board-title-input')
      await input.setValue('新看板名称')
      
      // 按 Esc 取消
      await input.trigger('keyup.esc')
      await wrapper.vm.$nextTick()
      
      // 验证没有调用 updateBoard
      expect(mockBoards.actions.updateBoard).not.toHaveBeenCalled()
      
      // 验证显示原来的名称
      expect(wrapper.find('.board-title').text()).toBe('测试看板')
    })
    
    it('输入框失焦应该保存看板名称', async () => {
      mockBoards.actions.updateBoard.mockResolvedValue({
        data: { id: 1, name: '新看板名称' }
      })
      
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      // 开始编辑
      await wrapper.find('.board-title').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 修改名称
      const input = wrapper.find('.board-title-input')
      await input.setValue('新看板名称')
      await input.trigger('blur')
      await flushPromises()
      
      // 验证调用了 updateBoard action
      expect(mockBoards.actions.updateBoard).toHaveBeenCalled()
    })
    
    it('空名称不应该保存', async () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      // 开始编辑
      await wrapper.find('.board-title').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 设置空名称
      const input = wrapper.find('.board-title-input')
      await input.setValue('   ')
      await input.trigger('blur')
      await flushPromises()
      
      // 验证没有调用 updateBoard
      expect(mockBoards.actions.updateBoard).not.toHaveBeenCalled()
    })
  })
  
  /**
   * 测试添加新列表功能
   * 需求：2.1
   */
  describe('添加新列表', () => {
    it('点击添加列表按钮应该显示表单', async () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      await wrapper.find('.btn-add-list').trigger('click')
      await wrapper.vm.$nextTick()
      
      expect(wrapper.find('.add-list-form').exists()).toBe(true)
      expect(wrapper.find('.list-name-input').exists()).toBe(true)
    })
    
    it('应该能够创建新列表', async () => {
      mockLists.actions.createList.mockResolvedValue({
        data: { id: 4, board_id: 1, name: '新列表', position: 3 }
      })
      
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      // 显示表单
      await wrapper.find('.btn-add-list').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 输入列表名称
      const input = wrapper.find('.list-name-input')
      await input.setValue('新列表')
      
      // 点击添加按钮
      await wrapper.find('.btn-submit').trigger('click')
      await flushPromises()
      
      // 验证调用了 createList action
      expect(mockLists.actions.createList).toHaveBeenCalledWith(
        expect.any(Object),
        {
          boardId: 1,
          data: { name: '新列表', position: 3 }
        }
      )
    })
    
    it('按 Enter 键应该创建列表', async () => {
      mockLists.actions.createList.mockResolvedValue({
        data: { id: 4, board_id: 1, name: '新列表', position: 3 }
      })
      
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      // 显示表单
      await wrapper.find('.btn-add-list').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 输入列表名称并按 Enter
      const input = wrapper.find('.list-name-input')
      await input.setValue('新列表')
      await input.trigger('keyup.enter')
      await flushPromises()
      
      // 验证调用了 createList action
      expect(mockLists.actions.createList).toHaveBeenCalled()
    })
    
    it('按 Esc 键应该取消添加', async () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      // 显示表单
      await wrapper.find('.btn-add-list').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 输入列表名称
      const input = wrapper.find('.list-name-input')
      await input.setValue('新列表')
      
      // 按 Esc 取消
      await input.trigger('keyup.esc')
      await wrapper.vm.$nextTick()
      
      // 验证没有调用 createList
      expect(mockLists.actions.createList).not.toHaveBeenCalled()
      
      // 验证表单已隐藏
      expect(wrapper.find('.add-list-form').exists()).toBe(false)
    })
    
    it('点击取消按钮应该隐藏表单', async () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      // 显示表单
      await wrapper.find('.btn-add-list').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 点击取消按钮
      await wrapper.find('.btn-cancel').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 验证表单已隐藏
      expect(wrapper.find('.add-list-form').exists()).toBe(false)
    })
    
    it('空名称不应该创建列表', async () => {
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      // 显示表单
      await wrapper.find('.btn-add-list').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 输入空名称
      const input = wrapper.find('.list-name-input')
      await input.setValue('   ')
      
      // 验证提交按钮被禁用
      expect(wrapper.find('.btn-submit').element.disabled).toBe(true)
    })
  })
  
  /**
   * 测试加载状态
   */
  describe('加载状态', () => {
    it('加载时应该显示加载指示器', () => {
      mockLists.state.loading = true
      mockLists.state.lists = []
      
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      expect(wrapper.find('.loading').exists()).toBe(true)
      expect(wrapper.find('.spinner').exists()).toBe(true)
    })
  })
  
  /**
   * 测试错误处理
   */
  describe('错误处理', () => {
    it('应该显示错误消息', () => {
      mockLists.state.error = '获取列表失败'
      
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      expect(wrapper.find('.error-message').exists()).toBe(true)
      expect(wrapper.find('.error-message').text()).toBe('获取列表失败')
    })
  })
  
  /**
   * 测试返回功能
   */
  describe('返回功能', () => {
    it('点击返回按钮应该清除当前看板和列表', async () => {
      // Mock window.alert
      window.alert = jest.fn()
      
      const wrapper = mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      await wrapper.find('.btn-back').trigger('click')
      await wrapper.vm.$nextTick()
      
      // 验证调用了 mutations
      expect(mockBoards.mutations.setCurrentBoard).toHaveBeenCalledWith(
        expect.any(Object),
        null
      )
      expect(mockLists.mutations.setLists).toHaveBeenCalledWith(
        expect.any(Object),
        []
      )
    })
  })
  
  /**
   * 测试组件挂载
   */
  describe('组件挂载', () => {
    it('挂载时应该获取列表', () => {
      mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      expect(mockLists.actions.fetchLists).toHaveBeenCalledWith(
        expect.any(Object),
        1
      )
    })
    
    it('没有当前看板时应该显示错误', () => {
      mockBoards.state.currentBoard = null
      
      mount(Board, {
        global: {
          plugins: [store],
          stubs: {
            draggable: true
          }
        }
      })
      
      expect(mockBoards.mutations.setError).toHaveBeenCalledWith(
        expect.any(Object),
        '请先选择一个看板'
      )
    })
  })
})
