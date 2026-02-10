/**
 * 看板详情页面组件
 * 
 * 显示单个看板的详细信息和列表
 * 
 * 需求：4.2, 5.2
 */
<template>
  <div class="board-detail">
    <Board v-if="boardId" :board-id="boardId" />
  </div>
</template>

<script>
import Board from '@/components/Board.vue'

export default {
  name: 'BoardDetail',
  components: {
    Board
  },
  computed: {
    boardId() {
      return parseInt(this.$route.params.id)
    }
  }
}
</script>

<style scoped>
.board-detail {
  width: 100%;
}
</style>
