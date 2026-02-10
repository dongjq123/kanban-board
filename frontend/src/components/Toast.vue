<template>
  <transition name="slide">
    <div v-if="visible" class="toast" :class="`toast--${type}`" role="alert">
      <div class="toast__icon">
        <i class="material-icons">{{ iconName }}</i>
      </div>
      <div class="toast__content">
        <div class="toast__title">{{ title }}</div>
        <div v-if="message" class="toast__message">{{ message }}</div>
      </div>
      <button class="toast__close" @click="close" aria-label="Close notification">
        <i class="material-icons">close</i>
      </button>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'Toast',
  props: {
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['success', 'warning', 'error', 'info'].includes(value)
    },
    title: {
      type: String,
      required: true
    },
    message: {
      type: String,
      default: ''
    },
    duration: {
      type: Number,
      default: 3000
    },
    autoClose: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      visible: true,
      timer: null
    };
  },
  computed: {
    iconName() {
      const icons = {
        success: 'check_circle',
        warning: 'warning',
        error: 'error',
        info: 'info'
      };
      return icons[this.type] || icons.info;
    }
  },
  mounted() {
    // Auto close after duration
    if (this.autoClose) {
      this.timer = setTimeout(() => {
        this.close();
      }, this.duration);
    }
  },
  beforeUnmount() {
    if (this.timer) {
      clearTimeout(this.timer);
    }
  },
  methods: {
    close() {
      this.visible = false;
      // Wait for animation to complete before emitting close event
      setTimeout(() => {
        this.$emit('close');
      }, 250); // Match transition duration
    }
  }
};
</script>

<style scoped>
.toast {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  min-width: 320px;
  max-width: 480px;
  padding: var(--spacing-md);
  background: var(--color-bg-primary);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  border-left: 4px solid var(--color-primary);
  position: relative;
}

.toast--success {
  border-left-color: var(--color-success);
}

.toast--warning {
  border-left-color: var(--color-warning);
}

.toast--error {
  border-left-color: var(--color-error);
}

.toast--info {
  border-left-color: var(--color-info);
}

.toast__icon {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-lg);
}

.toast--success .toast__icon {
  color: var(--color-success);
}

.toast--warning .toast__icon {
  color: var(--color-warning);
}

.toast--error .toast__icon {
  color: var(--color-error);
}

.toast--info .toast__icon {
  color: var(--color-info);
}

.toast__content {
  flex: 1;
  min-width: 0; /* Allow text to wrap properly */
}

.toast__title {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: 2px;
  font-size: var(--font-size-base);
  line-height: var(--line-height-tight);
}

.toast__message {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: var(--line-height-normal);
}

.toast__close {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-tertiary);
  cursor: pointer;
  border: none;
  background: none;
  padding: 0;
  transition: color var(--transition-fast);
  font-size: var(--font-size-lg);
}

.toast__close:hover {
  color: var(--color-text-primary);
}

.toast__close:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

/* Slide transition for toast */
.slide-enter-active,
.slide-leave-active {
  transition: all var(--transition-base);
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/**
 * 响应式设计 - 移动端媒体查询
 * 需求：5.1, 5.2
 */
@media (max-width: 767px) {
  .toast {
    min-width: 280px;
    max-width: calc(100vw - 32px);
    padding: var(--spacing-sm);
    gap: var(--spacing-sm);
  }
  
  .toast__icon {
    width: 20px;
    height: 20px;
    font-size: var(--font-size-base);
  }
  
  .toast__title {
    font-size: var(--font-size-sm);
  }
  
  .toast__message {
    font-size: var(--font-size-xs);
  }
  
  .toast__close {
    width: 20px;
    height: 20px;
    font-size: var(--font-size-base);
  }
}

/**
 * 响应式设计 - 平板端媒体查询
 * 需求：5.1
 */
@media (min-width: 768px) and (max-width: 1023px) {
  .toast {
    min-width: 300px;
    max-width: 420px;
  }
}

/**
 * 响应式设计 - 桌面端媒体查询
 * 需求：5.1 - 桌面设备适配
 */
@media (min-width: 1024px) {
  .toast {
    min-width: 340px;
    max-width: 500px;
    padding: var(--spacing-lg);
    gap: var(--spacing-lg);
  }
  
  .toast__icon {
    width: 28px;
    height: 28px;
    font-size: var(--font-size-xl);
  }
  
  .toast__title {
    font-size: var(--font-size-lg);
    margin-bottom: 4px;
  }
  
  .toast__message {
    font-size: var(--font-size-base);
  }
  
  .toast__close {
    width: 28px;
    height: 28px;
    font-size: var(--font-size-xl);
  }
}

/**
 * 响应式设计 - 大屏媒体查询
 * 需求：5.1 - 大屏设备适配
 */
@media (min-width: 1440px) {
  .toast {
    min-width: 380px;
    max-width: 560px;
    padding: var(--spacing-xl);
    gap: var(--spacing-xl);
  }
  
  .toast__icon {
    width: 32px;
    height: 32px;
    font-size: var(--font-size-2xl);
  }
  
  .toast__title {
    font-size: var(--font-size-xl);
    margin-bottom: var(--spacing-xs);
  }
  
  .toast__message {
    font-size: var(--font-size-lg);
  }
  
  .toast__close {
    width: 32px;
    height: 32px;
    font-size: var(--font-size-2xl);
  }
}
</style>
