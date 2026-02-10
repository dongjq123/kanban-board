/**
 * Toast 组件单元测试
 * 
 * 测试范围：
 * - 组件渲染
 * - 四种类型（success, warning, error, info）
 * - 图标显示
 * - 标题和消息显示
 * - 关闭按钮功能
 * - 自动关闭逻辑
 * - 滑入滑出动画
 * - Props 验证
 * 
 * 需求：7.2, 7.3, 7.5
 */

import { mount } from '@vue/test-utils'
import Toast from '@/components/Toast.vue'

describe('Toast.vue', () => {
  // 使用 fake timers 来测试自动关闭功能
  beforeEach(() => {
    jest.useFakeTimers()
  })

  afterEach(() => {
    jest.clearAllTimers()
    jest.useRealTimers()
  })

  describe('基本渲染', () => {
    it('应该渲染 Toast 组件', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test Title'
        }
      })
      
      expect(wrapper.find('.toast').exists()).toBe(true)
    })

    it('应该显示标题', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test Title'
        }
      })
      
      expect(wrapper.find('.toast__title').text()).toBe('Test Title')
    })

    it('应该显示消息（如果提供）', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test Title',
          message: 'Test Message'
        }
      })
      
      expect(wrapper.find('.toast__message').text()).toBe('Test Message')
    })

    it('没有消息时不应该显示消息元素', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test Title'
        }
      })
      
      expect(wrapper.find('.toast__message').exists()).toBe(false)
    })

    it('应该显示关闭按钮', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test Title'
        }
      })
      
      expect(wrapper.find('.toast__close').exists()).toBe(true)
    })
  })

  describe('Toast 类型', () => {
    it('默认应该是 info 类型', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test Title'
        }
      })
      
      expect(wrapper.find('.toast--info').exists()).toBe(true)
    })

    it('应该支持 success 类型', () => {
      const wrapper = mount(Toast, {
        props: {
          type: 'success',
          title: 'Success'
        }
      })
      
      expect(wrapper.find('.toast--success').exists()).toBe(true)
    })

    it('应该支持 warning 类型', () => {
      const wrapper = mount(Toast, {
        props: {
          type: 'warning',
          title: 'Warning'
        }
      })
      
      expect(wrapper.find('.toast--warning').exists()).toBe(true)
    })

    it('应该支持 error 类型', () => {
      const wrapper = mount(Toast, {
        props: {
          type: 'error',
          title: 'Error'
        }
      })
      
      expect(wrapper.find('.toast--error').exists()).toBe(true)
    })

    it('应该支持 info 类型', () => {
      const wrapper = mount(Toast, {
        props: {
          type: 'info',
          title: 'Info'
        }
      })
      
      expect(wrapper.find('.toast--info').exists()).toBe(true)
    })
  })

  describe('图标显示', () => {
    it('success 类型应该显示 check_circle 图标', async () => {
      const wrapper = mount(Toast, {
        props: {
          type: 'success',
          title: 'Success'
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.iconName).toBe('check_circle')
    })

    it('warning 类型应该显示 warning 图标', async () => {
      const wrapper = mount(Toast, {
        props: {
          type: 'warning',
          title: 'Warning'
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.iconName).toBe('warning')
    })

    it('error 类型应该显示 error 图标', async () => {
      const wrapper = mount(Toast, {
        props: {
          type: 'error',
          title: 'Error'
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.iconName).toBe('error')
    })

    it('info 类型应该显示 info 图标', async () => {
      const wrapper = mount(Toast, {
        props: {
          type: 'info',
          title: 'Info'
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.iconName).toBe('info')
    })

    it('应该渲染图标元素', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test'
        }
      })
      
      expect(wrapper.find('.toast__icon').exists()).toBe(true)
      expect(wrapper.find('.toast__icon .material-icons').exists()).toBe(true)
    })
  })

  describe('关闭功能', () => {
    it('点击关闭按钮应该隐藏 Toast', async () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test',
          autoClose: false
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.visible).toBe(true)
      
      await wrapper.find('.toast__close').trigger('click')
      expect(wrapper.vm.visible).toBe(false)
    })

    it('关闭时应该触发 close 事件', async () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test',
          autoClose: false
        }
      })
      
      await wrapper.vm.$nextTick()
      await wrapper.find('.toast__close').trigger('click')
      
      // Wait for the animation delay
      jest.advanceTimersByTime(250)
      
      expect(wrapper.emitted('close')).toBeTruthy()
    })

    it('关闭按钮应该有 aria-label', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test'
        }
      })
      
      const closeButton = wrapper.find('.toast__close')
      expect(closeButton.attributes('aria-label')).toBe('Close notification')
    })
  })

  describe('自动关闭功能', () => {
    it('默认应该在 3 秒后自动关闭', async () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test'
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.visible).toBe(true)
      
      // Fast-forward time by 3000ms
      jest.advanceTimersByTime(3000)
      
      expect(wrapper.vm.visible).toBe(false)
    })

    it('应该支持自定义关闭时长', async () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test',
          duration: 5000
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.visible).toBe(true)
      
      // After 3 seconds, should still be visible
      jest.advanceTimersByTime(3000)
      expect(wrapper.vm.visible).toBe(true)
      
      // After 5 seconds, should be hidden
      jest.advanceTimersByTime(2000)
      expect(wrapper.vm.visible).toBe(false)
    })

    it('autoClose 为 false 时不应该自动关闭', async () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test',
          autoClose: false
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.visible).toBe(true)
      
      // Even after a long time, should still be visible
      jest.advanceTimersByTime(10000)
      expect(wrapper.vm.visible).toBe(true)
    })

    it('组件卸载时应该清除定时器', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test'
        }
      })
      
      const clearTimeoutSpy = jest.spyOn(global, 'clearTimeout')
      wrapper.unmount()
      
      expect(clearTimeoutSpy).toHaveBeenCalled()
      clearTimeoutSpy.mockRestore()
    })
  })

  describe('Props 验证', () => {
    it('type 属性应该只接受有效的类型', () => {
      const validator = Toast.props.type.validator
      
      expect(validator('success')).toBe(true)
      expect(validator('warning')).toBe(true)
      expect(validator('error')).toBe(true)
      expect(validator('info')).toBe(true)
      expect(validator('invalid')).toBe(false)
      expect(validator('')).toBe(false)
    })

    it('type 属性默认值应该是 info', () => {
      expect(Toast.props.type.default).toBe('info')
    })

    it('title 属性应该是必需的', () => {
      expect(Toast.props.title.required).toBe(true)
    })

    it('message 属性应该有默认值', () => {
      expect(Toast.props.message.default).toBe('')
    })

    it('duration 属性默认值应该是 3000', () => {
      expect(Toast.props.duration.default).toBe(3000)
    })

    it('autoClose 属性默认值应该是 true', () => {
      expect(Toast.props.autoClose.default).toBe(true)
    })
  })

  describe('CSS 类名', () => {
    it('应该始终包含基础类名', async () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test'
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.find('.toast').exists()).toBe(true)
    })

    it('应该根据 type prop 添加对应的修饰类', () => {
      const types = ['success', 'warning', 'error', 'info']
      
      types.forEach(type => {
        const wrapper = mount(Toast, {
          props: {
            type,
            title: 'Test'
          }
        })
        
        expect(wrapper.find(`.toast--${type}`).exists()).toBe(true)
      })
    })

    it('应该包含所有必需的子元素类名', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test',
          message: 'Message'
        }
      })
      
      expect(wrapper.find('.toast__icon').exists()).toBe(true)
      expect(wrapper.find('.toast__content').exists()).toBe(true)
      expect(wrapper.find('.toast__title').exists()).toBe(true)
      expect(wrapper.find('.toast__message').exists()).toBe(true)
      expect(wrapper.find('.toast__close').exists()).toBe(true)
    })
  })

  describe('可访问性', () => {
    it('Toast 应该有 role="alert" 属性', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test'
        }
      })
      
      expect(wrapper.find('.toast').attributes('role')).toBe('alert')
    })

    it('关闭按钮应该有 aria-label', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test'
        }
      })
      
      const closeButton = wrapper.find('.toast__close')
      expect(closeButton.attributes('aria-label')).toBeDefined()
    })
  })

  describe('动画和过渡', () => {
    it('应该使用 transition 组件包裹', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test'
        }
      })
      
      // Check if transition is applied
      expect(wrapper.findComponent({ name: 'Transition' }).exists()).toBe(true)
    })

    it('挂载后应该显示 Toast', async () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test',
          autoClose: false
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.visible).toBe(true)
    })
  })

  describe('边缘情况', () => {
    it('应该处理空消息', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test',
          message: ''
        }
      })
      
      expect(wrapper.find('.toast__message').exists()).toBe(false)
    })

    it('应该处理长标题', () => {
      const longTitle = 'This is a very long title that should still be displayed correctly'
      const wrapper = mount(Toast, {
        props: {
          title: longTitle
        }
      })
      
      expect(wrapper.find('.toast__title').text()).toBe(longTitle)
    })

    it('应该处理长消息', () => {
      const longMessage = 'This is a very long message that should wrap properly and still be displayed correctly in the toast notification'
      const wrapper = mount(Toast, {
        props: {
          title: 'Test',
          message: longMessage
        }
      })
      
      expect(wrapper.find('.toast__message').text()).toBe(longMessage)
    })

    it('组件应该可以多次挂载和卸载', () => {
      const wrapper1 = mount(Toast, { props: { title: 'Test 1' } })
      expect(wrapper1.exists()).toBe(true)
      wrapper1.unmount()
      
      const wrapper2 = mount(Toast, { props: { title: 'Test 2' } })
      expect(wrapper2.exists()).toBe(true)
      wrapper2.unmount()
    })

    it('同时渲染多个不同类型的 Toast', () => {
      const wrapper1 = mount(Toast, { props: { type: 'success', title: 'Success' } })
      const wrapper2 = mount(Toast, { props: { type: 'error', title: 'Error' } })
      
      expect(wrapper1.find('.toast--success').exists()).toBe(true)
      expect(wrapper2.find('.toast--error').exists()).toBe(true)
      
      wrapper1.unmount()
      wrapper2.unmount()
    })

    it('duration 为 0 时应该立即关闭', async () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test',
          duration: 0
        }
      })
      
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.visible).toBe(true)
      
      jest.advanceTimersByTime(0)
      expect(wrapper.vm.visible).toBe(false)
    })
  })

  describe('组件结构', () => {
    it('应该有正确的 DOM 结构', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test',
          message: 'Message'
        }
      })
      
      const toast = wrapper.find('.toast')
      expect(toast.exists()).toBe(true)
      
      // 验证子元素存在
      expect(toast.find('.toast__icon').exists()).toBe(true)
      expect(toast.find('.toast__content').exists()).toBe(true)
      expect(toast.find('.toast__close').exists()).toBe(true)
      
      // 验证内容结构
      const content = toast.find('.toast__content')
      expect(content.find('.toast__title').exists()).toBe(true)
      expect(content.find('.toast__message').exists()).toBe(true)
    })

    it('图标元素应该包含 Material Icons', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test'
        }
      })
      
      const icon = wrapper.find('.toast__icon .material-icons')
      expect(icon.exists()).toBe(true)
    })

    it('关闭按钮应该包含 Material Icons', () => {
      const wrapper = mount(Toast, {
        props: {
          title: 'Test'
        }
      })
      
      const closeIcon = wrapper.find('.toast__close .material-icons')
      expect(closeIcon.exists()).toBe(true)
      expect(closeIcon.text()).toBe('close')
    })
  })
})
