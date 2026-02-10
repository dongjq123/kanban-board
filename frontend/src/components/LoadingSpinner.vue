<!--
  LoadingSpinner 组件
  
  一个可复用的加载旋转动画组件，支持不同尺寸。
  
  Props:
  - size: 'small' | 'normal' (默认: 'normal')
    控制加载指示器的尺寸
  
  使用示例:
  <LoadingSpinner />
  <LoadingSpinner size="small" />
  
  需求：7.1, 7.4
-->

<template>
  <div class="loading-spinner" :class="spinnerSizeClass">
    <div class="loading-spinner__circle"></div>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  
  props: {
    /**
     * 加载指示器的尺寸
     * @type {'small' | 'normal'}
     * @default 'normal'
     */
    size: {
      type: String,
      default: 'normal',
      validator: (value) => ['small', 'normal'].includes(value)
    }
  },
  
  computed: {
    /**
     * 根据 size prop 返回对应的 CSS 类名
     */
    spinnerSizeClass() {
      return `loading-spinner--${this.size}`
    }
  }
}
</script>

<style scoped>
/**
 * LoadingSpinner 组件样式
 * 
 * 实现旋转加载动画，支持两种尺寸：
 * - normal: 40px × 40px (默认)
 * - small: 20px × 20px
 * 
 * 使用 CSS 变量定义颜色，确保与设计系统一致
 * 需求：7.1, 7.4
 */

.loading-spinner {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.loading-spinner--small {
  width: 20px;
  height: 20px;
}

.loading-spinner__circle {
  width: 100%;
  height: 100%;
  border: 3px solid var(--color-gray-200);
  border-top-color: var(--color-primary);
  border-radius: var(--radius-full);
  animation: spin 0.8s linear infinite;
}

.loading-spinner--small .loading-spinner__circle {
  border-width: 2px;
}

/**
 * 可访问性支持
 * 为偏好减少动画的用户提供支持
 */
@media (prefers-reduced-motion: reduce) {
  .loading-spinner__circle {
    animation-duration: 2s;
  }
}
</style>
