/**
 * 主页组件
 * 
 * 显示看板列表
 * 
 * 需求：4.1, 5.2
 */
<template>
  <div class="home">
    <header>
      <h1>Visual Task Board</h1>
      <div class="user-info" v-if="currentUser">
        <span>{{ currentUser.username }}</span>
        <button @click="handleLogout" class="btn-logout">登出</button>
      </div>
    </header>
    <main>
      <BoardList />
    </main>
  </div>
</template>

<script>
import BoardList from '@/components/BoardList.vue'
import { useToast } from 'vue-toastification'

export default {
  name: 'Home',
  components: {
    BoardList
  },
  setup() {
    const toast = useToast()
    return { toast }
  },
  computed: {
    currentUser() {
      return this.$store.getters['auth/currentUser']
    }
  },
  methods: {
    handleLogout() {
      this.$store.dispatch('auth/logout')
      this.toast.success('已登出')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.home {
  width: 100%;
  min-height: 100vh;
}

header {
  background-color: var(--color-primary, #0079bf);
  color: white;
  padding: var(--spacing-md, 12px) var(--spacing-lg, 20px);
  box-shadow: var(--shadow-sm, 0 2px 4px rgba(0, 0, 0, 0.1));
  display: flex;
  justify-content: space-between;
  align-items: center;
}

header h1 {
  font-size: var(--font-size-2xl, 24px);
  font-weight: var(--font-weight-semibold, 600);
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md, 12px);
}

.user-info span {
  font-size: var(--font-size-base, 16px);
  font-weight: var(--font-weight-medium, 500);
}

.btn-logout {
  padding: var(--spacing-xs, 4px) var(--spacing-md, 12px);
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: var(--border-radius-md, 4px);
  font-size: var(--font-size-sm, 14px);
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-logout:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

main {
  padding: var(--spacing-lg, 20px);
}
</style>
