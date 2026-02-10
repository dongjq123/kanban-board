/**
 * Input 样式类测试
 * 
 * 验证 utilities.css 文件包含所有必需的输入框样式类
 * 需求：1.2, 3.2, 4.1
 */

import { describe, it, expect, beforeAll } from '@jest/globals'
import fs from 'fs'
import path from 'path'

describe('utilities.css - Input 样式类', () => {
  let utilitiesCSS

  beforeAll(() => {
    const utilitiesPath = path.resolve(__dirname, '../../../src/assets/styles/utilities.css')
    utilitiesCSS = fs.readFileSync(utilitiesPath, 'utf-8')
  })

  it('应该存在 utilities.css 文件', () => {
    expect(utilitiesCSS).toBeDefined()
    expect(utilitiesCSS.length).toBeGreaterThan(0)
  })

  describe('基础 Input 样式类', () => {
    it('应该定义 .input 基础样式类', () => {
      expect(utilitiesCSS).toMatch(/\.input\s*{/)
    })

    it('.input 应该使用 CSS 变量定义颜色', () => {
      const inputSection = extractInputSection(utilitiesCSS)
      expect(inputSection).toMatch(/var\(--color-text-primary\)/)
      expect(inputSection).toMatch(/var\(--color-bg-primary\)/)
      expect(inputSection).toMatch(/var\(--color-gray-\d+\)/)
    })

    it('.input 应该使用 CSS 变量定义间距', () => {
      const inputSection = extractInputSection(utilitiesCSS)
      expect(inputSection).toMatch(/var\(--spacing-\w+\)/)
    })

    it('.input 应该使用 CSS 变量定义圆角', () => {
      const inputSection = extractInputSection(utilitiesCSS)
      expect(inputSection).toMatch(/var\(--radius-\w+\)/)
    })

    it('.input 应该使用 CSS 变量定义过渡动画', () => {
      const inputSection = extractInputSection(utilitiesCSS)
      expect(inputSection).toMatch(/var\(--transition-\w+\)/)
    })
  })

  describe('Input Hover 状态', () => {
    it('应该定义 .input:hover 样式', () => {
      expect(utilitiesCSS).toMatch(/\.input:hover:not\(:disabled\)/)
    })

    it('.input:hover 应该改变边框颜色', () => {
      const hoverMatch = utilitiesCSS.match(/\.input:hover:not\(:disabled\)\s*{[^}]+}/s)
      expect(hoverMatch).toBeTruthy()
      expect(hoverMatch[0]).toMatch(/border-color/)
    })
  })

  describe('Input Focus 状态', () => {
    it('应该定义 .input:focus 样式', () => {
      expect(utilitiesCSS).toMatch(/\.input:focus\s*{/)
    })

    it('.input:focus 应该移除默认 outline', () => {
      const focusMatch = utilitiesCSS.match(/\.input:focus\s*{[^}]+}/s)
      expect(focusMatch).toBeTruthy()
      expect(focusMatch[0]).toMatch(/outline:\s*none/)
    })

    it('.input:focus 应该有清晰的焦点轮廓（border-color 或 box-shadow）', () => {
      const focusMatch = utilitiesCSS.match(/\.input:focus\s*{[^}]+}/s)
      expect(focusMatch).toBeTruthy()
      const focusStyles = focusMatch[0]
      
      // 应该有 border-color 变化或 box-shadow
      const hasBorderColor = focusStyles.match(/border-color/)
      const hasBoxShadow = focusStyles.match(/box-shadow/)
      
      expect(hasBorderColor || hasBoxShadow).toBeTruthy()
    })

    it('.input:focus 的焦点样式应该使用主色调', () => {
      const focusMatch = utilitiesCSS.match(/\.input:focus\s*{[^}]+}/s)
      expect(focusMatch).toBeTruthy()
      expect(focusMatch[0]).toMatch(/var\(--color-primary\)/)
    })
  })

  describe('Input Disabled 状态', () => {
    it('应该定义 .input:disabled 样式', () => {
      expect(utilitiesCSS).toMatch(/\.input:disabled\s*{/)
    })

    it('.input:disabled 应该改变背景色', () => {
      const disabledMatch = utilitiesCSS.match(/\.input:disabled\s*{[^}]+}/s)
      expect(disabledMatch).toBeTruthy()
      expect(disabledMatch[0]).toMatch(/background-color/)
    })

    it('.input:disabled 应该设置 cursor: not-allowed', () => {
      const disabledMatch = utilitiesCSS.match(/\.input:disabled\s*{[^}]+}/s)
      expect(disabledMatch).toBeTruthy()
      expect(disabledMatch[0]).toMatch(/cursor:\s*not-allowed/)
    })

    it('.input:disabled 应该降低透明度', () => {
      const disabledMatch = utilitiesCSS.match(/\.input:disabled\s*{[^}]+}/s)
      expect(disabledMatch).toBeTruthy()
      expect(disabledMatch[0]).toMatch(/opacity:\s*[\d.]+/)
    })
  })

  describe('Input Placeholder 样式', () => {
    it('应该定义 .input::placeholder 样式', () => {
      expect(utilitiesCSS).toMatch(/\.input::placeholder\s*{/)
    })

    it('.input::placeholder 应该使用较浅的文字颜色', () => {
      const placeholderMatch = utilitiesCSS.match(/\.input::placeholder\s*{[^}]+}/s)
      expect(placeholderMatch).toBeTruthy()
      expect(placeholderMatch[0]).toMatch(/color:\s*var\(--color-text-tertiary\)/)
    })
  })

  describe('Textarea 样式', () => {
    it('应该定义 .textarea 样式类', () => {
      expect(utilitiesCSS).toMatch(/\.textarea\s*{/)
    })

    it('.textarea 应该有 min-height 属性', () => {
      const textareaMatch = utilitiesCSS.match(/\.textarea\s*{[^}]+}/s)
      expect(textareaMatch).toBeTruthy()
      expect(textareaMatch[0]).toMatch(/min-height/)
    })

    it('.textarea 应该有 resize 属性', () => {
      const textareaMatch = utilitiesCSS.match(/\.textarea\s*{[^}]+}/s)
      expect(textareaMatch).toBeTruthy()
      expect(textareaMatch[0]).toMatch(/resize/)
    })

    it('.textarea 应该定义 hover 状态', () => {
      expect(utilitiesCSS).toMatch(/\.textarea:hover:not\(:disabled\)/)
    })

    it('.textarea 应该定义 focus 状态', () => {
      expect(utilitiesCSS).toMatch(/\.textarea:focus/)
    })

    it('.textarea 应该定义 disabled 状态', () => {
      expect(utilitiesCSS).toMatch(/\.textarea:disabled/)
    })
  })

  describe('Input 尺寸变体', () => {
    it('应该定义 .input--sm 小尺寸变体', () => {
      expect(utilitiesCSS).toMatch(/\.input--sm\s*{/)
    })

    it('应该定义 .input--lg 大尺寸变体', () => {
      expect(utilitiesCSS).toMatch(/\.input--lg\s*{/)
    })
  })

  describe('Input 状态变体', () => {
    it('应该定义 .input--error 错误状态', () => {
      expect(utilitiesCSS).toMatch(/\.input--error\s*{/)
    })

    it('应该定义 .input--success 成功状态', () => {
      expect(utilitiesCSS).toMatch(/\.input--success\s*{/)
    })

    it('应该定义 .input--warning 警告状态', () => {
      expect(utilitiesCSS).toMatch(/\.input--warning\s*{/)
    })

    it('.input--error:focus 应该使用错误颜色', () => {
      const errorFocusMatch = utilitiesCSS.match(/\.input--error:focus\s*{[^}]+}/s)
      expect(errorFocusMatch).toBeTruthy()
      expect(errorFocusMatch[0]).toMatch(/var\(--color-error\)/)
    })

    it('.input--success:focus 应该使用成功颜色', () => {
      const successFocusMatch = utilitiesCSS.match(/\.input--success:focus\s*{[^}]+}/s)
      expect(successFocusMatch).toBeTruthy()
      expect(successFocusMatch[0]).toMatch(/var\(--color-success\)/)
    })

    it('.input--warning:focus 应该使用警告颜色', () => {
      const warningFocusMatch = utilitiesCSS.match(/\.input--warning:focus\s*{[^}]+}/s)
      expect(warningFocusMatch).toBeTruthy()
      expect(warningFocusMatch[0]).toMatch(/var\(--color-warning\)/)
    })
  })

  describe('样式一致性', () => {
    it('所有输入框样式应该使用 box-sizing: border-box', () => {
      const inputMatch = utilitiesCSS.match(/\.input\s*{[^}]+}/s)
      const textareaMatch = utilitiesCSS.match(/\.textarea\s*{[^}]+}/s)
      
      expect(inputMatch[0]).toMatch(/box-sizing:\s*border-box/)
      expect(textareaMatch[0]).toMatch(/box-sizing:\s*border-box/)
    })

    it('所有输入框样式应该使用相同的字体系统', () => {
      const inputMatch = utilitiesCSS.match(/\.input\s*{[^}]+}/s)
      const textareaMatch = utilitiesCSS.match(/\.textarea\s*{[^}]+}/s)
      
      expect(inputMatch[0]).toMatch(/font-family:\s*var\(--font-family-base\)/)
      expect(textareaMatch[0]).toMatch(/font-family:\s*var\(--font-family-base\)/)
    })

    it('所有输入框样式应该使用相同的过渡动画', () => {
      const inputMatch = utilitiesCSS.match(/\.input\s*{[^}]+}/s)
      const textareaMatch = utilitiesCSS.match(/\.textarea\s*{[^}]+}/s)
      
      expect(inputMatch[0]).toMatch(/transition:.*var\(--transition-\w+\)/)
      expect(textareaMatch[0]).toMatch(/transition:.*var\(--transition-\w+\)/)
    })
  })
})

/**
 * 辅助函数：提取 Input 相关的 CSS 部分
 */
function extractInputSection(css) {
  // 查找输入框样式类部分，从注释开始到文件末尾或下一个大的注释块
  const inputSectionMatch = css.match(/\/\*[^*]*输入框样式类[^*]*\*\/[\s\S]*$/i)
  return inputSectionMatch ? inputSectionMatch[0] : ''
}
