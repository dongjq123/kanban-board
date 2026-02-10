/**
 * Toast 通知服务
 * 
 * 提供统一的 Toast 通知接口，封装 vue-toastification 库
 * 管理 Toast 组件的显示和隐藏
 * 
 * 使用方法：
 * import toast from '@/services/toast'
 * 
 * toast.success('操作成功')
 * toast.error('操作失败')
 * toast.warning('警告信息')
 * toast.info('提示信息')
 * 
 * 需求：7.2, 7.3
 */

import { useToast } from 'vue-toastification'

/**
 * Toast 实例
 * 延迟初始化，确保在 Vue 应用上下文中使用
 */
let toastInstance = null

/**
 * 获取 Toast 实例
 * 
 * 如果实例不存在，则创建新实例
 * 如果在 Vue 上下文外调用，提供 console 后备方案
 * 
 * @returns {Object} Toast 实例
 */
const getToastInstance = () => {
  if (!toastInstance) {
    try {
      toastInstance = useToast()
    } catch (error) {
      // 如果在 Vue 上下文外调用，使用 console 作为后备
      console.warn('Toast not available in current context, falling back to console')
      toastInstance = {
        success: (msg, options) => console.log('✓ SUCCESS:', msg, options),
        error: (msg, options) => console.error('✗ ERROR:', msg, options),
        warning: (msg, options) => console.warn('⚠ WARNING:', msg, options),
        info: (msg, options) => console.info('ℹ INFO:', msg, options),
        clear: () => console.log('Toast cleared'),
        clearAll: () => console.log('All toasts cleared')
      }
    }
  }
  return toastInstance
}

/**
 * Toast 服务对象
 * 
 * 提供统一的接口来显示不同类型的通知
 */
const toast = {
  /**
   * 显示成功通知
   * 
   * @param {string} message - 通知消息
   * @param {Object} options - 可选配置项
   * @param {number} options.timeout - 显示时长（毫秒），默认 3000
   * @param {boolean} options.closeOnClick - 点击关闭，默认 true
   * @param {boolean} options.pauseOnHover - 悬停暂停，默认 true
   * @returns {Object} Toast 实例 ID
   * 
   * @example
   * toast.success('操作成功')
   * toast.success('保存成功', { timeout: 5000 })
   */
  success(message, options = {}) {
    const instance = getToastInstance()
    return instance.success(message, {
      timeout: 3000,
      closeOnClick: true,
      pauseOnHover: true,
      ...options
    })
  },

  /**
   * 显示错误通知
   * 
   * @param {string} message - 错误消息
   * @param {Object} options - 可选配置项
   * @param {number} options.timeout - 显示时长（毫秒），默认 5000（错误消息显示更久）
   * @param {boolean} options.closeOnClick - 点击关闭，默认 true
   * @param {boolean} options.pauseOnHover - 悬停暂停，默认 true
   * @returns {Object} Toast 实例 ID
   * 
   * @example
   * toast.error('操作失败')
   * toast.error('网络连接失败，请重试', { timeout: 10000 })
   */
  error(message, options = {}) {
    const instance = getToastInstance()
    return instance.error(message, {
      timeout: 5000, // 错误消息显示更久
      closeOnClick: true,
      pauseOnHover: true,
      ...options
    })
  },

  /**
   * 显示警告通知
   * 
   * @param {string} message - 警告消息
   * @param {Object} options - 可选配置项
   * @param {number} options.timeout - 显示时长（毫秒），默认 4000
   * @param {boolean} options.closeOnClick - 点击关闭，默认 true
   * @param {boolean} options.pauseOnHover - 悬停暂停，默认 true
   * @returns {Object} Toast 实例 ID
   * 
   * @example
   * toast.warning('请注意')
   * toast.warning('即将超时', { timeout: 6000 })
   */
  warning(message, options = {}) {
    const instance = getToastInstance()
    return instance.warning(message, {
      timeout: 4000,
      closeOnClick: true,
      pauseOnHover: true,
      ...options
    })
  },

  /**
   * 显示信息通知
   * 
   * @param {string} message - 信息消息
   * @param {Object} options - 可选配置项
   * @param {number} options.timeout - 显示时长（毫秒），默认 3000
   * @param {boolean} options.closeOnClick - 点击关闭，默认 true
   * @param {boolean} options.pauseOnHover - 悬停暂停，默认 true
   * @returns {Object} Toast 实例 ID
   * 
   * @example
   * toast.info('提示信息')
   * toast.info('新功能已上线', { timeout: 5000 })
   */
  info(message, options = {}) {
    const instance = getToastInstance()
    return instance.info(message, {
      timeout: 3000,
      closeOnClick: true,
      pauseOnHover: true,
      ...options
    })
  },

  /**
   * 清除指定的 Toast 通知
   * 
   * @param {Object} toastId - Toast 实例 ID（由 success/error/warning/info 返回）
   * 
   * @example
   * const id = toast.info('加载中...')
   * // ... 稍后
   * toast.clear(id)
   */
  clear(toastId) {
    const instance = getToastInstance()
    if (instance.dismiss) {
      instance.dismiss(toastId)
    } else if (instance.clear) {
      instance.clear(toastId)
    }
  },

  /**
   * 清除所有 Toast 通知
   * 
   * @example
   * toast.clearAll()
   */
  clearAll() {
    const instance = getToastInstance()
    if (instance.clear) {
      instance.clear()
    }
  }
}

// 导出 toast 服务
export default toast

// 同时导出 getToastInstance 供高级用户使用
export { getToastInstance }
