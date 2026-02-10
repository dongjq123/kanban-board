/**
 * Toast 服务单元测试
 * 
 * 测试 Toast 服务的基本功能
 * 
 * 需求：7.2, 7.3
 */

// Mock vue-toastification BEFORE any imports
const mockToastInstance = {
  success: jest.fn(),
  error: jest.fn(),
  warning: jest.fn(),
  info: jest.fn(),
  dismiss: jest.fn(),
  clear: jest.fn()
}

jest.mock('vue-toastification', () => ({
  useToast: jest.fn(() => mockToastInstance)
}))

import toast from '@/services/toast'

describe('Toast Service', () => {
  beforeEach(() => {
    // 清除所有 mock 调用记录
    mockToastInstance.success.mockClear()
    mockToastInstance.error.mockClear()
    mockToastInstance.warning.mockClear()
    mockToastInstance.info.mockClear()
    mockToastInstance.dismiss.mockClear()
    mockToastInstance.clear.mockClear()
  })

  describe('toast.success()', () => {
    it('should call toast instance success method with message', () => {
      toast.success('操作成功')
      
      expect(mockToastInstance.success).toHaveBeenCalledTimes(1)
      expect(mockToastInstance.success).toHaveBeenCalledWith(
        '操作成功',
        expect.objectContaining({
          timeout: 3000,
          closeOnClick: true,
          pauseOnHover: true
        })
      )
    })

    it('should accept custom options', () => {
      toast.success('操作成功', { timeout: 5000 })
      
      expect(mockToastInstance.success).toHaveBeenCalledWith(
        '操作成功',
        expect.objectContaining({
          timeout: 5000,
          closeOnClick: true,
          pauseOnHover: true
        })
      )
    })
  })

  describe('toast.error()', () => {
    it('should call toast instance error method with message', () => {
      toast.error('操作失败')
      
      expect(mockToastInstance.error).toHaveBeenCalledTimes(1)
      expect(mockToastInstance.error).toHaveBeenCalledWith(
        '操作失败',
        expect.objectContaining({
          timeout: 5000, // 错误消息显示更久
          closeOnClick: true,
          pauseOnHover: true
        })
      )
    })

    it('should accept custom options', () => {
      toast.error('操作失败', { timeout: 10000 })
      
      expect(mockToastInstance.error).toHaveBeenCalledWith(
        '操作失败',
        expect.objectContaining({
          timeout: 10000,
          closeOnClick: true,
          pauseOnHover: true
        })
      )
    })
  })

  describe('toast.warning()', () => {
    it('should call toast instance warning method with message', () => {
      toast.warning('请注意')
      
      expect(mockToastInstance.warning).toHaveBeenCalledTimes(1)
      expect(mockToastInstance.warning).toHaveBeenCalledWith(
        '请注意',
        expect.objectContaining({
          timeout: 4000,
          closeOnClick: true,
          pauseOnHover: true
        })
      )
    })

    it('should accept custom options', () => {
      toast.warning('请注意', { timeout: 6000 })
      
      expect(mockToastInstance.warning).toHaveBeenCalledWith(
        '请注意',
        expect.objectContaining({
          timeout: 6000,
          closeOnClick: true,
          pauseOnHover: true
        })
      )
    })
  })

  describe('toast.info()', () => {
    it('should call toast instance info method with message', () => {
      toast.info('提示信息')
      
      expect(mockToastInstance.info).toHaveBeenCalledTimes(1)
      expect(mockToastInstance.info).toHaveBeenCalledWith(
        '提示信息',
        expect.objectContaining({
          timeout: 3000,
          closeOnClick: true,
          pauseOnHover: true
        })
      )
    })

    it('should accept custom options', () => {
      toast.info('提示信息', { timeout: 5000 })
      
      expect(mockToastInstance.info).toHaveBeenCalledWith(
        '提示信息',
        expect.objectContaining({
          timeout: 5000,
          closeOnClick: true,
          pauseOnHover: true
        })
      )
    })
  })

  describe('toast.clear()', () => {
    it('should call toast instance dismiss method with toast ID', () => {
      const toastId = 'test-toast-id'
      toast.clear(toastId)
      
      expect(mockToastInstance.dismiss).toHaveBeenCalledTimes(1)
      expect(mockToastInstance.dismiss).toHaveBeenCalledWith(toastId)
    })
  })

  describe('toast.clearAll()', () => {
    it('should call toast instance clear method', () => {
      toast.clearAll()
      
      expect(mockToastInstance.clear).toHaveBeenCalledTimes(1)
    })
  })

  describe('Default Options', () => {
    it('should use correct default timeout for success messages', () => {
      toast.success('测试')
      
      const call = mockToastInstance.success.mock.calls[0]
      expect(call[1].timeout).toBe(3000)
    })

    it('should use correct default timeout for error messages', () => {
      toast.error('测试')
      
      const call = mockToastInstance.error.mock.calls[0]
      expect(call[1].timeout).toBe(5000)
    })

    it('should use correct default timeout for warning messages', () => {
      toast.warning('测试')
      
      const call = mockToastInstance.warning.mock.calls[0]
      expect(call[1].timeout).toBe(4000)
    })

    it('should use correct default timeout for info messages', () => {
      toast.info('测试')
      
      const call = mockToastInstance.info.mock.calls[0]
      expect(call[1].timeout).toBe(3000)
    })
  })

  describe('Options Merging', () => {
    it('should merge custom options with defaults', () => {
      toast.success('测试', { 
        timeout: 10000,
        closeOnClick: false
      })
      
      const call = mockToastInstance.success.mock.calls[0]
      expect(call[1]).toEqual({
        timeout: 10000,
        closeOnClick: false,
        pauseOnHover: true
      })
    })

    it('should allow overriding all default options', () => {
      toast.error('测试', { 
        timeout: 1000,
        closeOnClick: false,
        pauseOnHover: false
      })
      
      const call = mockToastInstance.error.mock.calls[0]
      expect(call[1]).toEqual({
        timeout: 1000,
        closeOnClick: false,
        pauseOnHover: false
      })
    })
  })
})
