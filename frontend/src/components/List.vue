<!--
  List 组件
  
  功能：
  - 显示列表名称和其下的所有卡片
  - 实现编辑列表名称功能
  - 实现删除列表功能
  - 显示"添加卡片"按钮
  - 集成卡片拖拽功能（同列表内和跨列表）
  - 使用 Vue.Draggable 实现拖拽
  
  需求：2.3, 2.4, 2.8, 3.2, 4.1, 4.3
-->
<template>
  <div class="list" :data-list-id="list.id">
    <!-- 列表头部 -->
    <div class="list-header">
      <!-- 列表名称（可编辑） -->
      <div class="list-title-section">
        <h3 
          v-if="!isEditingName" 
          class="list-title"
          @click="startEditName"
          title="点击编辑列表名称"
        >
          {{ list.name }}
        </h3>
        <input
          v-else
          v-model="editedName"
          type="text"
          class="input list-title-input"
          @blur="saveName"
          @keyup.enter="saveName"
          @keyup.esc="cancelEditName"
          ref="nameInput"
        />
      </div>
      
      <!-- 删除按钮 -->
      <button 
        class="btn-delete" 
        @click="handleDelete"
        title="删除列表"
        :disabled="loading"
      >
        ×
      </button>
    </div>

    <!-- 卡片列表 -->
    <div class="cards-container">
      <!-- 使用 vuedraggable 实现卡片拖拽，配合 transition-group 实现过渡动画 -->
      <draggable
        v-model="sortedCards"
        :animation="200"
        ghost-class="card-ghost"
        drag-class="card-drag"
        group="cards"
        @end="handleCardDragEnd"
        class="cards-wrapper"
        item-key="id"
        tag="transition-group"
        :component-data="{
          name: 'list',
          type: 'transition'
        }"
      >
        <template #item="{ element: card }">
          <Card 
            :key="card.id" 
            :card="card"
            @click="handleCardClick(card)"
          />
        </template>
      </draggable>
    </div>

    <!-- 添加卡片 -->
    <div class="add-card-container">
      <div v-if="!showAddCardForm" class="add-card-button-wrapper">
        <button 
          class="btn-add-card" 
          @click="showAddCardForm = true"
          :disabled="loading"
        >
          + 添加卡片
        </button>
      </div>
      
      <div v-else class="add-card-form">
        <textarea
          v-model="newCardTitle"
          placeholder="输入卡片标题..."
          class="textarea card-title-input"
          @keyup.enter.exact="handleCreateCard"
          @keyup.esc="cancelAddCard"
          ref="cardTitleInput"
          rows="3"
        ></textarea>
        <div class="form-actions">
          <button 
            class="btn-submit" 
            @click="handleCreateCard"
            :disabled="!newCardTitle.trim() || loading"
          >
            添加卡片
          </button>
          <button 
            class="btn-cancel" 
            @click="cancelAddCard"
            :disabled="loading"
          >
            取消
          </button>
        </div>
      </div>
    </div>
    
    <!-- 卡片详情模态框 -->
    <CardDetail
      :visible="showCardDetail"
      :card="selectedCard"
      :listName="list.name"
      @close="closeCardDetail"
    />
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'
import draggable from 'vuedraggable'
import Card from './Card.vue'
import CardDetail from './CardDetail.vue'

export default {
  name: 'List',
  
  components: {
    draggable,
    Card,
    CardDetail
  },
  
  props: {
    list: {
      type: Object,
      required: true
    }
  },
  
  data() {
    return {
      isEditingName: false,
      editedName: '',
      showAddCardForm: false,
      newCardTitle: '',
      showCardDetail: false,
      selectedCard: null
    }
  },
  
  computed: {
    ...mapState('lists', {
      listsLoading: state => state.loading
    }),
    ...mapState('cards', {
      cardsLoading: state => state.loading
    }),
    ...mapGetters('cards', ['getCardsByListId']),
    
    // 合并加载状态
    loading() {
      return this.listsLoading || this.cardsLoading
    },
    
    // 获取当前列表的卡片
    cards() {
      return this.getCardsByListId(this.list.id)
    },
    
    // 按位置排序的卡片
    sortedCards: {
      get() {
        // 确保 cards 是数组，防止扩展运算符错误
        const cards = Array.isArray(this.cards) ? this.cards : []
        return [...cards].sort((a, b) => a.position - b.position)
      },
      set(value) {
        // 当拖拽改变顺序时，更新 store
        // 这里只是临时更新，实际的持久化在 handleCardDragEnd 中完成
        const listId = this.list.id
        this.$store.commit('cards/setCards', { listId, cards: value })
      }
    }
  },
  
  methods: {
    ...mapActions('lists', ['updateList', 'deleteList']),
    ...mapActions('cards', ['fetchCards', 'createCard', 'moveCard']),
    
    /**
     * 开始编辑列表名称
     * 需求：2.3
     */
    startEditName() {
      this.isEditingName = true
      this.editedName = this.list.name
      
      this.$nextTick(() => {
        this.$refs.nameInput?.focus()
        this.$refs.nameInput?.select()
      })
    },
    
    /**
     * 保存列表名称
     * 需求：2.3
     */
    async saveName() {
      const name = this.editedName.trim()
      
      if (!name || name === this.list.name) {
        this.cancelEditName()
        return
      }
      
      try {
        await this.updateList({
          id: this.list.id,
          data: { name }
        })
        this.isEditingName = false
      } catch (error) {
        console.error('更新列表名称失败:', error)
        // 错误已经在 store 中处理
      }
    },
    
    /**
     * 取消编辑列表名称
     */
    cancelEditName() {
      this.isEditingName = false
      this.editedName = ''
    },
    
    /**
     * 删除列表
     * 需求：2.4
     */
    async handleDelete() {
      if (!confirm(`确定要删除列表"${this.list.name}"吗？\n\n此操作将同时删除该列表下的所有卡片，且无法撤销。`)) {
        return
      }
      
      try {
        await this.deleteList(this.list.id)
      } catch (error) {
        console.error('删除列表失败:', error)
        // 错误已经在 store 中处理
      }
    },
    
    /**
     * 创建新卡片
     * 需求：3.2
     */
    async handleCreateCard() {
      const title = this.newCardTitle.trim()
      
      if (!title) {
        return
      }
      
      try {
        // 计算新卡片的位置（在最后）
        const position = this.cards.length
        
        await this.createCard({
          listId: this.list.id,
          data: { title, position }
        })
        
        this.newCardTitle = ''
        this.showAddCardForm = false
      } catch (error) {
        console.error('创建卡片失败:', error)
        // 错误已经在 store 中处理
      }
    },
    
    /**
     * 取消添加卡片
     */
    cancelAddCard() {
      this.showAddCardForm = false
      this.newCardTitle = ''
    },
    
    /**
     * 处理卡片拖拽结束
     * 需求：4.1, 4.2, 4.3, 4.4
     */
    async handleCardDragEnd(event) {
      const { oldIndex, newIndex, from, to } = event
      
      // 获取被移动的卡片
      const movedCard = this.sortedCards[newIndex]
      
      // 确定源列表和目标列表的 ID
      const oldListId = parseInt(from.closest('.list').dataset.listId)
      const newListId = parseInt(to.closest('.list').dataset.listId)
      
      // 如果位置和列表都没有变化，不需要更新
      if (oldIndex === newIndex && oldListId === newListId) {
        return
      }
      
      try {
        // 移动卡片到新位置
        await this.moveCard({
          cardId: movedCard.id,
          oldListId,
          newListId,
          position: newIndex
        })
        
        // 如果是同列表内移动，更新所有受影响的卡片位置
        if (oldListId === newListId) {
          const updates = this.sortedCards.map((card, index) => {
            if (card.position !== index) {
              return this.moveCard({
                cardId: card.id,
                oldListId,
                newListId,
                position: index
              })
            }
            return null
          }).filter(Boolean)
          
          // 等待所有更新完成
          if (updates.length > 0) {
            await Promise.all(updates)
          }
        }
      } catch (error) {
        console.error('移动卡片失败:', error)
        // 如果移动失败，重新获取卡片以恢复正确的顺序
        await this.fetchCards(this.list.id)
      }
    },
    
    /**
     * 处理卡片点击
     * 需求：3.6
     */
    handleCardClick(card) {
      // 设置当前卡片并显示详情模态框
      this.selectedCard = card
      this.showCardDetail = true
      this.$store.commit('cards/setCurrentCard', card)
    },
    
    /**
     * 关闭卡片详情模态框
     */
    closeCardDetail() {
      this.showCardDetail = false
      this.selectedCard = null
    }
  },
  
  /**
   * 组件挂载时获取卡片
   * 需求：3.1
   */
  mounted() {
    this.fetchCards(this.list.id)
  },
  
  /**
   * 监听添加卡片表单显示状态，自动聚焦输入框
   */
  watch: {
    showAddCardForm(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.$refs.cardTitleInput?.focus()
        })
      }
    }
  }
}
</script>

<style scoped>
/**
 * List Component Styles - Modernized
 * 
 * 现代化列表组件样式
 * 使用设计令牌确保一致性
 * 
 * 需求：1.2, 1.3, 2.5, 3.4
 */

/* ========================================
   列表容器 (List Container)
   ======================================== */

.list {
  flex: 0 0 320px;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 200px);
  background: var(--color-bg-primary);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-base);
  transition: box-shadow var(--transition-base);
}

/* 列表 hover 状态的阴影增强 */
.list:hover {
  box-shadow: var(--shadow-md);
}

/* 添加 data-list-id 属性用于拖拽识别 */
.list::before {
  content: attr(data-list-id);
  display: none;
}


/* ========================================
   列表头部 (List Header)
   ======================================== */

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--color-gray-200);
  cursor: grab;
}

.list-header:active {
  cursor: grabbing;
}

.list-title-section {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

/* 列表标题样式 */
.list-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background-color var(--transition-fast);
  word-wrap: break-word;
  line-height: var(--line-height-tight);
}

.list-title:hover {
  background-color: var(--color-gray-100);
}

/* 列表标题输入框 */
.list-title-input {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-lg);
}

/* 计数徽章（如果需要添加） */
.list__count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 var(--spacing-sm);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  background: var(--color-gray-100);
  border-radius: var(--radius-full);
}

/* 删除按钮 */
.btn-delete {
  background-color: transparent;
  color: var(--color-text-secondary);
  border: none;
  border-radius: var(--radius-sm);
  width: 32px;
  height: 32px;
  min-width: 32px;
  min-height: 32px;
  font-size: var(--font-size-2xl);
  line-height: 1;
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-delete:hover:not(:disabled) {
  background-color: var(--color-gray-100);
  color: var(--color-text-primary);
}

.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}


/* ========================================
   卡片容器 (Cards Container)
   ======================================== */

.cards-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: var(--spacing-md);
  min-height: 20px;
}

.cards-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  min-height: 20px;
}

/* 自定义滚动条样式 */
.cards-container::-webkit-scrollbar {
  width: 6px;
}

.cards-container::-webkit-scrollbar-track {
  background: transparent;
}

.cards-container::-webkit-scrollbar-thumb {
  background: var(--color-gray-300);
  border-radius: var(--radius-full);
  transition: background var(--transition-fast);
}

.cards-container::-webkit-scrollbar-thumb:hover {
  background: var(--color-gray-400);
}

/* 卡片拖拽样式 */
.card-ghost {
  opacity: 0.5;
  background-color: var(--color-gray-200);
}

.card-drag {
  opacity: 0.8;
  transform: rotate(3deg);
  cursor: grabbing;
}


/* ========================================
   添加卡片区域 (Add Card Section)
   ======================================== */

.add-card-container {
  padding: var(--spacing-md);
  border-top: 1px solid var(--color-gray-200);
}

.add-card-button-wrapper {
  padding: var(--spacing-xs);
}

.btn-add-card {
  width: 100%;
  background-color: transparent;
  color: var(--color-text-secondary);
  border: none;
  border-radius: var(--radius-base);
  padding: var(--spacing-sm);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  text-align: left;
  transition: all var(--transition-fast);
  min-height: 44px;
}

.btn-add-card:hover:not(:disabled) {
  background-color: var(--color-gray-100);
  color: var(--color-text-primary);
}

.btn-add-card:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 添加卡片表单 */
.add-card-form {
  background-color: var(--color-bg-primary);
  border-radius: var(--radius-base);
  padding: var(--spacing-sm);
  box-shadow: var(--shadow-sm);
}

.card-title-input {
  min-height: 60px;
  margin-bottom: var(--spacing-sm);
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
  box-shadow: var(--shadow-sm);
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


/* ========================================
   响应式设计 (Responsive Design)
   ======================================== */

/* 移动设备 - 需求：5.1, 5.2 */
@media (max-width: 767px) {
  .list {
    /* 移动端列表占满宽度，垂直堆叠 */
    flex: 1 1 auto;
    width: 100%;
    max-height: 400px;
    min-height: 300px;
  }
  
  /* 调整列表头部 */
  .list-header {
    padding: var(--spacing-sm) var(--spacing-md);
  }
  
  .list-title {
    font-size: var(--font-size-base);
  }
  
  .list-title-input {
    font-size: var(--font-size-base);
  }
  
  /* 调整卡片容器 */
  .cards-container {
    padding: var(--spacing-sm);
  }
  
  /* 调整添加卡片区域 */
  .add-card-container {
    padding: var(--spacing-sm);
  }
  
  .card-title-input {
    font-size: var(--font-size-sm);
    min-height: 50px;
  }
  
  /* 调整按钮尺寸 */
  .btn-submit,
  .btn-cancel {
    flex: 1;
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-sm);
  }
}

/* 平板设备 */
@media (min-width: 768px) and (max-width: 1023px) {
  .list {
    flex: 0 0 280px;
  }
}

/* 桌面设备 */
@media (min-width: 1024px) {
  .list {
    flex: 0 0 320px;
  }
}

/* 大屏设备 */
@media (min-width: 1440px) {
  .list {
    flex: 0 0 360px;
  }
}
</style>
