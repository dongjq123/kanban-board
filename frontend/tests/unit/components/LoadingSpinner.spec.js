/**
 * LoadingSpinner 组件单元测试
 * 
 * 测试范围：
 * - 组件渲染
 * - 尺寸变体（small, normal）
 * - CSS 类名应用
 * - 样式属性验证
 * - Props 验证
 * 
 * 需求：7.1, 7.4
 */

import { mount } from '@vue/test-utils'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

describe('LoadingSpinner.vue', () => {
  describe('基本渲染', () => {
    it('应该渲染加载指示器', () => {
      const wrapper = mount(LoadingSpinner)
      
      expect(wrapper.find('.loading-spinner').exists()).toBe(true)
      expect(wrapper.find('.loading-spinner__circle').exists()).toBe(true)
    })
    
    it('默认应该使用 normal 尺寸', () => {
      const wrapper = mount(LoadingSpinner)
      
      expect(wrapper.find('.loading-spinner--normal').exists()).toBe(true)
      expect(wrapper.find('.loading-spinner--small').exists()).toBe(false)
    })
  })
  
  describe('尺寸变体', () => {
    it('应该支持 small 尺寸', () => {
      const wrapper = mount(LoadingSpinner, {
        props: {
          size: 'small'
        }
      })
      
      expect(wrapper.find('.loading-spinner--small').exists()).toBe(true)
      expect(wrapper.find('.loading-spinner--normal').exists()).toBe(false)
    })
    
    it('应该支持 normal 尺寸', () => {
      const wrapper = mount(LoadingSpinner, {
        props: {
          size: 'normal'
        }
      })
      
      expect(wrapper.find('.loading-spinner--normal').exists()).toBe(true)
      expect(wrapper.find('.loading-spinner--small').exists()).toBe(false)
    })
    
    it('切换尺寸应该更新 CSS 类', async () => {
      const wrapper = mount(LoadingSpinner, {
        props: {
          size: 'normal'
        }
      })
      
      expect(wrapper.find('.loading-spinner--normal').exists()).toBe(true)
      
      await wrapper.setProps({ size: 'small' })
      
      expect(wrapper.find('.loading-spinner--small').exists()).toBe(true)
      expect(wrapper.find('.loading-spinner--normal').exists()).toBe(false)
    })
  })
  
  describe('Props 验证', () => {
    it('size 属性应该只接受 small 或 normal', () => {
      const validator = LoadingSpinner.props.size.validator
      
      expect(validator('small')).toBe(true)
      expect(validator('normal')).toBe(true)
      expect(validator('large')).toBe(false)
      expect(validator('invalid')).toBe(false)
      expect(validator('')).toBe(false)
    })
    
    it('size 属性默认值应该是 normal', () => {
      expect(LoadingSpinner.props.size.default).toBe('normal')
    })
  })
  
  describe('CSS 类名', () => {
    it('应该始终包含基础类名', () => {
      const wrapper = mount(LoadingSpinner)
      
      expect(wrapper.classes()).toContain('loading-spinner')
    })
    
    it('应该根据 size prop 添加对应的修饰类', () => {
      const wrapperNormal = mount(LoadingSpinner, {
        props: { size: 'normal' }
      })
      const wrapperSmall = mount(LoadingSpinner, {
        props: { size: 'small' }
      })
      
      expect(wrapperNormal.classes()).toContain('loading-spinner--normal')
      expect(wrapperSmall.classes()).toContain('loading-spinner--small')
    })
    
    it('圆圈元素应该包含正确的类名', () => {
      const wrapper = mount(LoadingSpinner)
      const circle = wrapper.find('.loading-spinner__circle')
      
      expect(circle.exists()).toBe(true)
      expect(circle.classes()).toContain('loading-spinner__circle')
    })
  })
  
  describe('计算属性', () => {
    it('spinnerSizeClass 应该返回正确的类名', () => {
      const wrapperNormal = mount(LoadingSpinner, {
        props: { size: 'normal' }
      })
      const wrapperSmall = mount(LoadingSpinner, {
        props: { size: 'small' }
      })
      
      expect(wrapperNormal.vm.spinnerSizeClass).toBe('loading-spinner--normal')
      expect(wrapperSmall.vm.spinnerSizeClass).toBe('loading-spinner--small')
    })
  })
  
  describe('样式类应用', () => {
    it('normal 尺寸应该应用正确的 CSS 类', () => {
      const wrapper = mount(LoadingSpinner, {
        props: { size: 'normal' }
      })
      
      const spinner = wrapper.find('.loading-spinner')
      
      // 验证应用了正确的尺寸类
      expect(spinner.classes()).toContain('loading-spinner--normal')
      expect(wrapper.find('.loading-spinner__circle').exists()).toBe(true)
    })
    
    it('small 尺寸应该应用正确的 CSS 类', () => {
      const wrapper = mount(LoadingSpinner, {
        props: { size: 'small' }
      })
      
      const spinner = wrapper.find('.loading-spinner')
      
      // 验证应用了正确的尺寸类
      expect(spinner.classes()).toContain('loading-spinner--small')
      expect(wrapper.find('.loading-spinner__circle').exists()).toBe(true)
    })
    
    it('圆圈元素应该存在并有正确的类名', () => {
      const wrapper = mount(LoadingSpinner)
      
      const circle = wrapper.find('.loading-spinner__circle')
      
      expect(circle.exists()).toBe(true)
      expect(circle.classes()).toContain('loading-spinner__circle')
    })
  })
  
  describe('可访问性', () => {
    it('组件应该有清晰的结构便于识别', () => {
      const wrapper = mount(LoadingSpinner)
      
      const spinner = wrapper.find('.loading-spinner')
      const circle = wrapper.find('.loading-spinner__circle')
      
      // 验证组件结构清晰
      expect(spinner.exists()).toBe(true)
      expect(circle.exists()).toBe(true)
    })
  })
  
  describe('边缘情况', () => {
    it('无效的 size 值应该被验证器拒绝', () => {
      const validator = LoadingSpinner.props.size.validator
      
      expect(validator(null)).toBe(false)
      expect(validator(undefined)).toBe(false)
      expect(validator(123)).toBe(false)
      expect(validator({})).toBe(false)
      expect(validator([])).toBe(false)
    })
    
    it('组件应该可以多次挂载和卸载', () => {
      const wrapper1 = mount(LoadingSpinner)
      expect(wrapper1.exists()).toBe(true)
      wrapper1.unmount()
      
      const wrapper2 = mount(LoadingSpinner)
      expect(wrapper2.exists()).toBe(true)
      wrapper2.unmount()
    })
    
    it('同时渲染多个不同尺寸的加载指示器', () => {
      const wrapper1 = mount(LoadingSpinner, { props: { size: 'small' } })
      const wrapper2 = mount(LoadingSpinner, { props: { size: 'normal' } })
      
      expect(wrapper1.find('.loading-spinner--small').exists()).toBe(true)
      expect(wrapper2.find('.loading-spinner--normal').exists()).toBe(true)
      
      wrapper1.unmount()
      wrapper2.unmount()
    })
  })
  
  describe('组件结构', () => {
    it('应该有正确的 DOM 结构', () => {
      const wrapper = mount(LoadingSpinner)
      
      // 验证结构：.loading-spinner > .loading-spinner__circle
      const spinner = wrapper.find('.loading-spinner')
      const circle = spinner.find('.loading-spinner__circle')
      
      expect(spinner.exists()).toBe(true)
      expect(circle.exists()).toBe(true)
      expect(spinner.element.children.length).toBe(1)
      expect(spinner.element.children[0]).toBe(circle.element)
    })
    
    it('不应该包含任何文本内容', () => {
      const wrapper = mount(LoadingSpinner)
      
      expect(wrapper.text()).toBe('')
    })
  })
})
