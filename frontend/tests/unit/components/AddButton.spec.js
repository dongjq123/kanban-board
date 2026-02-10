/**
 * AddButton 组件单元测试
 * 
 * 测试范围：
 * - 组件渲染
 * - 按钮点击显示表单
 * - 文本输入和提交
 * - 多行文本输入和提交
 * - 取消操作
 * - 键盘快捷键（Enter、Esc）
 * - 禁用状态
 * - 外部控制表单显示
 * 
 * 需求：1.1, 2.1, 3.2
 */

import { mount } from '@vue/test-utils'
import AddButton from '@/components/AddButton.vue'

describe('AddButton.vue', () => {
  describe('基本渲染', () => {
    it('应该渲染添加按钮', () => {
      const wrapper = mount(AddButton, {
        props: {
          buttonText: '+ 添加测试'
        }
      })
      
      expect(wrapper.find('.btn-add').exists()).toBe(true)
      expect(wrapper.find('.btn-add').text()).toBe('+ 添加测试')
      expect(wrapper.find('.add-form').exists()).toBe(false)
    })
    
    it('应该使用默认按钮文本', () => {
      const wrapper = mount(AddButton)
      
      expect(wrapper.find('.btn-add').text()).toBe('+ 添加')
    })
  })
  
  describe('显示表单', () => {
    it('点击按钮应该显示表单', async () => {
      const wrapper = mount(AddButton)
      
      await wrapper.find('.btn-add').trigger('click')
      
      expect(wrapper.find('.add-form').exists()).toBe(true)
      expect(wrapper.find('.btn-add').exists()).toBe(false)
    })
    
    it('显示表单后应该自动聚焦输入框', async () => {
      const wrapper = mount(AddButton, {
        attachTo: document.body
      })
      
      await wrapper.find('.btn-add').trigger('click')
      await wrapper.vm.$nextTick()
      
      const inputField = wrapper.find('.input-field').element
      expect(document.activeElement).toBe(inputField)
      
      wrapper.unmount()
    })
  })
  
  describe('文本输入类型', () => {
    it('应该渲染文本输入框', async () => {
      const wrapper = mount(AddButton, {
        props: {
          inputType: 'text',
          placeholder: '输入文本...'
        }
      })
      
      await wrapper.find('.btn-add').trigger('click')
      
      expect(wrapper.find('.input-field').exists()).toBe(true)
      expect(wrapper.find('.textarea-field').exists()).toBe(false)
      expect(wrapper.find('.input-field').attributes('placeholder')).toBe('输入文本...')
    })
    
    it('输入文本后应该启用提交按钮', async () => {
      const wrapper = mount(AddButton, {
        props: {
          inputType: 'text'
        }
      })
      
      await wrapper.find('.btn-add').trigger('click')
      
      const submitBtn = wrapper.find('.btn-submit')
      expect(submitBtn.attributes('disabled')).toBeDefined()
      
      const input = wrapper.find('.input-field')
      await input.setValue('测试内容')
      
      expect(submitBtn.attributes('disabled')).toBeUndefined()
    })
    
    it('按 Enter 键应该提交表单', async () => {
      const wrapper = mount(AddButton, {
        props: {
          inputType: 'text'
        }
      })
      
      await wrapper.find('.btn-add').trigger('click')
      
      const input = wrapper.find('.input-field')
      await input.setValue('测试内容')
      await input.trigger('keyup.enter')
      
      expect(wrapper.emitted('submit')).toBeTruthy()
      expect(wrapper.emitted('submit')[0]).toEqual(['测试内容'])
      expect(wrapper.find('.add-form').exists()).toBe(false)
    })
  })
  
  describe('多行文本输入类型', () => {
    it('应该渲染多行文本输入框', async () => {
      const wrapper = mount(AddButton, {
        props: {
          inputType: 'textarea',
          placeholder: '输入多行文本...',
          textareaRows: 5
        }
      })
      
      await wrapper.find('.btn-add').trigger('click')
      
      expect(wrapper.find('.textarea-field').exists()).toBe(true)
      expect(wrapper.find('.input-field').exists()).toBe(false)
      expect(wrapper.find('.textarea-field').attributes('placeholder')).toBe('输入多行文本...')
      expect(wrapper.find('.textarea-field').attributes('rows')).toBe('5')
    })
    
    it('按 Enter 键（不按 Shift）应该提交表单', async () => {
      const wrapper = mount(AddButton, {
        props: {
          inputType: 'textarea'
        }
      })
      
      await wrapper.find('.btn-add').trigger('click')
      
      const textarea = wrapper.find('.textarea-field')
      await textarea.setValue('多行测试内容')
      await textarea.trigger('keyup.enter', { shiftKey: false })
      
      expect(wrapper.emitted('submit')).toBeTruthy()
      expect(wrapper.emitted('submit')[0]).toEqual(['多行测试内容'])
    })
  })
  
  describe('提交操作', () => {
    it('点击提交按钮应该触发 submit 事件', async () => {
      const wrapper = mount(AddButton)
      
      await wrapper.find('.btn-add').trigger('click')
      
      const input = wrapper.find('.input-field')
      await input.setValue('测试内容')
      
      await wrapper.find('.btn-submit').trigger('click')
      
      expect(wrapper.emitted('submit')).toBeTruthy()
      expect(wrapper.emitted('submit')[0]).toEqual(['测试内容'])
    })
    
    it('提交后应该清空输入框并隐藏表单', async () => {
      const wrapper = mount(AddButton)
      
      await wrapper.find('.btn-add').trigger('click')
      
      const input = wrapper.find('.input-field')
      await input.setValue('测试内容')
      await wrapper.find('.btn-submit').trigger('click')
      
      expect(wrapper.find('.add-form').exists()).toBe(false)
      expect(wrapper.find('.btn-add').exists()).toBe(true)
    })
    
    it('应该去除输入内容的首尾空格', async () => {
      const wrapper = mount(AddButton)
      
      await wrapper.find('.btn-add').trigger('click')
      
      const input = wrapper.find('.input-field')
      await input.setValue('  测试内容  ')
      await wrapper.find('.btn-submit').trigger('click')
      
      expect(wrapper.emitted('submit')[0]).toEqual(['测试内容'])
    })
    
    it('空内容或仅空格不应该提交', async () => {
      const wrapper = mount(AddButton)
      
      await wrapper.find('.btn-add').trigger('click')
      
      const input = wrapper.find('.input-field')
      await input.setValue('   ')
      await wrapper.find('.btn-submit').trigger('click')
      
      expect(wrapper.emitted('submit')).toBeFalsy()
      expect(wrapper.find('.add-form').exists()).toBe(true)
    })
  })
  
  describe('取消操作', () => {
    it('点击取消按钮应该隐藏表单', async () => {
      const wrapper = mount(AddButton)
      
      await wrapper.find('.btn-add').trigger('click')
      
      const input = wrapper.find('.input-field')
      await input.setValue('测试内容')
      
      await wrapper.find('.btn-cancel').trigger('click')
      
      expect(wrapper.emitted('cancel')).toBeTruthy()
      expect(wrapper.find('.add-form').exists()).toBe(false)
      expect(wrapper.find('.btn-add').exists()).toBe(true)
    })
    
    it('按 Esc 键应该取消并隐藏表单', async () => {
      const wrapper = mount(AddButton)
      
      await wrapper.find('.btn-add').trigger('click')
      
      const input = wrapper.find('.input-field')
      await input.setValue('测试内容')
      await input.trigger('keyup.esc')
      
      expect(wrapper.emitted('cancel')).toBeTruthy()
      expect(wrapper.find('.add-form').exists()).toBe(false)
    })
    
    it('取消后应该清空输入框', async () => {
      const wrapper = mount(AddButton)
      
      await wrapper.find('.btn-add').trigger('click')
      
      const input = wrapper.find('.input-field')
      await input.setValue('测试内容')
      await wrapper.find('.btn-cancel').trigger('click')
      
      // 重新打开表单，检查输入框是否为空
      await wrapper.find('.btn-add').trigger('click')
      expect(wrapper.find('.input-field').element.value).toBe('')
    })
  })
  
  describe('禁用状态', () => {
    it('禁用时按钮应该不可点击', async () => {
      const wrapper = mount(AddButton, {
        props: {
          disabled: true
        }
      })
      
      const button = wrapper.find('.btn-add')
      expect(button.attributes('disabled')).toBeDefined()
      
      await button.trigger('click')
      expect(wrapper.find('.add-form').exists()).toBe(false)
    })
    
    it('禁用时提交按钮应该不可点击', async () => {
      const wrapper = mount(AddButton, {
        props: {
          disabled: true
        }
      })
      
      // 手动设置 showForm 为 true 以显示表单
      await wrapper.setData({ showForm: true })
      
      const submitBtn = wrapper.find('.btn-submit')
      expect(submitBtn.attributes('disabled')).toBeDefined()
    })
  })
  
  describe('外部控制', () => {
    it('通过 visible 属性控制表单显示', async () => {
      const wrapper = mount(AddButton, {
        props: {
          visible: false
        }
      })
      
      expect(wrapper.find('.add-form').exists()).toBe(false)
      
      await wrapper.setProps({ visible: true })
      
      expect(wrapper.find('.add-form').exists()).toBe(true)
    })
    
    it('外部控制显示时应该自动聚焦', async () => {
      const wrapper = mount(AddButton, {
        props: {
          visible: false
        },
        attachTo: document.body
      })
      
      await wrapper.setProps({ visible: true })
      await wrapper.vm.$nextTick()
      
      const inputField = wrapper.find('.input-field').element
      expect(document.activeElement).toBe(inputField)
      
      wrapper.unmount()
    })
  })
  
  describe('自定义文本', () => {
    it('应该使用自定义提交按钮文本', async () => {
      const wrapper = mount(AddButton, {
        props: {
          submitText: '创建'
        }
      })
      
      await wrapper.find('.btn-add').trigger('click')
      
      expect(wrapper.find('.btn-submit').text()).toBe('创建')
    })
    
    it('应该使用自定义占位符文本', async () => {
      const wrapper = mount(AddButton, {
        props: {
          placeholder: '请输入名称...'
        }
      })
      
      await wrapper.find('.btn-add').trigger('click')
      
      expect(wrapper.find('.input-field').attributes('placeholder')).toBe('请输入名称...')
    })
  })
  
  describe('边缘情况', () => {
    it('快速连续点击提交按钮不应该触发多次 submit 事件', async () => {
      const wrapper = mount(AddButton)
      
      await wrapper.find('.btn-add').trigger('click')
      
      const input = wrapper.find('.input-field')
      await input.setValue('测试内容')
      
      const submitBtn = wrapper.find('.btn-submit')
      await submitBtn.trigger('click')
      await submitBtn.trigger('click')
      await submitBtn.trigger('click')
      
      // 由于第一次提交后表单已隐藏，后续点击不会触发事件
      expect(wrapper.emitted('submit').length).toBe(1)
    })
    
    it('输入类型验证应该只接受 text 或 textarea', () => {
      const validator = AddButton.props.inputType.validator
      
      expect(validator('text')).toBe(true)
      expect(validator('textarea')).toBe(true)
      expect(validator('invalid')).toBe(false)
    })
  })
})
