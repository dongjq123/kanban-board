<!--
  AddButton 通用组件
  
  功能：
  - 实现可复用的添加按钮组件
  - 支持内联输入和提交
  - 支持文本输入和多行文本输入
  
  需求：1.1, 2.1, 3.2
-->
<template>
  <div class="add-button-container">
    <!-- 添加按钮 -->
    <div v-if="!showForm" class="add-button-wrapper">
      <button 
        class="btn-add" 
        :class="`btn-add--${variant}`"
        @click="handleShowForm"
        :disabled="disabled"
      >
        {{ buttonText }}
      </button>
    </div>
    
    <!-- 添加表单 -->
    <div v-else class="add-form">
      <!-- 文本输入框 -->
      <input
        v-if="inputType === 'text'"
        v-model="inputValue"
        type="text"
        :placeholder="placeholder"
        class="input input-field"
        @keyup.enter="handleSubmit"
        @keyup.esc="handleCancel"
        ref="inputField"
      />
      
      <!-- 多行文本输入框 -->
      <textarea
        v-else
        v-model="inputValue"
        :placeholder="placeholder"
        class="textarea textarea-field"
        @keyup.enter.exact="handleSubmit"
        @keyup.esc="handleCancel"
        ref="inputField"
        :rows="textareaRows"
      ></textarea>
      
      <!-- 操作按钮 -->
      <div class="form-actions">
        <button 
          class="btn-submit" 
          @click="handleSubmit"
          :disabled="!inputValue.trim() || disabled"
        >
          {{ submitText }}
        </button>
        <button 
          class="btn-cancel" 
          @click="handleCancel"
          :disabled="disabled"
        >
          取消
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddButton',
  
  props: {
    // 按钮文本（例如："+ 添加列表" 或 "+ 添加卡片"）
    buttonText: {
      type: String,
      default: '+ 添加'
    },
    
    // 提交按钮文本
    submitText: {
      type: String,
      default: '添加'
    },
    
    // 输入框占位符文本
    placeholder: {
      type: String,
      default: '输入内容...'
    },
    
    // 输入框类型：'text' 或 'textarea'
    inputType: {
      type: String,
      default: 'text',
      validator: (value) => ['text', 'textarea'].includes(value)
    },
    
    // textarea 的行数（仅当 inputType 为 'textarea' 时有效）
    textareaRows: {
      type: Number,
      default: 3
    },
    
    // 是否禁用
    disabled: {
      type: Boolean,
      default: false
    },
    
    // 是否自动显示表单（用于外部控制）
    visible: {
      type: Boolean,
      default: false
    },
    
    // 按钮变体：'primary'、'secondary' 或 'ghost'
    variant: {
      type: String,
      default: 'ghost',
      validator: (value) => ['primary', 'secondary', 'ghost'].includes(value)
    }
  },
  
  data() {
    return {
      showForm: false,
      inputValue: ''
    }
  },
  
  methods: {
    /**
     * 显示表单
     */
    handleShowForm() {
      this.showForm = true
      this.$nextTick(() => {
        this.$refs.inputField?.focus()
      })
    },
    
    /**
     * 提交表单
     * 需求：1.1, 2.1, 3.2
     */
    handleSubmit() {
      const value = this.inputValue.trim()
      
      if (!value) {
        return
      }
      
      // 触发 submit 事件，传递输入值
      this.$emit('submit', value)
      
      // 重置表单
      this.inputValue = ''
      this.showForm = false
    },
    
    /**
     * 取消添加
     */
    handleCancel() {
      this.inputValue = ''
      this.showForm = false
      
      // 触发 cancel 事件
      this.$emit('cancel')
    }
  },
  
  watch: {
    /**
     * 监听 visible 属性变化，支持外部控制表单显示
     */
    visible(newVal) {
      this.showForm = newVal
      if (newVal) {
        this.$nextTick(() => {
          this.$refs.inputField?.focus()
        })
      }
    },
    
    /**
     * 监听表单显示状态，同步到外部
     */
    showForm(newVal) {
      if (!newVal && this.visible) {
        this.$emit('update:visible', false)
      }
    }
  }
}
</script>

<style scoped>
.add-button-container {
  width: 100%;
}

/* 添加按钮包装器 */
.add-button-wrapper {
  padding: var(--spacing-xs);
}

/* 添加按钮基础样式 */
.btn-add {
  /* 布局 */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 44px; /* 确保最小点击区域 44x44px */
  padding: var(--spacing-sm) var(--spacing-md);
  
  /* 字体 */
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  font-family: var(--font-family-base);
  text-align: left;
  
  /* 边框和圆角 */
  border: none;
  border-radius: var(--radius-base);
  
  /* 过渡动画 */
  transition: all var(--transition-fast);
  
  /* 交互 */
  cursor: pointer;
}

/* 焦点状态 */
.btn-add:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* 禁用状态 */
.btn-add:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* Primary 变体 */
.btn-add--primary {
  background: var(--color-primary);
  color: white;
  box-shadow: var(--shadow-sm);
}

.btn-add--primary:hover:not(:disabled) {
  background: var(--color-primary-dark);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.btn-add--primary:active:not(:disabled) {
  background: var(--color-primary-dark);
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}

/* Secondary 变体 */
.btn-add--secondary {
  background: var(--color-gray-100);
  color: var(--color-text-primary);
  box-shadow: var(--shadow-sm);
}

.btn-add--secondary:hover:not(:disabled) {
  background: var(--color-gray-200);
  box-shadow: var(--shadow-base);
}

.btn-add--secondary:active:not(:disabled) {
  background: var(--color-gray-300);
  transform: scale(0.98);
}

/* Ghost 变体 */
.btn-add--ghost {
  background: transparent;
  color: var(--color-text-secondary);
}

.btn-add--ghost:hover:not(:disabled) {
  background: var(--color-gray-100);
  color: var(--color-text-primary);
}

.btn-add--ghost:active:not(:disabled) {
  background: var(--color-gray-200);
}

/* 添加表单 */
.add-form {
  background-color: var(--color-bg-primary);
  border-radius: var(--radius-base);
  padding: var(--spacing-sm);
  box-shadow: var(--shadow-base);
}

/* 输入框 - Component-specific overrides */
.input-field,
.textarea-field {
  /* Override border color to use primary color for this component */
  border-color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.input-field:hover,
.textarea-field:hover {
  border-color: var(--color-primary-dark);
}

.input-field:focus,
.textarea-field:focus {
  border-color: var(--color-primary-dark);
}

.textarea-field {
  min-height: 60px;
}

/* 操作按钮 */
.form-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.btn-submit,
.btn-cancel {
  /* 布局 */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px; /* 确保最小点击区域 */
  padding: var(--spacing-sm) var(--spacing-md);
  
  /* 字体 */
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  font-family: var(--font-family-base);
  
  /* 边框和圆角 */
  border: none;
  border-radius: var(--radius-base);
  
  /* 过渡动画 */
  transition: all var(--transition-fast);
  
  /* 交互 */
  cursor: pointer;
}

/* 提交按钮 */
.btn-submit {
  background: var(--color-primary);
  color: white;
  box-shadow: var(--shadow-sm);
}

.btn-submit:hover:not(:disabled) {
  background: var(--color-primary-dark);
  box-shadow: var(--shadow-md);
}

.btn-submit:active:not(:disabled) {
  background: var(--color-primary-dark);
  transform: scale(0.98);
}

.btn-submit:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* 取消按钮 */
.btn-cancel {
  background: var(--color-gray-100);
  color: var(--color-text-primary);
}

.btn-cancel:hover:not(:disabled) {
  background: var(--color-gray-200);
}

.btn-cancel:active:not(:disabled) {
  background: var(--color-gray-300);
  transform: scale(0.98);
}

.btn-cancel:focus {
  outline: 2px solid var(--color-gray-400);
  outline-offset: 2px;
}

.btn-cancel:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/**
 * 响应式设计 - 移动端媒体查询
 * 需求：5.1, 5.2
 */
@media (max-width: 767px) {
  /* 调整按钮尺寸 */
  .btn-add {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-sm);
    min-height: 40px;
  }
  
  /* 调整表单 */
  .add-form {
    padding: var(--spacing-xs);
  }
  
  .input-field,
  .textarea-field {
    font-size: var(--font-size-sm);
    padding: var(--spacing-xs) var(--spacing-sm);
  }
  
  .textarea-field {
    min-height: 50px;
  }
  
  /* 调整操作按钮 */
  .form-actions {
    gap: var(--spacing-xs);
  }
  
  .btn-submit,
  .btn-cancel {
    flex: 1;
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-sm);
    min-height: 40px;
  }
}

/**
 * 响应式设计 - 平板端媒体查询
 * 需求：5.1
 */
@media (min-width: 768px) and (max-width: 1023px) {
  /* 平板端保持标准尺寸，略微调整间距 */
  .add-form {
    padding: var(--spacing-sm);
  }
  
  .form-actions {
    gap: var(--spacing-sm);
  }
}

/**
 * 响应式设计 - 桌面端媒体查询
 * 需求：5.1 - 桌面设备适配
 */
@media (min-width: 1024px) {
  /* 桌面端使用标准尺寸 */
  .btn-add {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-sm);
    min-height: 44px;
  }
  
  .add-form {
    padding: var(--spacing-md);
  }
  
  .input-field,
  .textarea-field {
    font-size: var(--font-size-base);
    padding: var(--spacing-sm) var(--spacing-md);
  }
  
  .textarea-field {
    min-height: 60px;
  }
  
  .btn-submit,
  .btn-cancel {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-sm);
    min-height: 44px;
  }
}

/**
 * 响应式设计 - 大屏媒体查询
 * 需求：5.1 - 大屏设备适配
 */
@media (min-width: 1440px) {
  /* 大屏端增加尺寸，提供更宽敞的布局 */
  .btn-add {
    padding: var(--spacing-md) var(--spacing-lg);
    font-size: var(--font-size-base);
    min-height: 48px;
  }
  
  .add-form {
    padding: var(--spacing-lg);
  }
  
  .input-field,
  .textarea-field {
    font-size: var(--font-size-lg);
    padding: var(--spacing-md) var(--spacing-lg);
  }
  
  .textarea-field {
    min-height: 80px;
  }
  
  .form-actions {
    gap: var(--spacing-md);
  }
  
  .btn-submit,
  .btn-cancel {
    padding: var(--spacing-md) var(--spacing-lg);
    font-size: var(--font-size-base);
    min-height: 48px;
  }
}
</style>
