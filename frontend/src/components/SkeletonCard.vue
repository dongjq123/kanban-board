<!--
  SkeletonCard 组件
  
  功能：
  - 在数据加载时显示骨架屏占位符
  - 实现 shimmer 动画效果
  - 模拟真实卡片的布局结构
  
  需求：7.4
-->
<template>
  <div class="skeleton-card">
    <div class="skeleton skeleton--title"></div>
    <div class="skeleton skeleton--text"></div>
    <div class="skeleton skeleton--text skeleton--text-short"></div>
  </div>
</template>

<script>
export default {
  name: 'SkeletonCard'
}
</script>

<style scoped>
/**
 * SkeletonCard Component Styles
 * 骨架屏卡片样式
 * 
 * 需求：7.4
 */

/**
 * 骨架卡片容器
 * 模拟真实卡片的样式
 */
.skeleton-card {
  padding: var(--spacing-md);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--radius-base);
  box-shadow: var(--shadow-sm);
}

/**
 * 骨架占位符基础样式
 * 使用渐变背景实现 shimmer 效果
 */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-gray-200) 25%,
    var(--color-gray-100) 50%,
    var(--color-gray-200) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}

/**
 * 标题骨架
 * 模拟卡片标题的高度和宽度
 */
.skeleton--title {
  height: 20px;
  width: 70%;
  margin-bottom: var(--spacing-sm);
}

/**
 * 文本骨架
 * 模拟卡片描述文本
 */
.skeleton--text {
  height: 14px;
  width: 100%;
  margin-bottom: var(--spacing-xs);
}

/**
 * 短文本骨架
 * 模拟较短的文本行
 */
.skeleton--text-short {
  width: 60%;
  margin-bottom: 0;
}

/**
 * Shimmer 动画
 * 创建从左到右的闪烁效果
 * 
 * 需求：7.4
 */
@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/**
 * 响应式设计 - 移动端媒体查询
 * 需求：5.1, 5.2
 */
@media (max-width: 767px) {
  .skeleton-card {
    padding: var(--spacing-sm);
  }
  
  .skeleton--title {
    height: 16px;
    margin-bottom: var(--spacing-xs);
  }
  
  .skeleton--text {
    height: 12px;
  }
}

/**
 * 响应式设计 - 平板端媒体查询
 * 需求：5.1
 */
@media (min-width: 768px) and (max-width: 1023px) {
  .skeleton-card {
    padding: var(--spacing-sm) var(--spacing-md);
  }
}

/**
 * 响应式设计 - 桌面端媒体查询
 * 需求：5.1 - 桌面设备适配
 */
@media (min-width: 1024px) {
  .skeleton-card {
    padding: var(--spacing-md);
  }
  
  .skeleton--title {
    height: 20px;
    margin-bottom: var(--spacing-sm);
  }
  
  .skeleton--text {
    height: 14px;
    margin-bottom: var(--spacing-xs);
  }
}

/**
 * 响应式设计 - 大屏媒体查询
 * 需求：5.1 - 大屏设备适配
 */
@media (min-width: 1440px) {
  .skeleton-card {
    padding: var(--spacing-lg);
  }
  
  .skeleton--title {
    height: 24px;
    width: 75%;
    margin-bottom: var(--spacing-md);
  }
  
  .skeleton--text {
    height: 16px;
    margin-bottom: var(--spacing-sm);
  }
  
  .skeleton--text-short {
    width: 65%;
  }
}
</style>
