<!--
  Card 组件
  
  功能：
  - 显示卡片标题
  - 实现点击卡片打开详情功能
  - 支持拖拽（通过 Vue.Draggable）
  
  需求：3.6, 4.1, 4.3
-->
<template>
  <div 
    class="card"
    @click="handleClick"
  >
    <div class="card-content">
      <p class="card-title">{{ card.title }}</p>
      
      <!-- 卡片元数据 -->
      <div v-if="hasMetadata" class="card-metadata">
        <!-- 截止日期 -->
        <span v-if="card.due_date" class="metadata-item due-date" :class="dueDateClass">
          <span class="icon">📅</span>
          {{ formattedDueDate }}
        </span>
        
        <!-- 描述指示器 -->
        <span v-if="card.description" class="metadata-item description-indicator">
          <span class="icon">📝</span>
        </span>
        
        <!-- 标签 -->
        <div v-if="card.tags && card.tags.length > 0" class="tags">
          <span 
            v-for="(tag, index) in card.tags" 
            :key="index" 
            class="tag"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Card',
  
  props: {
    card: {
      type: Object,
      required: true
    }
  },
  
  computed: {
    /**
     * 检查卡片是否有元数据
     */
    hasMetadata() {
      return this.card.due_date || this.card.description || (this.card.tags && this.card.tags.length > 0)
    },
    
    /**
     * 格式化截止日期
     */
    formattedDueDate() {
      if (!this.card.due_date) return ''
      
      const date = new Date(this.card.due_date)
      const now = new Date()
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      const dueDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
      
      const diffTime = dueDate - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      const month = date.getMonth() + 1
      const day = date.getDate()
      
      if (diffDays < 0) {
        return `${month}月${day}日 (已逾期)`
      } else if (diffDays === 0) {
        return `${month}月${day}日 (今天)`
      } else if (diffDays === 1) {
        return `${month}月${day}日 (明天)`
      } else {
        return `${month}月${day}日`
      }
    },
    
    /**
     * 截止日期样式类
     */
    dueDateClass() {
      if (!this.card.due_date) return ''
      
      const date = new Date(this.card.due_date)
      const now = new Date()
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      const dueDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
      
      const diffTime = dueDate - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays < 0) {
        return 'overdue'
      } else if (diffDays === 0) {
        return 'due-today'
      } else if (diffDays <= 2) {
        return 'due-soon'
      }
      
      return ''
    }
  },
  
  methods: {
    /**
     * 处理卡片点击
     * 需求：3.6
     */
    handleClick() {
      this.$emit('click', this.card)
    }
  }
}
</script>

<style scoped>
/**
 * Card Component Styles
 * 现代化卡片样式
 * 
 * 需求：1.2, 1.3, 3.3, 4.1, 4.3
 */

.card {
  /* 基础样式 */
  padding: var(--spacing-md);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--radius-base);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  
  /* 过渡动画 - 使用 all 以支持多个属性变化 */
  transition: all var(--transition-base);
  
  /* 移除旧的 margin-bottom，由父容器的 gap 控制间距 */
}

/**
 * Hover 状态 - 提升效果
 * 需求：3.3, 4.1
 */
.card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

/**
 * Active 状态 - 按下效果
 * 需求：4.1
 */
.card:active {
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}

/**
 * 卡片标题
 * 需求：1.3
 */
.card-title {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
  word-wrap: break-word;
  line-height: var(--line-height-tight);
}

/**
 * 卡片元数据容器
 * 需求：1.3, 4.3
 */
.card-metadata {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-sm);
  align-items: center;
}

/**
 * 元数据项基础样式
 */
.metadata-item {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  padding: 2px var(--spacing-sm);
  border-radius: var(--radius-sm);
  background-color: var(--color-gray-100);
}

.icon {
  font-size: var(--font-size-xs);
}

/**
 * 截止日期样式
 * 使用语义化颜色
 */
.due-date {
  font-weight: var(--font-weight-medium);
}

.due-date.overdue {
  background-color: var(--color-error);
  color: white;
}

.due-date.due-today {
  background-color: var(--color-warning);
  color: var(--color-text-primary);
}

.due-date.due-soon {
  background-color: #ff9f1a;
  color: white;
}

.description-indicator {
  background-color: transparent;
  padding: 2px;
}

/**
 * 标签样式
 * 需求：3.3
 */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 2px var(--spacing-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  background: var(--color-gray-100);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
}

/**
 * 拖拽状态样式
 * 需求：4.3
 * 
 * .card--dragging 类用于自定义拖拽状态
 * .sortable-ghost 和 .sortable-drag 用于 Vue.Draggable 库
 */
.card--dragging,
.card.sortable-ghost,
.card.sortable-drag {
  opacity: 0.5;
  transform: rotate(3deg);
  box-shadow: var(--shadow-lg);
}

/**
 * 响应式设计 - 移动端媒体查询
 * 需求：5.1, 5.2
 */
@media (max-width: 767px) {
  .card {
    /* 调整卡片内边距 */
    padding: var(--spacing-sm);
  }
  
  .card-title {
    font-size: var(--font-size-sm);
    margin-bottom: var(--spacing-xs);
  }
  
  .card-metadata {
    gap: var(--spacing-xs);
    margin-top: var(--spacing-xs);
  }
  
  .metadata-item {
    font-size: 10px;
    padding: 2px var(--spacing-xs);
  }
  
  .icon {
    font-size: 10px;
  }
  
  .tag {
    font-size: 10px;
    padding: 2px var(--spacing-xs);
  }
  
  /* 移动端减少 hover 效果的位移 */
  .card:hover {
    transform: translateY(-1px);
  }
}

/**
 * 响应式设计 - 平板端媒体查询
 * 需求：5.1
 */
@media (min-width: 768px) and (max-width: 1023px) {
  .card {
    /* 平板端略微减少内边距 */
    padding: var(--spacing-sm) var(--spacing-md);
  }
  
  .card-title {
    font-size: var(--font-size-sm);
  }
  
  .metadata-item {
    font-size: 11px;
  }
  
  .tag {
    font-size: 11px;
  }
}

/**
 * 响应式设计 - 桌面端媒体查询
 * 需求：5.1 - 桌面设备适配
 */
@media (min-width: 1024px) {
  .card {
    /* 桌面端使用标准内边距 */
    padding: var(--spacing-md);
  }
  
  .card-title {
    font-size: var(--font-size-base);
  }
  
  .metadata-item {
    font-size: var(--font-size-xs);
  }
  
  .tag {
    font-size: var(--font-size-xs);
  }
  
  /* 桌面端增强 hover 效果 */
  .card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
  }
}

/**
 * 响应式设计 - 大屏媒体查询
 * 需求：5.1 - 大屏设备适配
 */
@media (min-width: 1440px) {
  .card {
    /* 大屏端增加内边距，提供更宽敞的布局 */
    padding: var(--spacing-lg);
  }
  
  .card-title {
    font-size: var(--font-size-lg);
    margin-bottom: var(--spacing-md);
  }
  
  .card-metadata {
    gap: var(--spacing-md);
    margin-top: var(--spacing-md);
  }
  
  .metadata-item {
    font-size: var(--font-size-sm);
    padding: 4px var(--spacing-sm);
  }
  
  .icon {
    font-size: var(--font-size-sm);
  }
  
  .tag {
    font-size: var(--font-size-sm);
    padding: 4px var(--spacing-sm);
  }
  
  /* 大屏端进一步增强 hover 效果 */
  .card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-xl);
  }
}
</style>
