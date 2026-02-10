/**
 * 动画定义文件测试
 * 
 * 验证 animations.css 文件包含所有必需的动画定义
 * 需求：4.1, 4.2
 */

import { describe, it, expect } from '@jest/globals'
import fs from 'fs'
import path from 'path'

describe('animations.css', () => {
  let animationsCSS

  beforeAll(() => {
    const animationsPath = path.resolve(__dirname, '../../../src/assets/styles/animations.css')
    animationsCSS = fs.readFileSync(animationsPath, 'utf-8')
  })

  it('应该存在 animations.css 文件', () => {
    expect(animationsCSS).toBeDefined()
    expect(animationsCSS.length).toBeGreaterThan(0)
  })

  describe('关键帧动画定义', () => {
    it('应该定义 fadeIn 关键帧动画', () => {
      expect(animationsCSS).toMatch(/@keyframes\s+fadeIn/)
      expect(animationsCSS).toMatch(/from\s*{\s*opacity:\s*0/)
      expect(animationsCSS).toMatch(/to\s*{\s*opacity:\s*1/)
    })

    it('应该定义 slideIn 关键帧动画', () => {
      expect(animationsCSS).toMatch(/@keyframes\s+slideIn/)
      expect(animationsCSS).toMatch(/opacity:\s*0/)
      expect(animationsCSS).toMatch(/transform:\s*translateY\(10px\)/)
      expect(animationsCSS).toMatch(/transform:\s*translateY\(0\)/)
    })

    it('应该定义 scaleIn 关键帧动画', () => {
      expect(animationsCSS).toMatch(/@keyframes\s+scaleIn/)
      expect(animationsCSS).toMatch(/transform:\s*scale\(0\.95\)/)
      expect(animationsCSS).toMatch(/transform:\s*scale\(1\)/)
    })

    it('应该定义 spin 加载动画', () => {
      expect(animationsCSS).toMatch(/@keyframes\s+spin/)
      expect(animationsCSS).toMatch(/transform:\s*rotate\(0deg\)/)
      expect(animationsCSS).toMatch(/transform:\s*rotate\(360deg\)/)
    })
  })

  describe('Vue 过渡类定义', () => {
    it('应该定义 fade 过渡类', () => {
      expect(animationsCSS).toMatch(/\.fade-enter-active/)
      expect(animationsCSS).toMatch(/\.fade-leave-active/)
      expect(animationsCSS).toMatch(/\.fade-enter-from/)
      expect(animationsCSS).toMatch(/\.fade-leave-to/)
    })

    it('应该定义 slide 过渡类', () => {
      expect(animationsCSS).toMatch(/\.slide-enter-active/)
      expect(animationsCSS).toMatch(/\.slide-leave-active/)
      expect(animationsCSS).toMatch(/\.slide-enter-from/)
      expect(animationsCSS).toMatch(/\.slide-leave-to/)
    })

    it('应该定义 list 过渡类', () => {
      expect(animationsCSS).toMatch(/\.list-enter-active/)
      expect(animationsCSS).toMatch(/\.list-leave-active/)
      expect(animationsCSS).toMatch(/\.list-enter-from/)
      expect(animationsCSS).toMatch(/\.list-leave-to/)
      expect(animationsCSS).toMatch(/\.list-move/)
    })
  })

  describe('可访问性支持', () => {
    it('应该包含 prefers-reduced-motion 媒体查询', () => {
      expect(animationsCSS).toMatch(/@media\s*\(prefers-reduced-motion:\s*reduce\)/)
    })

    it('prefers-reduced-motion 应该禁用动画', () => {
      const reducedMotionSection = animationsCSS.match(
        /@media\s*\(prefers-reduced-motion:\s*reduce\)\s*{[^}]*}/s
      )
      expect(reducedMotionSection).toBeTruthy()
      expect(reducedMotionSection[0]).toMatch(/animation-duration:\s*0\.01ms/)
      expect(reducedMotionSection[0]).toMatch(/transition-duration:\s*0\.01ms/)
    })
  })

  describe('动画使用 CSS 变量', () => {
    it('过渡效果应该使用 CSS 变量定义时长', () => {
      expect(animationsCSS).toMatch(/var\(--transition-base\)/)
    })
  })
})
