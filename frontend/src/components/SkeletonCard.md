# SkeletonCard 组件文档

## 概述

SkeletonCard 是一个骨架屏组件，用于在数据加载时显示占位符，提供更好的用户体验。它模拟真实卡片的布局结构，并通过 shimmer 动画效果提供视觉反馈。

## 功能特性

- ✅ 模拟真实卡片的布局结构
- ✅ 实现 shimmer 闪烁动画效果
- ✅ 使用 CSS 变量保持样式一致性
- ✅ 轻量级，无需任何 props
- ✅ 可以同时渲染多个实例

## 使用方法

### 基本用法

```vue
<template>
  <div>
    <!-- 数据加载时显示骨架屏 -->
    <SkeletonCard v-if="loading" />
    
    <!-- 数据加载完成后显示真实卡片 -->
    <Card v-else :card="cardData" />
  </div>
</template>

<script>
import SkeletonCard from '@/components/SkeletonCard.vue'
import Card from '@/components/Card.vue'

export default {
  components: {
    SkeletonCard,
    Card
  },
  data() {
    return {
      loading: true,
      cardData: null
    }
  },
  mounted() {
    this.fetchCardData()
  },
  methods: {
    async fetchCardData() {
      this.loading = true
      try {
        this.cardData = await api.getCard()
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
```

### 在列表中使用

```vue
<template>
  <div class="card-list">
    <!-- 加载状态：显示多个骨架卡片 -->
    <template v-if="loading">
      <SkeletonCard v-for="n in 3" :key="`skeleton-${n}`" />
    </template>
    
    <!-- 加载完成：显示真实卡片 -->
    <template v-else>
      <Card 
        v-for="card in cards" 
        :key="card.id" 
        :card="card" 
      />
    </template>
  </div>
</template>

<script>
import SkeletonCard from '@/components/SkeletonCard.vue'
import Card from '@/components/Card.vue'

export default {
  components: {
    SkeletonCard,
    Card
  },
  data() {
    return {
      loading: true,
      cards: []
    }
  },
  mounted() {
    this.fetchCards()
  },
  methods: {
    async fetchCards() {
      this.loading = true
      try {
        this.cards = await api.getCards()
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.card-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}
</style>
```

### 在 List 组件中使用

```vue
<template>
  <div class="list">
    <div class="list__header">
      <h3 class="list__title">{{ list.title }}</h3>
    </div>
    
    <div class="list__cards">
      <!-- 加载状态 -->
      <template v-if="loading">
        <SkeletonCard v-for="n in 5" :key="`skeleton-${n}`" />
      </template>
      
      <!-- 真实卡片 -->
      <template v-else>
        <Card 
          v-for="card in cards" 
          :key="card.id" 
          :card="card"
          @click="handleCardClick"
        />
      </template>
    </div>
  </div>
</template>
```

## API

### Props

该组件不接受任何 props。它是一个纯展示组件，专注于提供一致的加载状态视觉反馈。

### Events

该组件不触发任何事件。

### Slots

该组件不提供插槽。

## 样式说明

### CSS 类名

- `.skeleton-card` - 骨架卡片容器，模拟真实卡片的样式
- `.skeleton` - 骨架占位符基础类，定义 shimmer 动画
- `.skeleton--title` - 标题骨架，模拟卡片标题
- `.skeleton--text` - 文本骨架，模拟卡片内容
- `.skeleton--text-short` - 短文本骨架，模拟较短的文本行

### 动画效果

组件使用 `shimmer` 关键帧动画创建从左到右的闪烁效果：

```css
@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
```

动画持续时间为 1.5 秒，无限循环。

### 自定义样式

如果需要自定义骨架卡片的样式，可以通过 CSS 变量进行调整：

```css
/* 自定义骨架屏颜色 */
:root {
  --color-gray-100: #f0f0f0;
  --color-gray-200: #e0e0e0;
}

/* 或者在特定组件中覆盖 */
.my-custom-list .skeleton-card {
  /* 自定义样式 */
}
```

## 设计考虑

### 1. 布局模拟

SkeletonCard 的布局设计与真实的 Card 组件保持一致：

- **标题区域**：70% 宽度，20px 高度
- **文本区域**：两行文本，第一行 100% 宽度，第二行 60% 宽度
- **间距**：使用与真实卡片相同的间距变量

### 2. 视觉反馈

- **Shimmer 动画**：提供动态的加载反馈，让用户知道内容正在加载
- **颜色选择**：使用中性灰色，不会分散用户注意力
- **平滑过渡**：与真实内容的切换应该使用过渡动画

### 3. 性能优化

- **纯 CSS 动画**：使用 CSS 动画而非 JavaScript，性能更好
- **轻量级**：无 props、无事件、无逻辑，渲染速度快
- **可复用**：可以同时渲染多个实例而不影响性能

## 最佳实践

### 1. 显示合适数量的骨架卡片

```vue
<!-- 好的做法：显示预期数量的骨架卡片 -->
<SkeletonCard v-for="n in expectedCount" :key="`skeleton-${n}`" />

<!-- 避免：显示过多或过少的骨架卡片 -->
<SkeletonCard v-for="n in 100" :key="`skeleton-${n}`" />
```

### 2. 使用过渡动画

```vue
<template>
  <transition-group name="fade" tag="div" class="card-list">
    <SkeletonCard 
      v-if="loading" 
      v-for="n in 3" 
      :key="`skeleton-${n}`" 
    />
    <Card 
      v-else 
      v-for="card in cards" 
      :key="card.id" 
      :card="card" 
    />
  </transition-group>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-base);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

### 3. 结合错误状态

```vue
<template>
  <div class="card-container">
    <!-- 加载状态 -->
    <SkeletonCard v-if="loading" />
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="error-message">
      加载失败，请重试
    </div>
    
    <!-- 正常状态 -->
    <Card v-else :card="cardData" />
  </div>
</template>
```

### 4. 避免过度使用

骨架屏适合用于：
- ✅ 首次加载数据
- ✅ 页面切换时的内容加载
- ✅ 预期加载时间较长的操作

不适合用于：
- ❌ 即时响应的操作（如按钮点击）
- ❌ 加载时间极短的操作（< 200ms）
- ❌ 后台刷新数据（应该保持现有内容）

## 可访问性

虽然 SkeletonCard 是一个纯视觉组件，但仍需考虑可访问性：

```vue
<template>
  <div class="list__cards" aria-busy="true" aria-label="正在加载卡片">
    <SkeletonCard v-for="n in 3" :key="`skeleton-${n}`" />
  </div>
</template>
```

或者使用 ARIA live region：

```vue
<template>
  <div>
    <div v-if="loading" role="status" aria-live="polite">
      <span class="sr-only">正在加载内容...</span>
      <SkeletonCard v-for="n in 3" :key="`skeleton-${n}`" />
    </div>
    <div v-else>
      <Card v-for="card in cards" :key="card.id" :card="card" />
    </div>
  </div>
</template>

<style>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>
```

## 浏览器兼容性

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**注意**：组件使用 CSS 变量和现代 CSS 特性，不支持 IE11。

## 相关组件

- **Card** - 真实的卡片组件
- **LoadingSpinner** - 旋转加载指示器，适用于不同的加载场景
- **Toast** - 消息通知组件

## 需求映射

该组件实现了以下需求：

- **需求 7.4**：为加载状态使用骨架屏或加载指示器

## 测试

组件包含完整的单元测试，覆盖以下方面：

- ✅ 基本渲染
- ✅ 组件结构
- ✅ CSS 类名
- ✅ 样式模拟
- ✅ 动画效果
- ✅ 可访问性
- ✅ 边缘情况
- ✅ 性能

运行测试：

```bash
npm run test:unit -- SkeletonCard.spec.js
```

## 更新日志

### v1.0.0 (2024)
- ✨ 初始版本
- ✨ 实现基础骨架屏功能
- ✨ 添加 shimmer 动画效果
- ✨ 模拟真实卡片布局
