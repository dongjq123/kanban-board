<!--
  Board 组件
  
  功能：
  - 显示当前看板和其下的所有列表
  - 实现编辑看板名称功能
  - 实现添加新列表功能
  - 集成列表拖拽排序功能
  
  需求：1.4, 2.1, 2.6
-->
<template>
  <div class="board-container">
    <!-- 看板头部 -->
    <div class="board-header">
      <!-- 看板名称（可编辑） -->
      <div class="board-title-section">
        <h2 
          v-if="!isEditingBoardName" 
          class="board-title"
          @click="startEditBoardName"
          title="点击编辑看板名称"
        >
          {{ currentBoard?.name || '未命名看板' }}
        </h2>
        <input
          v-else
          v-model="editedBoardName"
          type="text"
          class="input board-title-input"
          @blur="saveBoardName"
          @keyup.enter="saveBoardName"
          @keyup.esc="cancelEditBoardName"
          ref="boardNameInput"
        />
      </div>
      
      <!-- 返回按钮 -->
      <button 
        class="btn-back" 
        @click="handleBack"
        title="返回看板列表"
      >
        ← 返回看板列表
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading && lists.length === 0" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 列表容器 -->
    <div v-else class="lists-container">
      <!-- 使用 vuedraggable 实现列表拖拽排序 -->
      <draggable
        v-model="sortedLists"
        :animation="200"
        ghost-class="ghost"
        drag-class="drag"
        handle=".list-header"
        @end="handleListDragEnd"
        class="lists-wrapper"
        item-key="id"
      >
        <template #item="{ element: list }">
          <div class="list-wrapper" :key="list.id">
            <List :list="list" />
          </div>
        </template>
      </draggable>

      <!-- 添加新列表 -->
      <div class="add-list-container">
        <div v-if="!showAddListForm" class="add-list-button-wrapper">
          <button 
            class="btn-add-list" 
            @click="showAddListForm = true"
            :disabled="loading"
          >
            + 添加列表
          </button>
        </div>
        
        <div v-else class="add-list-form">
          <input
            v-model="newListName"
            type="text"
            placeholder="输入列表名称..."
            class="input list-name-input"
            @keyup.enter="handleCreateList"
            @keyup.esc="cancelAddList"
            ref="listNameInput"
          />
          <div class="form-actions">
            <button 
              class="btn-submit" 
              @click="handleCreateList"
              :disabled="!newListName.trim() || loading"
            >
              添加列表
            </button>
            <button 
              class="btn-cancel" 
              @click="cancelAddList"
              :disabled="loading"
            >
              取消
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import draggable from 'vuedraggable'
import List from './List.vue'

export default {
  name: 'Board',
  
  components: {
    draggable,
    List
  },
  
  props: {
    boardId: {
      type: Number,
      required: true
    }
  },
  
  data() {
    return {
      isEditingBoardName: false,
      editedBoardName: '',
      showAddListForm: false,
      newListName: ''
    }
  },
  
  computed: {
    ...mapState('boards', {
      currentBoard: state => state.currentBoard,
      boardsLoading: state => state.loading,
      boardsError: state => state.error
    }),
    ...mapState('lists', {
      lists: state => state.lists,
      listsLoading: state => state.loading,
      listsError: state => state.error
    }),
    
    // 合并加载状态和错误
    loading() {
      return this.boardsLoading || this.listsLoading
    },
    
    error() {
      return this.boardsError || this.listsError
    },
    
    // 按位置排序的列表
    sortedLists: {
      get() {
        // 确保 lists 是数组，防止扩展运算符错误
        const lists = Array.isArray(this.lists) ? this.lists : []
        return [...lists].sort((a, b) => a.position - b.position)
      },
      set(value) {
        // 当拖拽改变顺序时，更新 store
        // 这里只是临时更新，实际的持久化在 handleListDragEnd 中完成
        this.$store.commit('lists/setLists', value)
      }
    }
  },
  
  methods: {
    ...mapActions('boards', ['updateBoard', 'fetchBoard']),
    ...mapActions('lists', ['fetchLists', 'createList', 'updateListPosition']),
    
    /**
     * 开始编辑看板名称
     * 需求：1.4
     */
    startEditBoardName() {
      if (!this.currentBoard) return
      
      this.isEditingBoardName = true
      this.editedBoardName = this.currentBoard.name
      
      this.$nextTick(() => {
        this.$refs.boardNameInput?.focus()
        this.$refs.boardNameInput?.select()
      })
    },
    
    /**
     * 保存看板名称
     * 需求：1.4
     */
    async saveBoardName() {
      const name = this.editedBoardName.trim()
      
      if (!name || name === this.currentBoard.name) {
        this.cancelEditBoardName()
        return
      }
      
      try {
        await this.updateBoard({
          id: this.currentBoard.id,
          data: { name }
        })
        this.isEditingBoardName = false
      } catch (error) {
        console.error('更新看板名称失败:', error)
        // 错误已经在 store 中处理
      }
    },
    
    /**
     * 取消编辑看板名称
     */
    cancelEditBoardName() {
      this.isEditingBoardName = false
      this.editedBoardName = ''
    },
    
    /**
     * 创建新列表
     * 需求：2.1
     */
    async handleCreateList() {
      const name = this.newListName.trim()
      
      if (!name || !this.currentBoard) {
        return
      }
      
      try {
        // 计算新列表的位置（在最后）
        const position = this.lists.length
        
        await this.createList({
          boardId: this.currentBoard.id,
          data: { name, position }
        })
        
        this.newListName = ''
        this.showAddListForm = false
      } catch (error) {
        console.error('创建列表失败:', error)
        // 错误已经在 store 中处理
      }
    },
    
    /**
     * 取消添加列表
     */
    cancelAddList() {
      this.showAddListForm = false
      this.newListName = ''
    },
    
    /**
     * 处理列表拖拽结束
     * 需求：2.6, 2.7
     */
    async handleListDragEnd(event) {
      const { oldIndex, newIndex } = event
      
      // 如果位置没有变化，不需要更新
      if (oldIndex === newIndex) {
        return
      }
      
      // 获取被移动的列表
      const movedList = this.sortedLists[newIndex]
      
      try {
        // 更新列表位置到后端
        await this.updateListPosition({
          id: movedList.id,
          position: newIndex
        })
        
        // 更新所有受影响的列表的位置
        // 这样可以确保位置值是连续的
        const updates = this.sortedLists.map((list, index) => {
          if (list.position !== index) {
            return this.updateListPosition({
              id: list.id,
              position: index
            })
          }
          return null
        }).filter(Boolean)
        
        // 等待所有更新完成
        if (updates.length > 0) {
          await Promise.all(updates)
        }
      } catch (error) {
        console.error('更新列表位置失败:', error)
        // 如果更新失败，重新获取列表以恢复正确的顺序
        if (this.currentBoard) {
          await this.fetchLists(this.currentBoard.id)
        }
      }
    },
    
    /**
     * 返回看板列表
     */
    handleBack() {
      // 清除当前看板
      this.$store.commit('boards/setCurrentBoard', null)
      // 清除列表
      this.$store.commit('lists/setLists', [])
      
      // 导航回主页（看板列表）
      this.$router.push('/')
    }
  },
  
  /**
   * 组件挂载时获取看板和列表
   * 需求：2.1
   */
  async mounted() {
    console.log('[Board] Mounting with boardId:', this.boardId)
    
    try {
      // 如果没有 currentBoard 或者 currentBoard 的 id 与 boardId 不匹配，则获取看板详情
      if (!this.currentBoard || this.currentBoard.id !== this.boardId) {
        console.log('[Board] Fetching board details for boardId:', this.boardId)
        await this.fetchBoard(this.boardId)
        console.log('[Board] Board fetched:', this.currentBoard)
      }
      
      // 获取该看板的列表
      console.log('[Board] Fetching lists for boardId:', this.boardId)
      const lists = await this.fetchLists(this.boardId)
      console.log('[Board] Lists fetched:', lists)
    } catch (error) {
      console.error('[Board] 加载看板失败:', error)
      this.$store.commit('boards/setError', '加载看板失败，请重试')
    }
  },
  
  /**
   * 监听添加列表表单显示状态，自动聚焦输入框
   */
  watch: {
    showAddListForm(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.$refs.listNameInput?.focus()
        })
      }
    }
  }
}
</script>

<style scoped>
/* 
  Board Component Styles
  现代化看板组件样式
  
  需求：1.2, 1.3, 2.1, 2.5
  - 应用现代化背景渐变效果
  - 优化看板头部样式（毛玻璃效果）
  - 实现列表容器的横向滚动和自定义滚动条
  - 优化列表之间的间距
*/

.board-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  /* 现代化背景渐变效果 - 需求 1.2, 1.3 */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
}

/* 看板头部 - 毛玻璃效果 */
.board-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-md) var(--spacing-lg);
  /* 毛玻璃效果 - 需求 1.3, 2.1 */
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  transition: box-shadow var(--transition-base);
}

.board-header:hover {
  box-shadow: var(--shadow-lg);
}

.board-title-section {
  flex: 1;
}

.board-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-base);
  cursor: pointer;
  display: inline-block;
  transition: background-color var(--transition-fast);
}

.board-title:hover {
  background-color: var(--color-gray-100);
}

.board-title-input {
  /* Component-specific overrides for board title input */
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  min-width: 300px;
  /* Base input styles are inherited from .input class */
}

.btn-back {
  background-color: var(--color-gray-100);
  color: var(--color-text-primary);
  border: none;
  border-radius: var(--radius-base);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  min-height: 44px;
}

.btn-back:hover {
  background-color: var(--color-gray-200);
  box-shadow: var(--shadow-sm);
}

.btn-back:active {
  transform: scale(0.98);
}

/* 加载状态 */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-3xl) var(--spacing-lg);
  color: white;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: var(--radius-full);
  animation: spin 0.8s linear infinite;
  margin-bottom: var(--spacing-md);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 列表容器 - 横向滚动和自定义滚动条 */
.lists-container {
  flex: 1;
  display: flex;
  padding: 0 var(--spacing-lg) var(--spacing-lg);
  overflow-x: auto;
  overflow-y: hidden;
  /* 自定义滚动条 - 需求 2.5 */
}

/* 自定义滚动条样式 - Webkit 浏览器 */
.lists-container::-webkit-scrollbar {
  height: 8px;
}

.lists-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-full);
  margin: 0 var(--spacing-lg);
}

.lists-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: var(--radius-full);
  transition: background var(--transition-fast);
}

.lists-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

.lists-wrapper {
  display: flex;
  gap: var(--spacing-md); /* 优化列表间距 - 需求 2.5 */
  min-height: 100%;
  padding-bottom: var(--spacing-md);
}

.list-wrapper {
  flex-shrink: 0;
}

/* 拖拽样式 */
.ghost {
  opacity: 0.5;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: var(--radius-md);
}

.drag {
  opacity: 0.8;
  transform: rotate(2deg);
  box-shadow: var(--shadow-lg);
}

/* 添加列表 */
.add-list-container {
  flex-shrink: 0;
  width: 280px;
}

.add-list-button-wrapper {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: var(--radius-base);
  padding: var(--spacing-md);
  transition: all var(--transition-fast);
}

.add-list-button-wrapper:hover {
  background-color: rgba(255, 255, 255, 0.4);
  box-shadow: var(--shadow-sm);
}

.btn-add-list {
  width: 100%;
  background-color: transparent;
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  text-align: left;
  transition: background-color var(--transition-fast);
  min-height: 44px;
}

.btn-add-list:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.2);
}

.btn-add-list:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.add-list-form {
  background-color: var(--color-bg-tertiary);
  border-radius: var(--radius-base);
  padding: var(--spacing-md);
  box-shadow: var(--shadow-base);
}

.list-name-input {
  /* Component-specific overrides for list name input */
  margin-bottom: var(--spacing-md);
  /* Base input styles are inherited from .input class */
}

.form-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.btn-submit,
.btn-cancel {
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  border-radius: var(--radius-base);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  min-height: 44px;
}

.btn-submit {
  background-color: var(--color-primary);
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
  box-shadow: var(--shadow-md);
}

.btn-submit:active:not(:disabled) {
  transform: scale(0.98);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: var(--color-gray-100);
  color: var(--color-text-primary);
}

.btn-cancel:hover:not(:disabled) {
  background-color: var(--color-gray-200);
}

.btn-cancel:active:not(:disabled) {
  transform: scale(0.98);
}

/* 错误提示 */
.error-message {
  position: fixed;
  bottom: var(--spacing-lg);
  left: 50%;
  transform: translateX(-50%);
  background-color: var(--color-error);
  color: white;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-base);
  font-size: var(--font-size-sm);
  box-shadow: var(--shadow-xl);
  z-index: 1000;
}

/* 响应式设计 - 移动端媒体查询 */
/* 需求：5.1, 5.2 - 移动设备适配 */
@media (max-width: 767px) {
  .board-container {
    min-height: 100vh;
  }

  /* 调整看板头部布局 - 垂直排列 */
  .board-header {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
    margin: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
    padding: var(--spacing-md);
  }
  
  .board-title-section {
    width: 100%;
  }
  
  .board-title {
    font-size: var(--font-size-xl);
    padding: var(--spacing-xs) var(--spacing-sm);
  }
  
  .board-title-input {
    width: 100%;
    min-width: 100%;
    font-size: var(--font-size-xl);
  }
  
  .btn-back {
    width: 100%;
    justify-content: center;
  }
  
  /* 调整列表容器 - 垂直堆叠 */
  .lists-container {
    flex-direction: column;
    padding: 0 var(--spacing-md) var(--spacing-md);
    overflow-x: hidden;
    overflow-y: auto;
  }
  
  .lists-wrapper {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .list-wrapper {
    width: 100%;
  }
  
  /* 调整添加列表容器 */
  .add-list-container {
    width: 100%;
  }
  
  .add-list-form {
    padding: var(--spacing-sm);
  }
  
  .list-name-input {
    font-size: var(--font-size-base);
  }
  
  /* 调整按钮尺寸 */
  .btn-submit,
  .btn-cancel {
    flex: 1;
    padding: var(--spacing-sm);
  }
}

/* 响应式设计 - 平板端媒体查询 */
/* 需求：5.1 - 平板设备适配 */
@media (min-width: 768px) and (max-width: 1023px) {
  /* 调整看板内边距 */
  .board-header {
    margin: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
    padding: var(--spacing-md) var(--spacing-lg);
  }
  
  /* 调整列表容器间距 */
  .lists-container {
    padding: 0 var(--spacing-md) var(--spacing-md);
  }
  
  .lists-wrapper {
    gap: var(--spacing-sm);
  }
  
  /* 调整添加列表容器宽度 */
  .add-list-container {
    width: 260px;
  }
}

/* 响应式设计 - 桌面端媒体查询 */
/* 需求：5.1 - 桌面设备适配 */
@media (min-width: 1024px) {
  /* 增加看板内边距，提供更宽敞的布局 */
  .board-header {
    margin: var(--spacing-xl);
    margin-bottom: var(--spacing-2xl);
    padding: var(--spacing-lg) var(--spacing-xl);
  }
  
  /* 增加列表容器间距 */
  .lists-container {
    padding: 0 var(--spacing-xl) var(--spacing-xl);
  }
  
  .lists-wrapper {
    gap: var(--spacing-md);
  }
  
  /* 标准列表宽度 */
  .add-list-container {
    width: 280px;
  }
  
  /* 优化看板标题 */
  .board-title {
    font-size: var(--font-size-3xl);
  }
  
  .board-title-input {
    font-size: var(--font-size-3xl);
    min-width: 400px;
  }
}

/* 响应式设计 - 大屏媒体查询 */
/* 需求：5.1 - 大屏设备适配 */
@media (min-width: 1440px) {
  /* 进一步增加看板内边距 */
  .board-header {
    margin: var(--spacing-2xl);
    margin-bottom: var(--spacing-3xl);
    padding: var(--spacing-xl) var(--spacing-2xl);
  }
  
  /* 增加列表容器间距 */
  .lists-container {
    padding: 0 var(--spacing-2xl) var(--spacing-2xl);
  }
  
  .lists-wrapper {
    gap: var(--spacing-lg);
  }
  
  /* 增加列表宽度以利用大屏空间 */
  .add-list-container {
    width: 320px;
  }
  
  /* 优化看板标题尺寸 */
  .board-title {
    font-size: var(--font-size-3xl);
  }
  
  .board-title-input {
    font-size: var(--font-size-3xl);
    min-width: 500px;
  }
}
</style>
