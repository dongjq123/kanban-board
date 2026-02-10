<!--
  CardDetail 模态框组件
  
  功能：
  - 显示卡片完整信息（标题、描述、截止日期、标签）
  - 实现编辑卡片标题功能
  - 实现添加/编辑描述功能
  - 实现添加/编辑截止日期功能
  - 实现添加/编辑标签功能
  - 实现删除卡片功能
  
  需求：3.4, 3.5, 3.7, 3.8, 3.9
-->
<template>
  <!-- 模态框遮罩层 -->
  <div v-if="isVisible" class="modal-overlay" @click.self="handleClose">
    <div class="modal-container">
      <!-- 模态框头部 -->
      <div class="modal-header">
        <!-- 卡片标题（可编辑） -->
        <div class="title-section">
          <span class="title-icon">📋</span>
          <div class="title-content">
            <h2 
              v-if="!isEditingTitle" 
              class="card-title"
              @click="startEditTitle"
              title="点击编辑标题"
            >
              {{ localCard.title }}
            </h2>
            <textarea
              v-else
              v-model="editedTitle"
              class="input title-input"
              @blur="saveTitle"
              @keyup.enter.exact="saveTitle"
              @keyup.esc="cancelEditTitle"
              ref="titleInput"
              rows="2"
            ></textarea>
            <p class="list-info">在列表 <span class="list-name">{{ listName }}</span> 中</p>
          </div>
        </div>
        
        <!-- 关闭按钮 -->
        <button 
          class="btn-close" 
          @click="handleClose"
          title="关闭"
          :disabled="loading"
        >
          ×
        </button>
      </div>

      <!-- 模态框主体 -->
      <div class="modal-body">
        <!-- 左侧：主要内容 -->
        <div class="main-content">
          <!-- 描述 -->
          <div class="section">
            <div class="section-header">
              <span class="section-icon">📝</span>
              <h3 class="section-title">描述</h3>
            </div>
            
            <div v-if="!isEditingDescription && !localCard.description" class="empty-state">
              <button 
                class="btn-add-description" 
                @click="startEditDescription"
                :disabled="loading"
              >
                添加更详细的描述...
              </button>
            </div>
            
            <div v-else-if="!isEditingDescription" class="description-display">
              <p class="description-text">{{ localCard.description }}</p>
              <button 
                class="btn-edit" 
                @click="startEditDescription"
                :disabled="loading"
              >
                编辑
              </button>
            </div>
            
            <div v-else class="description-edit">
              <textarea
                v-model="editedDescription"
                class="textarea description-input"
                placeholder="添加更详细的描述..."
                @keyup.esc="cancelEditDescription"
                ref="descriptionInput"
                rows="6"
              ></textarea>
              <div class="form-actions">
                <button 
                  class="btn-save" 
                  @click="saveDescription"
                  :disabled="loading"
                >
                  保存
                </button>
                <button 
                  class="btn-cancel" 
                  @click="cancelEditDescription"
                  :disabled="loading"
                >
                  取消
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：操作和元数据 -->
        <div class="sidebar">
          <!-- 添加到卡片 -->
          <div class="sidebar-section">
            <h4 class="sidebar-title">添加到卡片</h4>
            
            <!-- 截止日期 -->
            <div class="action-item">
              <span class="action-icon">📅</span>
              <div class="action-content">
                <label class="action-label">截止日期</label>
                <input
                  v-model="editedDueDate"
                  type="date"
                  class="input date-input"
                  @change="saveDueDate"
                  :disabled="loading"
                />
                <button 
                  v-if="localCard.due_date"
                  class="btn-clear-date"
                  @click="clearDueDate"
                  :disabled="loading"
                  title="清除截止日期"
                >
                  清除
                </button>
              </div>
            </div>
            
            <!-- 标签 -->
            <div class="action-item">
              <span class="action-icon">🏷️</span>
              <div class="action-content">
                <label class="action-label">标签</label>
                
                <!-- 已有标签 -->
                <div v-if="localCard.tags && localCard.tags.length > 0" class="tags-list">
                  <span 
                    v-for="(tag, index) in localCard.tags" 
                    :key="index" 
                    class="tag"
                  >
                    {{ tag }}
                    <button 
                      class="btn-remove-tag"
                      @click="removeTag(index)"
                      :disabled="loading"
                      title="移除标签"
                    >
                      ×
                    </button>
                  </span>
                </div>
                
                <!-- 添加标签 -->
                <div class="add-tag-form">
                  <input
                    v-model="newTag"
                    type="text"
                    class="input tag-input"
                    placeholder="添加标签..."
                    @keyup.enter="addTag"
                    @keyup.esc="newTag = ''"
                    :disabled="loading"
                  />
                  <button 
                    class="btn-add-tag" 
                    @click="addTag"
                    :disabled="!newTag.trim() || loading"
                  >
                    添加
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 操作 -->
          <div class="sidebar-section">
            <h4 class="sidebar-title">操作</h4>
            
            <!-- 删除卡片 -->
            <button 
              class="btn-delete-card" 
              @click="handleDelete"
              :disabled="loading"
            >
              <span class="action-icon">🗑️</span>
              删除卡片
            </button>
          </div>
        </div>
      </div>

      <!-- 加载指示器 -->
      <div v-if="loading" class="loading-overlay">
        <div class="spinner"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'CardDetail',
  
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    card: {
      type: Object,
      default: null
    },
    listName: {
      type: String,
      default: '未知列表'
    }
  },
  
  data() {
    return {
      localCard: null,
      isEditingTitle: false,
      editedTitle: '',
      isEditingDescription: false,
      editedDescription: '',
      editedDueDate: '',
      newTag: ''
    }
  },
  
  computed: {
    ...mapState('cards', {
      loading: state => state.loading
    }),
    
    isVisible() {
      return this.visible && this.localCard
    }
  },
  
  methods: {
    ...mapActions('cards', ['updateCard', 'deleteCard']),
    
    /**
     * 初始化本地卡片数据
     */
    initLocalCard() {
      if (this.card) {
        this.localCard = { ...this.card }
        this.editedDueDate = this.localCard.due_date || ''
      }
    },
    
    /**
     * 开始编辑标题
     * 需求：3.4
     */
    startEditTitle() {
      this.isEditingTitle = true
      this.editedTitle = this.localCard.title
      
      this.$nextTick(() => {
        this.$refs.titleInput?.focus()
        this.$refs.titleInput?.select()
      })
    },
    
    /**
     * 保存标题
     * 需求：3.4
     */
    async saveTitle() {
      const title = this.editedTitle.trim()
      
      if (!title || title === this.localCard.title) {
        this.cancelEditTitle()
        return
      }
      
      try {
        await this.updateCard({
          id: this.localCard.id,
          data: { title }
        })
        this.localCard.title = title
        this.isEditingTitle = false
      } catch (error) {
        console.error('更新卡片标题失败:', error)
      }
    },
    
    /**
     * 取消编辑标题
     */
    cancelEditTitle() {
      this.isEditingTitle = false
      this.editedTitle = ''
    },
    
    /**
     * 开始编辑描述
     * 需求：3.7
     */
    startEditDescription() {
      this.isEditingDescription = true
      this.editedDescription = this.localCard.description || ''
      
      this.$nextTick(() => {
        this.$refs.descriptionInput?.focus()
      })
    },
    
    /**
     * 保存描述
     * 需求：3.7
     */
    async saveDescription() {
      const description = this.editedDescription.trim()
      
      try {
        await this.updateCard({
          id: this.localCard.id,
          data: { description: description || null }
        })
        this.localCard.description = description || null
        this.isEditingDescription = false
      } catch (error) {
        console.error('更新卡片描述失败:', error)
      }
    },
    
    /**
     * 取消编辑描述
     */
    cancelEditDescription() {
      this.isEditingDescription = false
      this.editedDescription = ''
    },
    
    /**
     * 保存截止日期
     * 需求：3.8
     */
    async saveDueDate() {
      const dueDate = this.editedDueDate || null
      
      if (dueDate === this.localCard.due_date) {
        return
      }
      
      try {
        await this.updateCard({
          id: this.localCard.id,
          data: { due_date: dueDate }
        })
        this.localCard.due_date = dueDate
      } catch (error) {
        console.error('更新截止日期失败:', error)
        // 恢复原值
        this.editedDueDate = this.localCard.due_date || ''
      }
    },
    
    /**
     * 清除截止日期
     * 需求：3.8
     */
    async clearDueDate() {
      try {
        await this.updateCard({
          id: this.localCard.id,
          data: { due_date: null }
        })
        this.localCard.due_date = null
        this.editedDueDate = ''
      } catch (error) {
        console.error('清除截止日期失败:', error)
      }
    },
    
    /**
     * 添加标签
     * 需求：3.9
     */
    async addTag() {
      const tag = this.newTag.trim()
      
      if (!tag) {
        return
      }
      
      // 检查标签是否已存在
      if (this.localCard.tags && this.localCard.tags.includes(tag)) {
        alert('该标签已存在')
        this.newTag = ''
        return
      }
      
      try {
        const tags = [...(this.localCard.tags || []), tag]
        await this.updateCard({
          id: this.localCard.id,
          data: { tags }
        })
        this.localCard.tags = tags
        this.newTag = ''
      } catch (error) {
        console.error('添加标签失败:', error)
      }
    },
    
    /**
     * 移除标签
     * 需求：3.9
     */
    async removeTag(index) {
      try {
        const tags = [...this.localCard.tags]
        tags.splice(index, 1)
        
        await this.updateCard({
          id: this.localCard.id,
          data: { tags }
        })
        this.localCard.tags = tags
      } catch (error) {
        console.error('移除标签失败:', error)
      }
    },
    
    /**
     * 删除卡片
     * 需求：3.5
     */
    async handleDelete() {
      if (!confirm(`确定要删除卡片"${this.localCard.title}"吗？\n\n此操作无法撤销。`)) {
        return
      }
      
      try {
        await this.deleteCard({
          cardId: this.localCard.id,
          listId: this.localCard.list_id
        })
        this.handleClose()
      } catch (error) {
        console.error('删除卡片失败:', error)
      }
    },
    
    /**
     * 关闭模态框
     */
    handleClose() {
      if (this.loading) {
        return
      }
      
      // 重置编辑状态
      this.isEditingTitle = false
      this.isEditingDescription = false
      this.editedTitle = ''
      this.editedDescription = ''
      this.newTag = ''
      
      this.$emit('close')
    }
  },
  
  watch: {
    /**
     * 监听 card prop 变化，更新本地数据
     */
    card: {
      handler(newCard) {
        if (newCard) {
          this.initLocalCard()
        }
      },
      immediate: true,
      deep: true
    },
    
    /**
     * 监听 visible prop 变化
     */
    visible(newVal) {
      if (newVal) {
        this.initLocalCard()
        // 阻止背景滚动
        document.body.style.overflow = 'hidden'
      } else {
        // 恢复背景滚动
        document.body.style.overflow = ''
      }
    }
  },
  
  /**
   * 组件销毁时恢复背景滚动
   */
  beforeUnmount() {
    document.body.style.overflow = ''
  }
}
</script>

<style scoped>
/* 模态框遮罩层 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 1000;
  overflow-y: auto;
  padding: 48px 0;
}

/* 模态框容器 */
.modal-container {
  background-color: #f4f5f7;
  border-radius: 8px;
  width: 90%;
  max-width: 768px;
  min-height: 400px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  position: relative;
  margin: 0 auto;
}

/* 模态框头部 */
.modal-header {
  padding: 20px 24px 16px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.title-section {
  flex: 1;
  display: flex;
  gap: 12px;
  min-width: 0;
}

.title-icon {
  font-size: 24px;
  flex-shrink: 0;
  margin-top: 4px;
}

.title-content {
  flex: 1;
  min-width: 0;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  color: #172b4d;
  margin: 0 0 8px 0;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  word-wrap: break-word;
  line-height: 1.4;
}

.card-title:hover {
  background-color: rgba(9, 30, 66, 0.08);
}

.title-input {
  /* Component-specific overrides for title input */
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
  /* Base input styles are inherited from .input class */
}

.list-info {
  font-size: 14px;
  color: #5e6c84;
  margin: 0;
  padding-left: 12px;
}

.list-name {
  font-weight: 500;
  color: #172b4d;
}

.btn-close {
  background-color: transparent;
  color: #5e6c84;
  border: none;
  border-radius: 4px;
  width: 32px;
  height: 32px;
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover:not(:disabled) {
  background-color: rgba(9, 30, 66, 0.08);
  color: #172b4d;
}

.btn-close:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 模态框主体 */
.modal-body {
  display: flex;
  gap: 24px;
  padding: 0 24px 24px;
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  min-width: 0;
}

.section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.section-icon {
  font-size: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #172b4d;
  margin: 0;
}

/* 描述 */
.empty-state {
  margin-bottom: 12px;
}

.btn-add-description {
  width: 100%;
  background-color: rgba(9, 30, 66, 0.04);
  color: #5e6c84;
  border: none;
  border-radius: 4px;
  padding: 12px;
  font-size: 14px;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-add-description:hover:not(:disabled) {
  background-color: rgba(9, 30, 66, 0.08);
  color: #172b4d;
}

.btn-add-description:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.description-display {
  background-color: white;
  border-radius: 4px;
  padding: 12px;
  position: relative;
}

.description-text {
  font-size: 14px;
  color: #172b4d;
  margin: 0 0 12px 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  line-height: 1.6;
}

.btn-edit {
  background-color: rgba(9, 30, 66, 0.04);
  color: #5e6c84;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-edit:hover:not(:disabled) {
  background-color: rgba(9, 30, 66, 0.08);
  color: #172b4d;
}

.btn-edit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.description-edit {
  background-color: white;
  border-radius: 4px;
  padding: 12px;
}

.description-input {
  /* Component-specific overrides for description input */
  min-height: 120px;
  margin-bottom: 12px;
  /* Base textarea styles are inherited from .textarea class */
}

.form-actions {
  display: flex;
  gap: 8px;
}

.btn-save,
.btn-cancel {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-save {
  background-color: #0079bf;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background-color: #026aa7;
}

.btn-save:disabled {
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

/* 侧边栏 */
.sidebar {
  width: 200px;
  flex-shrink: 0;
}

.sidebar-section {
  margin-bottom: 24px;
}

.sidebar-title {
  font-size: 12px;
  font-weight: 600;
  color: #5e6c84;
  text-transform: uppercase;
  margin: 0 0 8px 0;
  letter-spacing: 0.5px;
}

.action-item {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.action-icon {
  font-size: 16px;
  flex-shrink: 0;
  margin-top: 2px;
}

.action-content {
  flex: 1;
  min-width: 0;
}

.action-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #172b4d;
  margin-bottom: 8px;
}

.date-input {
  /* Component-specific overrides for date input */
  margin-bottom: 8px;
  /* Base input styles are inherited from .input class */
}

.btn-clear-date {
  width: 100%;
  background-color: #f4f5f7;
  color: #5e6c84;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 13px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-clear-date:hover:not(:disabled) {
  background-color: #e4e6ea;
  color: #172b4d;
}

.btn-clear-date:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 标签 */
.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: white;
  background-color: #0079bf;
  padding: 4px 8px;
  border-radius: 3px;
  font-weight: 500;
}

.btn-remove-tag {
  background-color: transparent;
  color: white;
  border: none;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  margin-left: 2px;
  transition: opacity 0.2s;
}

.btn-remove-tag:hover:not(:disabled) {
  opacity: 0.8;
}

.btn-remove-tag:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.add-tag-form {
  display: flex;
  gap: 6px;
}

.tag-input {
  /* Component-specific overrides for tag input */
  flex: 1;
  font-size: 13px;
  /* Base input styles are inherited from .input class */
}

.btn-add-tag {
  background-color: #0079bf;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.btn-add-tag:hover:not(:disabled) {
  background-color: #026aa7;
}

.btn-add-tag:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 删除卡片按钮 */
.btn-delete-card {
  width: 100%;
  background-color: #eb5a46;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-delete-card:hover:not(:disabled) {
  background-color: #cf513d;
}

.btn-delete-card:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 加载指示器 */
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
  border-radius: 8px;
  z-index: 10;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f4f5f7;
  border-top-color: #0079bf;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 响应式设计 - 移动端媒体查询 */
/* 需求：5.1, 5.2 - 移动设备适配 */
@media (max-width: 767px) {
  .modal-overlay {
    padding: 0;
    align-items: stretch;
  }
  
  .modal-container {
    width: 100%;
    max-width: 100%;
    min-height: 100vh;
    border-radius: 0;
  }
  
  /* 调整头部 */
  .modal-header {
    padding: var(--spacing-md) var(--spacing-md) var(--spacing-sm);
  }
  
  .title-icon {
    font-size: 20px;
  }
  
  .card-title {
    font-size: var(--font-size-lg);
    padding: var(--spacing-xs) var(--spacing-sm);
  }
  
  .title-input {
    font-size: var(--font-size-lg);
  }
  
  .list-info {
    font-size: var(--font-size-xs);
  }
  
  .btn-close {
    width: 28px;
    height: 28px;
    font-size: 24px;
  }
  
  /* 调整主体布局 - 垂直堆叠 */
  .modal-body {
    flex-direction: column;
    padding: 0 var(--spacing-md) var(--spacing-md);
    gap: var(--spacing-md);
  }
  
  /* 主要内容区域 */
  .section {
    margin-bottom: var(--spacing-md);
  }
  
  .section-icon {
    font-size: 18px;
  }
  
  .section-title {
    font-size: var(--font-size-base);
  }
  
  .description-input {
    min-height: 100px;
    font-size: var(--font-size-sm);
  }
  
  /* 侧边栏 */
  .sidebar {
    width: 100%;
  }
  
  .action-item {
    margin-bottom: var(--spacing-sm);
  }
  
  .action-icon {
    font-size: 14px;
  }
  
  .action-label {
    font-size: var(--font-size-sm);
    margin-bottom: var(--spacing-xs);
  }
  
  /* 调整按钮尺寸 */
  .btn-save,
  .btn-cancel {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-sm);
  }
  
  .btn-add-tag,
  .btn-clear-date {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-xs);
  }
  
  .tag-input {
    font-size: var(--font-size-xs);
  }
  
  .tag {
    font-size: 11px;
    padding: 3px var(--spacing-xs);
  }
}

/* 响应式设计 - 平板端媒体查询 */
/* 需求：5.1 - 平板设备适配 */
@media (min-width: 768px) and (max-width: 1023px) {
  .modal-container {
    width: 90%;
    max-width: 700px;
  }
  
  /* 调整主体布局 - 保持水平布局但调整间距 */
  .modal-body {
    gap: var(--spacing-lg);
  }
  
  /* 主要内容区域 */
  .main-content {
    flex: 1;
    min-width: 0;
  }
  
  /* 侧边栏 */
  .sidebar {
    width: 200px;
  }
}

/* 响应式设计 - 桌面端媒体查询 */
/* 需求：5.1 - 桌面设备适配 */
@media (min-width: 1024px) {
  .modal-overlay {
    padding: 64px 0;
  }
  
  .modal-container {
    width: 85%;
    max-width: 800px;
  }
  
  /* 调整头部 */
  .modal-header {
    padding: var(--spacing-xl) var(--spacing-2xl) var(--spacing-lg);
  }
  
  .title-icon {
    font-size: 28px;
  }
  
  .card-title {
    font-size: var(--font-size-2xl);
    padding: var(--spacing-sm) var(--spacing-md);
  }
  
  .title-input {
    font-size: var(--font-size-2xl);
  }
  
  .list-info {
    font-size: var(--font-size-base);
    padding-left: var(--spacing-md);
  }
  
  /* 调整主体布局 */
  .modal-body {
    gap: var(--spacing-xl);
    padding: 0 var(--spacing-2xl) var(--spacing-2xl);
  }
  
  /* 主要内容区域 */
  .section {
    margin-bottom: var(--spacing-xl);
  }
  
  .section-icon {
    font-size: 24px;
  }
  
  .section-title {
    font-size: var(--font-size-lg);
  }
  
  .description-text {
    font-size: var(--font-size-base);
    line-height: 1.7;
  }
  
  .description-input {
    min-height: 140px;
    font-size: var(--font-size-base);
  }
  
  /* 侧边栏 */
  .sidebar {
    width: 220px;
  }
  
  .sidebar-title {
    font-size: var(--font-size-sm);
    margin-bottom: var(--spacing-sm);
  }
  
  .action-item {
    margin-bottom: var(--spacing-lg);
  }
  
  .action-icon {
    font-size: 18px;
  }
  
  .action-label {
    font-size: var(--font-size-base);
    margin-bottom: var(--spacing-sm);
  }
  
  /* 调整按钮尺寸 */
  .btn-save,
  .btn-cancel {
    padding: var(--spacing-sm) var(--spacing-lg);
    font-size: var(--font-size-base);
  }
  
  .btn-add-tag,
  .btn-clear-date {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-sm);
  }
  
  .tag-input {
    font-size: var(--font-size-sm);
  }
  
  .tag {
    font-size: var(--font-size-sm);
    padding: var(--spacing-xs) var(--spacing-sm);
  }
}

/* 响应式设计 - 大屏媒体查询 */
/* 需求：5.1 - 大屏设备适配 */
@media (min-width: 1440px) {
  .modal-overlay {
    padding: 80px 0;
  }
  
  .modal-container {
    width: 80%;
    max-width: 900px;
  }
  
  /* 调整头部 */
  .modal-header {
    padding: var(--spacing-2xl) var(--spacing-3xl) var(--spacing-xl);
  }
  
  .title-icon {
    font-size: 32px;
  }
  
  .card-title {
    font-size: var(--font-size-3xl);
    padding: var(--spacing-md) var(--spacing-lg);
  }
  
  .title-input {
    font-size: var(--font-size-3xl);
  }
  
  .list-info {
    font-size: var(--font-size-lg);
    padding-left: var(--spacing-lg);
  }
  
  .btn-close {
    width: 40px;
    height: 40px;
    font-size: 32px;
  }
  
  /* 调整主体布局 */
  .modal-body {
    gap: var(--spacing-2xl);
    padding: 0 var(--spacing-3xl) var(--spacing-3xl);
  }
  
  /* 主要内容区域 */
  .section {
    margin-bottom: var(--spacing-2xl);
  }
  
  .section-icon {
    font-size: 28px;
  }
  
  .section-title {
    font-size: var(--font-size-xl);
  }
  
  .description-display,
  .description-edit {
    padding: var(--spacing-lg);
  }
  
  .description-text {
    font-size: var(--font-size-lg);
    line-height: 1.8;
    margin-bottom: var(--spacing-lg);
  }
  
  .description-input {
    min-height: 160px;
    font-size: var(--font-size-lg);
  }
  
  .btn-add-description {
    padding: var(--spacing-lg);
    font-size: var(--font-size-base);
  }
  
  .btn-edit {
    padding: var(--spacing-sm) var(--spacing-lg);
    font-size: var(--font-size-base);
  }
  
  /* 侧边栏 */
  .sidebar {
    width: 260px;
  }
  
  .sidebar-section {
    margin-bottom: var(--spacing-2xl);
  }
  
  .sidebar-title {
    font-size: var(--font-size-base);
    margin-bottom: var(--spacing-md);
  }
  
  .action-item {
    margin-bottom: var(--spacing-xl);
  }
  
  .action-icon {
    font-size: 20px;
  }
  
  .action-label {
    font-size: var(--font-size-lg);
    margin-bottom: var(--spacing-md);
  }
  
  /* 调整按钮尺寸 */
  .btn-save,
  .btn-cancel {
    padding: var(--spacing-md) var(--spacing-xl);
    font-size: var(--font-size-lg);
  }
  
  .btn-add-tag,
  .btn-clear-date {
    padding: var(--spacing-sm) var(--spacing-lg);
    font-size: var(--font-size-base);
  }
  
  .tag-input {
    font-size: var(--font-size-base);
    padding: var(--spacing-sm) var(--spacing-md);
  }
  
  .tag {
    font-size: var(--font-size-base);
    padding: var(--spacing-sm) var(--spacing-md);
  }
  
  .btn-delete-card {
    padding: var(--spacing-md) var(--spacing-lg);
    font-size: var(--font-size-base);
  }
}
</style>
