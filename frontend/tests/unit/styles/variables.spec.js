/**
 * CSS 变量定义测试
 * 
 * 验证 variables.css 文件包含所有必需的 CSS 变量（设计令牌）
 * 需求：1.1, 1.5, 10.1
 */

import { describe, it, expect, beforeAll } from '@jest/globals'
import fs from 'fs'
import path from 'path'

describe('variables.css - CSS 变量定义', () => {
  let variablesCSS

  beforeAll(() => {
    const variablesPath = path.resolve(__dirname, '../../../src/assets/styles/variables.css')
    variablesCSS = fs.readFileSync(variablesPath, 'utf-8')
  })

  it('应该存在 variables.css 文件', () => {
    expect(variablesCSS).toBeDefined()
    expect(variablesCSS.length).toBeGreaterThan(0)
  })

  describe('颜色系统', () => {
    it('应该定义主色调变量', () => {
      expect(variablesCSS).toMatch(/--color-primary:\s*#[0-9a-fA-F]{6}/)
      expect(variablesCSS).toMatch(/--color-primary-light:\s*#[0-9a-fA-F]{6}/)
      expect(variablesCSS).toMatch(/--color-primary-dark:\s*#[0-9a-fA-F]{6}/)
    })

    it('应该定义辅助色变量', () => {
      expect(variablesCSS).toMatch(/--color-secondary:\s*#[0-9a-fA-F]{6}/)
      expect(variablesCSS).toMatch(/--color-accent:\s*#[0-9a-fA-F]{6}/)
    })

    it('应该定义中性色变量（灰度）', () => {
      const grayLevels = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
      grayLevels.forEach(level => {
        expect(variablesCSS).toMatch(new RegExp(`--color-gray-${level}:\\s*#[0-9a-fA-F]{6}`))
      })
    })

    it('应该定义语义化颜色变量', () => {
      expect(variablesCSS).toMatch(/--color-success:\s*#[0-9a-fA-F]{6}/)
      expect(variablesCSS).toMatch(/--color-warning:\s*#[0-9a-fA-F]{6}/)
      expect(variablesCSS).toMatch(/--color-error:\s*#[0-9a-fA-F]{6}/)
      expect(variablesCSS).toMatch(/--color-info:\s*#[0-9a-fA-F]{6}/)
    })

    it('应该定义背景色变量', () => {
      expect(variablesCSS).toMatch(/--color-bg-primary:\s*#[0-9a-fA-F]{6}/)
      expect(variablesCSS).toMatch(/--color-bg-secondary:\s*#[0-9a-fA-F]{6}/)
      expect(variablesCSS).toMatch(/--color-bg-tertiary:\s*#[0-9a-fA-F]{6}/)
    })

    it('应该定义文字颜色变量', () => {
      expect(variablesCSS).toMatch(/--color-text-primary:\s*#[0-9a-fA-F]{6}/)
      expect(variablesCSS).toMatch(/--color-text-secondary:\s*#[0-9a-fA-F]{6}/)
      expect(variablesCSS).toMatch(/--color-text-tertiary:\s*#[0-9a-fA-F]{6}/)
    })
  })

  describe('间距系统', () => {
    it('应该定义所有间距变量', () => {
      const spacings = ['xs', 'sm', 'md', 'lg', 'xl', '2xl', '3xl']
      spacings.forEach(size => {
        expect(variablesCSS).toMatch(new RegExp(`--spacing-${size}:\\s*\\d+px`))
      })
    })

    it('间距值应该符合 4px 基准', () => {
      const spacingMatches = variablesCSS.match(/--spacing-\w+:\s*(\d+)px/g)
      expect(spacingMatches).toBeTruthy()
      
      spacingMatches.forEach(match => {
        const value = parseInt(match.match(/(\d+)px/)[1])
        expect(value % 4).toBe(0) // 应该是 4 的倍数
      })
    })
  })

  describe('字体系统', () => {
    it('应该定义字体族变量', () => {
      expect(variablesCSS).toMatch(/--font-family-base:/)
      expect(variablesCSS).toMatch(/--font-family-mono:/)
    })

    it('应该定义字体大小变量', () => {
      const fontSizes = ['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl']
      fontSizes.forEach(size => {
        expect(variablesCSS).toMatch(new RegExp(`--font-size-${size}:`))
      })
    })

    it('应该定义字重变量', () => {
      expect(variablesCSS).toMatch(/--font-weight-normal:\s*\d+/)
      expect(variablesCSS).toMatch(/--font-weight-medium:\s*\d+/)
      expect(variablesCSS).toMatch(/--font-weight-semibold:\s*\d+/)
      expect(variablesCSS).toMatch(/--font-weight-bold:\s*\d+/)
    })

    it('应该定义行高变量', () => {
      expect(variablesCSS).toMatch(/--line-height-tight:\s*[\d.]+/)
      expect(variablesCSS).toMatch(/--line-height-normal:\s*[\d.]+/)
      expect(variablesCSS).toMatch(/--line-height-relaxed:\s*[\d.]+/)
    })
  })

  describe('阴影系统', () => {
    it('应该定义所有阴影变量', () => {
      const shadows = ['sm', 'base', 'md', 'lg', 'xl']
      shadows.forEach(size => {
        expect(variablesCSS).toMatch(new RegExp(`--shadow-${size}:`))
      })
    })

    it('阴影值应该包含 rgba 颜色', () => {
      const shadowMatches = variablesCSS.match(/--shadow-\w+:[^;]+;/g)
      expect(shadowMatches).toBeTruthy()
      
      shadowMatches.forEach(match => {
        expect(match).toMatch(/rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)/)
      })
    })
  })

  describe('圆角系统', () => {
    it('应该定义所有圆角变量', () => {
      const radii = ['sm', 'base', 'md', 'lg', 'full']
      radii.forEach(size => {
        expect(variablesCSS).toMatch(new RegExp(`--radius-${size}:`))
      })
    })
  })

  describe('过渡动画时长', () => {
    it('应该定义所有过渡时长变量', () => {
      expect(variablesCSS).toMatch(/--transition-fast:\s*\d+ms/)
      expect(variablesCSS).toMatch(/--transition-base:\s*\d+ms/)
      expect(variablesCSS).toMatch(/--transition-slow:\s*\d+ms/)
    })

    it('过渡时长应该包含缓动函数', () => {
      expect(variablesCSS).toMatch(/--transition-fast:.*ease/)
      expect(variablesCSS).toMatch(/--transition-base:.*ease/)
      expect(variablesCSS).toMatch(/--transition-slow:.*ease/)
    })
  })

  describe('CSS 变量格式', () => {
    it('所有 CSS 变量应该在 :root 选择器中定义', () => {
      expect(variablesCSS).toMatch(/:root\s*{/)
    })

    it('颜色值应该使用正确的十六进制格式', () => {
      const colorMatches = variablesCSS.match(/--color-[^:]+:\s*#[0-9a-fA-F]{6}/g)
      expect(colorMatches).toBeTruthy()
      expect(colorMatches.length).toBeGreaterThan(20) // 至少应该有 20+ 个颜色变量
    })
  })
})
