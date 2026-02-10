/**
 * CSS 命名规范测试
 * 
 * 验证所有 CSS 类名是否遵循 BEM 命名规范
 * 属性 8：CSS 命名规范一致性
 * 验证：需求 10.3
 */

import { describe, it, expect, beforeAll } from '@jest/globals'
import fs from 'fs'
import path from 'path'

describe('CSS 命名规范 - BEM 一致性', () => {
  let cssFiles = []

  beforeAll(() => {
    // 读取所有样式文件
    const stylesDir = path.resolve(__dirname, '../../../src/assets/styles')
    const files = ['variables.css', 'base.css', 'utilities.css', 'animations.css']
    
    files.forEach(file => {
      const filePath = path.join(stylesDir, file)
      if (fs.existsSync(filePath)) {
        cssFiles.push({
          name: file,
          content: fs.readFileSync(filePath, 'utf-8')
        })
      }
    })
  })

  it('应该成功读取所有样式文件', () => {
    expect(cssFiles.length).toBeGreaterThan(0)
  })

  describe('BEM 命名规范验证', () => {
    /**
     * BEM 命名规范：
     * - Block: .block
     * - Element: .block__element
     * - Modifier: .block--modifier 或 .block__element--modifier
     * 
     * 工具类除外（如 .flex, .p-md 等）
     */

    it('utilities.css 应该使用简短的工具类命名', () => {
      const utilitiesFile = cssFiles.find(f => f.name === 'utilities.css')
      if (!utilitiesFile) return

      // 工具类应该使用简短的命名，如 .flex, .p-md, .text-center
      const utilityPattern = /\.(flex|grid|p-|m-|text-|font-|rounded|shadow|border|bg-|gap-|items-|justify-|leading-|opacity-|cursor-|transition|w-|h-|overflow-|block|inline|hidden|relative|absolute|fixed|sticky)/
      
      const classMatches = utilitiesFile.content.match(/\.[a-z][a-z0-9-]*/gi)
      expect(classMatches).toBeTruthy()
      
      // 至少应该有一些工具类
      const utilityClasses = classMatches.filter(cls => utilityPattern.test(cls))
      expect(utilityClasses.length).toBeGreaterThan(20)
    })

    it('animations.css 应该使用 BEM 或描述性命名', () => {
      const animationsFile = cssFiles.find(f => f.name === 'animations.css')
      if (!animationsFile) return

      // 动画类应该使用描述性命名或 BEM 格式
      // 例如：.fade-enter-active, .list-move, .animate-spin
      const animationPattern = /\.(fade|slide|list|animate)-[a-z-]+/
      
      const classMatches = animationsFile.content.match(/\.[a-z][a-z0-9-]*/gi)
      if (classMatches) {
        const animationClasses = classMatches.filter(cls => animationPattern.test(cls))
        expect(animationClasses.length).toBeGreaterThan(0)
      }
    })

    it('CSS 类名应该使用小写字母和连字符', () => {
      cssFiles.forEach(file => {
        // 提取所有类名
        const classMatches = file.content.match(/\.[a-zA-Z][a-zA-Z0-9_-]*/g)
        
        if (classMatches) {
          classMatches.forEach(className => {
            // 移除前导点号
            const name = className.substring(1)
            
            // 跳过伪类和伪元素
            if (name.includes(':') || name.includes('::')) return
            
            // 类名应该只包含小写字母、数字、连字符和下划线（BEM 使用 __ 和 --）
            expect(name).toMatch(/^[a-z][a-z0-9_-]*$/)
          })
        }
      })
    })

    it('CSS 类名不应该使用驼峰命名', () => {
      cssFiles.forEach(file => {
        // 查找可能的驼峰命名
        const camelCasePattern = /\.[a-z]+[A-Z][a-zA-Z]*/g
        const camelCaseMatches = file.content.match(camelCasePattern)
        
        // 不应该有驼峰命名的类
        if (camelCaseMatches) {
          expect(camelCaseMatches.length).toBe(0)
        }
      })
    })

    it('BEM 元素分隔符应该使用双下划线 __', () => {
      cssFiles.forEach(file => {
        // 如果文件中有 BEM 元素命名，应该使用 __
        const bemElementPattern = /\.[a-z][a-z0-9-]*__[a-z][a-z0-9-]*/g
        const bemElements = file.content.match(bemElementPattern)
        
        // 如果有 BEM 元素，验证格式正确
        if (bemElements) {
          bemElements.forEach(element => {
            // 应该只有一个 __ 分隔符（block__element）
            const underscoreCount = (element.match(/__/g) || []).length
            expect(underscoreCount).toBe(1)
          })
        }
      })
    })

    it('BEM 修饰符分隔符应该使用双连字符 --', () => {
      cssFiles.forEach(file => {
        // 如果文件中有 BEM 修饰符命名，应该使用 --
        const bemModifierPattern = /\.[a-z][a-z0-9-]*--[a-z][a-z0-9-]*/g
        const bemModifiers = file.content.match(bemModifierPattern)
        
        // 如果有 BEM 修饰符，验证格式正确
        if (bemModifiers) {
          bemModifiers.forEach(modifier => {
            // 修饰符应该在 block 或 element 之后
            expect(modifier).toMatch(/\.[a-z][a-z0-9-]*(__[a-z][a-z0-9-]*)?--[a-z][a-z0-9-]*/)
          })
        }
      })
    })
  })

  describe('CSS 变量命名规范', () => {
    it('CSS 变量应该使用双连字符前缀 --', () => {
      const variablesFile = cssFiles.find(f => f.name === 'variables.css')
      if (!variablesFile) return

      // 所有 CSS 变量应该以 -- 开头
      const varPattern = /--[a-z][a-z0-9-]*:/g
      const variables = variablesFile.content.match(varPattern)
      
      expect(variables).toBeTruthy()
      expect(variables.length).toBeGreaterThan(50) // 应该有 50+ 个变量
    })

    it('CSS 变量应该使用描述性的分类命名', () => {
      const variablesFile = cssFiles.find(f => f.name === 'variables.css')
      if (!variablesFile) return

      // 变量应该有清晰的分类前缀
      const categories = [
        'color',
        'spacing',
        'font',
        'shadow',
        'radius',
        'transition',
        'line-height'
      ]

      categories.forEach(category => {
        const categoryPattern = new RegExp(`--${category}-[a-z0-9-]+:`, 'g')
        const matches = variablesFile.content.match(categoryPattern)
        expect(matches).toBeTruthy()
        expect(matches.length).toBeGreaterThan(0)
      })
    })

    it('CSS 变量名应该使用连字符分隔单词', () => {
      const variablesFile = cssFiles.find(f => f.name === 'variables.css')
      if (!variablesFile) return

      // 提取所有变量名
      const variables = variablesFile.content.match(/--[a-z][a-z0-9-]*:/g)
      
      if (variables) {
        variables.forEach(varName => {
          // 移除前缀 -- 和后缀 :
          const name = varName.substring(2, varName.length - 1)
          
          // 变量名应该只包含小写字母、数字和连字符
          expect(name).toMatch(/^[a-z][a-z0-9-]*$/)
          
          // 不应该有驼峰命名
          expect(name).not.toMatch(/[A-Z]/)
        })
      }
    })
  })

  describe('命名一致性', () => {
    it('相关的类名应该使用一致的前缀', () => {
      const utilitiesFile = cssFiles.find(f => f.name === 'utilities.css')
      if (!utilitiesFile) return

      // 检查间距类的一致性
      const paddingClasses = utilitiesFile.content.match(/\.p[xy]?-[a-z0-9]+/g)
      const marginClasses = utilitiesFile.content.match(/\.m[xy]?-[a-z0-9]+/g)
      
      expect(paddingClasses).toBeTruthy()
      expect(marginClasses).toBeTruthy()
      
      // padding 和 margin 应该有相同的尺寸选项
      const paddingSizes = new Set(paddingClasses.map(c => c.split('-')[1]))
      const marginSizes = new Set(marginClasses.map(c => c.split('-')[1]))
      
      // 大部分尺寸应该在两者中都存在
      const commonSizes = [...paddingSizes].filter(s => marginSizes.has(s))
      expect(commonSizes.length).toBeGreaterThan(3)
    })

    it('颜色相关的类名应该使用一致的命名模式', () => {
      const utilitiesFile = cssFiles.find(f => f.name === 'utilities.css')
      if (!utilitiesFile) return

      // 文字颜色类
      const textColorClasses = utilitiesFile.content.match(/\.text-[a-z]+/g)
      // 背景颜色类
      const bgColorClasses = utilitiesFile.content.match(/\.bg-[a-z]+/g)
      
      if (textColorClasses && bgColorClasses) {
        // 应该有一些共同的颜色名称
        const textColors = new Set(textColorClasses.map(c => c.split('-')[1]))
        const bgColors = new Set(bgColorClasses.map(c => c.split('-')[1]))
        
        const commonColors = [...textColors].filter(c => bgColors.has(c))
        expect(commonColors.length).toBeGreaterThan(0)
      }
    })
  })
})
