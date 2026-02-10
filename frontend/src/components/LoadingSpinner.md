# LoadingSpinner 组件

一个可复用的加载旋转动画组件，用于显示加载状态。

## 功能特性

- ✅ 支持两种尺寸：`small` (20px) 和 `normal` (40px)
- ✅ 使用 CSS 变量定义颜色，与设计系统一致
- ✅ 平滑的旋转动画
- ✅ 支持 `prefers-reduced-motion` 可访问性特性
- ✅ 轻量级，无外部依赖

## 使用方法

### 基本使用

```vue
<template>
  <div>
    <!-- 默认尺寸 (normal) -->
    <LoadingSpinner />
    
    <!-- 小尺寸 -->
    <LoadingSpinner size="small" />
  </div>
</template>

<script>
import LoadingSpinner from '@/components/LoadingSpinner.vue'

export default {
  components: {
    LoadingSpinner
  }
}
</script>
```

### 在加载状态中使用

```vue
<template>
  <div>
    <div v-if="loading" class="loading-container">
      <LoadingSpinner />
      <p>加载中...</p>
    </div>
    
    <div v-else>
      <!-- 内容 -->
    </div>
  </div>
</template>

<script>
import LoadingSpinner from '@/components/LoadingSpinner.vue'

export default {
  components: {
    LoadingSpinner
  },
  data() {
    return {
      loading: true
    }
  }
}
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-xl);
}
</style>
```

### 在按钮中使用

```vue
<template>
  <button :disabled="loading" class="btn">
    <LoadingSpinner v-if="loading" size="small" />
    <span v-else>提交</span>
  </button>
</template>

<script>
import LoadingSpinner from '@/components/LoadingSpinner.vue'

export default {
  components: {
    LoadingSpinner
  },
  data() {
    return {
      loading: false
    }
  }
}
</script>
```

### 在覆盖层中使用

```vue
<template>
  <div class="content-wrapper">
    <!-- 内容 -->
    <div class="content">
      ...
    </div>
    
    <!-- 加载覆盖层 -->
    <div v-if="loading" class="loading-overlay">
      <LoadingSpinner />
    </div>
  </div>
</template>

<script>
import LoadingSpinner from '@/components/LoadingSpinner.vue'

export default {
  components: {
    LoadingSpinner
  },
  data() {
    return {
      loading: false
    }
  }
}
</script>

<style scoped>
.content-wrapper {
  position: relative;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}
</style>
```

## Props

| 属性 | 类型 | 默认值 | 可选值 | 说明 |
|------|------|--------|--------|------|
| size | String | 'normal' | 'small', 'normal' | 加载指示器的尺寸 |

## 尺寸规格

- **normal**: 40px × 40px，边框宽度 3px
- **small**: 20px × 20px，边框宽度 2px

## 样式定制

组件使用以下 CSS 变量，可以通过修改这些变量来定制样式：

- `--color-gray-200`: 加载圈的背景色
- `--color-primary`: 加载圈的前景色（旋转部分）
- `--radius-full`: 圆角半径（9999px）

## 可访问性

组件支持 `prefers-reduced-motion` 媒体查询，为偏好减少动画的用户提供更慢的动画速度。

## 浏览器兼容性

- Chrome/Edge: ✅
- Firefox: ✅
- Safari: ✅
- IE11: ⚠️ 需要 CSS 变量 polyfill

## 相关需求

- 需求 7.1: 数据加载时显示优雅的加载动画
- 需求 7.4: 为加载状态使用骨架屏或加载指示器

## 示例截图

```
Normal 尺寸:
  ⟳  (40px × 40px)

Small 尺寸:
  ⟳  (20px × 20px)
```

## 迁移指南

如果你的代码中有类似以下的内联加载指示器：

```vue
<!-- 旧代码 -->
<div class="spinner"></div>

<style>
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f4f5f7;
  border-top-color: #0079bf;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
</style>
```

可以替换为：

```vue
<!-- 新代码 -->
<LoadingSpinner />

<script>
import LoadingSpinner from '@/components/LoadingSpinner.vue'

export default {
  components: {
    LoadingSpinner
  }
}
</script>
```

这样可以：
- 减少重复代码
- 确保样式一致性
- 使用设计系统的颜色变量
- 获得可访问性支持
