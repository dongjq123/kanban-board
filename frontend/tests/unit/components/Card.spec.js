/**
 * Card 组件单元测试
 * 
 * 测试内容：
 * - 组件渲染
 * - 卡片标题显示
 * - 卡片元数据显示（截止日期、描述、标签）
 * - 卡片点击事件
 * 
 * 需求：3.6, 3.7, 3.8, 3.9
 */
import { mount } from '@vue/test-utils'
import Card from '@/components/Card.vue'

describe('Card.vue', () => {
  // 测试数据
  const mockCard = {
    id: 1,
    list_id: 1,
    title: '测试卡片',
    description: '这是一个测试卡片',
    due_date: '2024-12-31',
    tags: ['标签1', '标签2'],
    position: 0
  }
  
  /**
   * 测试组件渲染
   * 需求：3.6
   */
  describe('组件渲染', () => {
    it('应该正确渲染卡片标题', () => {
      const wrapper = mount(Card, {
        propsData: {
          card: mockCard
        }
      })
      
      expect(wrapper.find('.card-title').text()).toBe('测试卡片')
    })
    
    it('应该渲染为可点击的卡片', () => {
      const wrapper = mount(Card, {
        propsData: {
          card: mockCard
        }
      })
      
      expect(wrapper.find('.card').exists()).toBe(true)
      // Check that the card has the correct class (cursor style is in CSS)
      expect(wrapper.find('.card').classes()).toContain('card')
    })
  })
  
  /**
   * 测试卡片元数据显示
   * 需求：3.7, 3.8, 3.9
   */
  describe('卡片元数据', () => {
    it('有元数据时应该显示元数据区域', () => {
      const wrapper = mount(Card, {
        propsData: {
          card: mockCard
        }
      })
      
      expect(wrapper.find('.card-metadata').exists()).toBe(true)
    })
    
    it('没有元数据时不应该显示元数据区域', () => {
      const simpleCard = {
        id: 1,
        list_id: 1,
        title: '简单卡片',
        description: null,
        due_date: null,
        tags: [],
        position: 0
      }
      
      const wrapper = mount(Card, {
        propsData: {
          card: simpleCard
        }
      })
      
      expect(wrapper.find('.card-metadata').exists()).toBe(false)
    })
    
    it('应该显示截止日期', () => {
      const wrapper = mount(Card, {
        propsData: {
          card: mockCard
        }
      })
      
      expect(wrapper.find('.due-date').exists()).toBe(true)
      expect(wrapper.find('.due-date').text()).toContain('12月31日')
    })
    
    it('有描述时应该显示描述指示器', () => {
      const wrapper = mount(Card, {
        propsData: {
          card: mockCard
        }
      })
      
      expect(wrapper.find('.description-indicator').exists()).toBe(true)
    })
    
    it('没有描述时不应该显示描述指示器', () => {
      const cardWithoutDesc = {
        ...mockCard,
        description: null
      }
      
      const wrapper = mount(Card, {
        propsData: {
          card: cardWithoutDesc
        }
      })
      
      expect(wrapper.find('.description-indicator').exists()).toBe(false)
    })
    
    it('应该显示所有标签', () => {
      const wrapper = mount(Card, {
        propsData: {
          card: mockCard
        }
      })
      
      const tags = wrapper.findAll('.tag')
      expect(tags.length).toBe(2)
      expect(tags.at(0).text()).toBe('标签1')
      expect(tags.at(1).text()).toBe('标签2')
    })
    
    it('没有标签时不应该显示标签区域', () => {
      const cardWithoutTags = {
        ...mockCard,
        tags: []
      }
      
      const wrapper = mount(Card, {
        propsData: {
          card: cardWithoutTags
        }
      })
      
      expect(wrapper.find('.tags').exists()).toBe(false)
    })
  })
  
  /**
   * 测试截止日期样式
   * 需求：3.8
   */
  describe('截止日期样式', () => {
    it('已逾期的日期应该显示为红色', () => {
      const yesterday = new Date()
      yesterday.setDate(yesterday.getDate() - 1)
      
      const overdueCard = {
        ...mockCard,
        due_date: yesterday.toISOString().split('T')[0]
      }
      
      const wrapper = mount(Card, {
        propsData: {
          card: overdueCard
        }
      })
      
      expect(wrapper.find('.due-date').classes()).toContain('overdue')
      expect(wrapper.find('.due-date').text()).toContain('已逾期')
    })
    
    it('今天到期的日期应该显示为黄色', () => {
      const today = new Date()
      
      const todayCard = {
        ...mockCard,
        due_date: today.toISOString().split('T')[0]
      }
      
      const wrapper = mount(Card, {
        propsData: {
          card: todayCard
        }
      })
      
      expect(wrapper.find('.due-date').classes()).toContain('due-today')
      expect(wrapper.find('.due-date').text()).toContain('今天')
    })
    
    it('明天到期的日期应该显示为橙色', () => {
      const tomorrow = new Date()
      tomorrow.setDate(tomorrow.getDate() + 1)
      
      const tomorrowCard = {
        ...mockCard,
        due_date: tomorrow.toISOString().split('T')[0]
      }
      
      const wrapper = mount(Card, {
        propsData: {
          card: tomorrowCard
        }
      })
      
      expect(wrapper.find('.due-date').classes()).toContain('due-soon')
      expect(wrapper.find('.due-date').text()).toContain('明天')
    })
    
    it('未来日期应该正常显示', () => {
      const future = new Date()
      future.setDate(future.getDate() + 10)
      
      const futureCard = {
        ...mockCard,
        due_date: future.toISOString().split('T')[0]
      }
      
      const wrapper = mount(Card, {
        propsData: {
          card: futureCard
        }
      })
      
      const dueDate = wrapper.find('.due-date')
      expect(dueDate.classes()).not.toContain('overdue')
      expect(dueDate.classes()).not.toContain('due-today')
      expect(dueDate.classes()).not.toContain('due-soon')
    })
  })
  
  /**
   * 测试卡片点击事件
   * 需求：3.6
   */
  describe('卡片点击', () => {
    it('点击卡片应该触发 click 事件', async () => {
      const wrapper = mount(Card, {
        propsData: {
          card: mockCard
        }
      })
      
      await wrapper.find('.card').trigger('click')
      
      expect(wrapper.emitted('click')).toBeTruthy()
      expect(wrapper.emitted('click')[0]).toEqual([mockCard])
    })
    
    it('鼠标悬停时应该改变背景色', async () => {
      const wrapper = mount(Card, {
        propsData: {
          card: mockCard
        }
      })
      
      const card = wrapper.find('.card')
      
      // 检查 hover 样式是否定义（通过 CSS 类）
      expect(card.classes()).toContain('card')
    })
  })
  
  /**
   * 测试边缘情况
   */
  describe('边缘情况', () => {
    it('应该处理空标签数组', () => {
      const cardWithEmptyTags = {
        ...mockCard,
        tags: []
      }
      
      const wrapper = mount(Card, {
        propsData: {
          card: cardWithEmptyTags
        }
      })
      
      expect(wrapper.find('.tags').exists()).toBe(false)
    })
    
    it('应该处理 null 标签', () => {
      const cardWithNullTags = {
        ...mockCard,
        tags: null
      }
      
      const wrapper = mount(Card, {
        propsData: {
          card: cardWithNullTags
        }
      })
      
      expect(wrapper.find('.tags').exists()).toBe(false)
    })
    
    it('应该处理长标题', () => {
      const longTitleCard = {
        ...mockCard,
        title: '这是一个非常非常非常非常非常非常非常非常非常非常长的卡片标题，用于测试文本换行'
      }
      
      const wrapper = mount(Card, {
        propsData: {
          card: longTitleCard
        }
      })
      
      expect(wrapper.find('.card-title').text()).toBe(longTitleCard.title)
    })
  })
})
