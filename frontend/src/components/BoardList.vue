<!--
  BoardList 组件
  
  功能：
  - 显示所有看板列表
  - 实现创建新看板功能
  - 实现选择看板功能
  - 实现删除看板功能
  
  需求：1.1, 1.3, 1.5
-->
<template>
  <div class="board-list-container">
    <div class="board-list-header">
      <h2>我的看板</h2>
      <button 
        class="btn-create-board" 
        @click="showCreateForm = true"
        :disabled="loading"
      >
        + 创建新看板
      </button>
    </div>

    <!-- 创建看板表单 -->
    <div v-if="showCreateForm" class="create-board-form">
      <input
        v-model="newBoardName"
        type="text"
        placeholder="输入看板名称..."
        class="input board-name-input"
        @keyup.enter="handleCreateBoard"
        @keyup.esc="cancelCreate"
        ref="createInput"
      />
      <div class="form-actions">
        <button 
          class="btn-submit" 
          @click="handleCreateBoard"
          :disabled="!newBoardName.trim() || loading"
        >
          创建
        </button>
        <button 
          class="btn-cancel" 
          @click="cancelCreate"
          :disabled="loading"
        >
          取消
        </button>
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading && boards.length === 0" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 看板列表 -->
    <div v-else-if="boards.length > 0" class="boards-grid">
      <div
        v-for="board in boards"
        :key="board.id"
        class="board-card"
        @click="handleSelectBoard(board)"
      >
        <div class="board-card-content">
          <h3 class="board-name">{{ board.name }}</h3>
          <p class="board-date">创建于 {{ formatDate(board.created_at) }}</p>
        </div>
        <button
          class="btn-delete"
          @click.stop="handleDeleteBoard(board.id)"
          :disabled="loading"
          title="删除看板"
        >
          ×
        </button>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <p>还没有看板，点击上方按钮创建第一个看板吧！</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="error && !showCreateForm" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'

export default {
  name: 'BoardList',
  
  data() {
    return {
      showCreateForm: false,
      newBoardName: ''
    }
  },
  
  computed: {
    ...mapState('boards', ['loading', 'error']),
    ...mapGetters('boards', ['allBoards']),
    
    boards() {
      return this.allBoards
    }
  },
  
  methods: {
    ...mapActions('boards', ['fetchBoards', 'createBoard', 'deleteBoard']),
    
    /**
     * 创建新看板
     * 需求：1.1, 1.2
     */
    async handleCreateBoard() {
      const name = this.newBoardName.trim()
      
      if (!name) {
        return
      }
      
      try {
        await this.createBoard({ name })
        this.newBoardName = ''
        this.showCreateForm = false
      } catch (error) {
        // 错误已经在 store 中处理
        console.error('创建看板失败:', error)
      }
    },
    
    /**
     * 取消创建
     */
    cancelCreate() {
      this.showCreateForm = false
      this.newBoardName = ''
    },
    
    /**
     * 选择看板
     * 需求：1.3
     */
    handleSelectBoard(board) {
      this.$store.commit('boards/setCurrentBoard', board)
      this.$router.push(`/boards/${board.id}`)  // 导航到看板详情页面
    },
    
    /**
     * 删除看板
     * 需求：1.5, 1.6
     */
    async handleDeleteBoard(boardId) {
      if (!confirm('确定要删除这个看板吗？删除后将无法恢复，且会同时删除该看板下的所有列表和卡片。')) {
        return
      }
      
      try {
        await this.deleteBoard(boardId)
      } catch (error) {
        // 错误已经在 store 中处理
        console.error('删除看板失败:', error)
      }
    },
    
    /**
     * 格式化日期
     */
    formatDate(dateString) {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      
      return `${year}-${month}-${day}`
    }
  },
  
  /**
   * 组件挂载时获取所有看板
   * 需求：1.3
   */
  mounted() {
    this.fetchBoards()
  },
  
  /**
   * 监听创建表单显示状态，自动聚焦输入框
   */
  watch: {
    showCreateForm(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.$refs.createInput?.focus()
        })
      }
    }
  }
}
</script>

<style scoped>
.board-list-container {
  max-width: 1200px;
  margin: 0 auto;
}

.board-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.board-list-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #172b4d;
}

.btn-create-board {
  background-color: #0079bf;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-create-board:hover:not(:disabled) {
  background-color: #026aa7;
}

.btn-create-board:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 创建看板表单 */
.create-board-form {
  background-color: white;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.board-name-input {
  /* Component-specific overrides for board name input */
  margin-bottom: 12px;
  /* Base input styles are inherited from .input class */
}

.form-actions {
  display: flex;
  gap: 8px;
}

.btn-submit,
.btn-cancel {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-submit {
  background-color: #0079bf;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background-color: #026aa7;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: #f4f5f7;
  color: #172b4d;
}

.btn-cancel:hover:not(:disabled) {
  background-color: #e4e6ea;
}

/* 加载状态 */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #5e6c84;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f4f5f7;
  border-top-color: #0079bf;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 看板网格 */
.boards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

/* 看板卡片 */
.board-card {
  position: relative;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.board-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.board-card-content {
  padding-right: 30px;
}

.board-name {
  font-size: 18px;
  font-weight: 600;
  color: #172b4d;
  margin-bottom: 8px;
  word-wrap: break-word;
}

.board-date {
  font-size: 12px;
  color: #5e6c84;
}

.btn-delete {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 28px;
  height: 28px;
  background-color: transparent;
  border: none;
  border-radius: 4px;
  font-size: 24px;
  line-height: 1;
  color: #5e6c84;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-delete:hover:not(:disabled) {
  background-color: #eb5a46;
  color: white;
}

.btn-delete:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #5e6c84;
  font-size: 16px;
}

/* 错误提示 */
.error-message {
  background-color: #ffebe6;
  color: #bf2600;
  padding: 12px 16px;
  border-radius: 4px;
  margin-top: 12px;
  font-size: 14px;
}

/* 响应式设计 - 移动端媒体查询 */
/* 需求：5.1, 5.2 - 移动设备适配 */
@media (max-width: 767px) {
  .board-list-container {
    padding: var(--spacing-md);
  }
  
  .board-list-header {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-md);
  }
  
  .board-list-header h2 {
    font-size: var(--font-size-xl);
  }
  
  .btn-create-board {
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-sm);
  }
  
  /* 创建表单 */
  .create-board-form {
    padding: var(--spacing-sm);
    margin-bottom: var(--spacing-md);
  }
  
  .board-name-input {
    font-size: var(--font-size-sm);
    margin-bottom: var(--spacing-sm);
  }
  
  .form-actions {
    gap: var(--spacing-xs);
  }
  
  .btn-submit,
  .btn-cancel {
    flex: 1;
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-sm);
  }
  
  /* 看板网格 - 单列布局 */
  .boards-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-sm);
  }
  
  /* 看板卡片 */
  .board-card {
    padding: var(--spacing-md);
  }
  
  .board-name {
    font-size: var(--font-size-base);
    margin-bottom: var(--spacing-xs);
  }
  
  .board-date {
    font-size: 11px;
  }
  
  .btn-delete {
    width: 32px;
    height: 32px;
    top: var(--spacing-sm);
    right: var(--spacing-sm);
  }
  
  /* 空状态 */
  .empty-state {
    padding: var(--spacing-2xl) var(--spacing-md);
    font-size: var(--font-size-sm);
  }
  
  /* 错误提示 */
  .error-message {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-xs);
  }
}

/* 响应式设计 - 平板端媒体查询 */
/* 需求：5.1 - 平板设备适配 */
@media (min-width: 768px) and (max-width: 1023px) {
  .board-list-container {
    padding: var(--spacing-lg);
  }
  
  /* 看板网格 - 双列布局 */
  .boards-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-md);
  }
  
  /* 看板卡片 */
  .board-card {
    padding: var(--spacing-lg);
  }
}

/* 响应式设计 - 桌面端媒体查询 */
/* 需求：5.1 - 桌面设备适配 */
@media (min-width: 1024px) {
  .board-list-container {
    padding: var(--spacing-xl);
    max-width: 1200px;
  }
  
  .board-list-header {
    margin-bottom: var(--spacing-xl);
  }
  
  .board-list-header h2 {
    font-size: var(--font-size-3xl);
  }
  
  .btn-create-board {
    padding: var(--spacing-sm) var(--spacing-lg);
    font-size: var(--font-size-base);
  }
  
  /* 创建表单 */
  .create-board-form {
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
  }
  
  .board-name-input {
    font-size: var(--font-size-base);
    margin-bottom: var(--spacing-md);
  }
  
  .form-actions {
    gap: var(--spacing-sm);
  }
  
  .btn-submit,
  .btn-cancel {
    padding: var(--spacing-sm) var(--spacing-lg);
    font-size: var(--font-size-base);
  }
  
  /* 看板网格 - 三列布局 */
  .boards-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-lg);
  }
  
  /* 看板卡片 */
  .board-card {
    padding: var(--spacing-xl);
  }
  
  .board-name {
    font-size: var(--font-size-xl);
    margin-bottom: var(--spacing-sm);
  }
  
  .board-date {
    font-size: var(--font-size-sm);
  }
  
  .btn-delete {
    width: 32px;
    height: 32px;
    font-size: 28px;
  }
  
  /* 空状态 */
  .empty-state {
    padding: var(--spacing-3xl) var(--spacing-xl);
    font-size: var(--font-size-lg);
  }
  
  /* 错误提示 */
  .error-message {
    padding: var(--spacing-md) var(--spacing-lg);
    font-size: var(--font-size-base);
  }
}

/* 响应式设计 - 大屏媒体查询 */
/* 需求：5.1 - 大屏设备适配 */
@media (min-width: 1440px) {
  .board-list-container {
    padding: var(--spacing-2xl);
    max-width: 1400px;
  }
  
  .board-list-header {
    margin-bottom: var(--spacing-2xl);
  }
  
  .board-list-header h2 {
    font-size: var(--font-size-3xl);
    font-weight: var(--font-weight-bold);
  }
  
  .btn-create-board {
    padding: var(--spacing-md) var(--spacing-xl);
    font-size: var(--font-size-lg);
  }
  
  /* 创建表单 */
  .create-board-form {
    padding: var(--spacing-xl);
    margin-bottom: var(--spacing-2xl);
  }
  
  .board-name-input {
    font-size: var(--font-size-lg);
    padding: var(--spacing-md) var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
  }
  
  .form-actions {
    gap: var(--spacing-md);
  }
  
  .btn-submit,
  .btn-cancel {
    padding: var(--spacing-md) var(--spacing-xl);
    font-size: var(--font-size-lg);
  }
  
  /* 看板网格 - 四列布局 */
  .boards-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: var(--spacing-xl);
  }
  
  /* 看板卡片 */
  .board-card {
    padding: var(--spacing-2xl);
  }
  
  .board-card-content {
    padding-right: 40px;
  }
  
  .board-name {
    font-size: var(--font-size-2xl);
    margin-bottom: var(--spacing-md);
  }
  
  .board-date {
    font-size: var(--font-size-base);
  }
  
  .btn-delete {
    width: 36px;
    height: 36px;
    font-size: 32px;
    top: var(--spacing-lg);
    right: var(--spacing-lg);
  }
  
  /* 空状态 */
  .empty-state {
    padding: var(--spacing-3xl) var(--spacing-2xl);
    font-size: var(--font-size-xl);
  }
  
  /* 错误提示 */
  .error-message {
    padding: var(--spacing-lg) var(--spacing-xl);
    font-size: var(--font-size-lg);
  }
}
</style>
