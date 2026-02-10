/**
 * 登录页面组件
 * 
 * 提供用户登录功能
 * 
 * 需求：2.1-2.4
 */
<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="identifier">邮箱或用户名</label>
          <input
            id="identifier"
            v-model="identifier"
            type="text"
            class="input"
            placeholder="请输入邮箱或用户名"
            required
            :disabled="loading"
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="input"
            placeholder="请输入密码"
            required
            :disabled="loading"
          />
        </div>
        
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <div class="auth-footer">
        <p>还没有账户？<router-link to="/register">立即注册</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from 'vue-toastification'

export default {
  name: 'Login',
  data() {
    return {
      identifier: '',
      password: '',
      loading: false
    }
  },
  setup() {
    const toast = useToast()
    return { toast }
  },
  methods: {
    async handleLogin() {
      // 验证输入
      if (!this.identifier || !this.password) {
        this.toast.error('请填写所有字段')
        return
      }
      
      this.loading = true
      
      try {
        // 调用 Vuex action 进行登录
        await this.$store.dispatch('auth/login', {
          identifier: this.identifier,
          password: this.password
        })
        
        this.toast.success('登录成功！')
        
        // 登录成功后重定向
        // 如果有 redirect 参数，跳转到原始目标页面
        // 否则跳转到主页
        const redirect = this.$route.query.redirect || '/'
        this.$router.push(redirect)
      } catch (error) {
        // 错误已经在 axios 拦截器中显示 Toast
        console.error('登录失败:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--color-background, #f5f6f8);
  padding: var(--spacing-lg, 20px);
}

.auth-card {
  background: white;
  border-radius: var(--border-radius-lg, 8px);
  box-shadow: var(--shadow-md, 0 4px 6px rgba(0, 0, 0, 0.1));
  padding: var(--spacing-2xl, 32px);
  width: 100%;
  max-width: 400px;
}

.auth-card h2 {
  margin: 0 0 var(--spacing-xl, 24px) 0;
  font-size: var(--font-size-2xl, 24px);
  font-weight: var(--font-weight-semibold, 600);
  color: var(--color-text-primary, #172b4d);
  text-align: center;
}

.form-group {
  margin-bottom: var(--spacing-lg, 20px);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-xs, 4px);
  font-size: var(--font-size-sm, 14px);
  font-weight: var(--font-weight-medium, 500);
  color: var(--color-text-secondary, #5e6c84);
}

/* Input styles are inherited from .input class in utilities.css */
/* Component-specific overrides can be added here if needed */

.btn-primary {
  width: 100%;
  padding: var(--spacing-md, 12px);
  background-color: var(--color-primary, #0079bf);
  color: white;
  border: none;
  border-radius: var(--border-radius-md, 4px);
  font-size: var(--font-size-base, 16px);
  font-weight: var(--font-weight-medium, 500);
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-primary-dark, #026aa7);
}

.btn-primary:disabled {
  background-color: var(--color-border, #dfe1e6);
  cursor: not-allowed;
}

.auth-footer {
  margin-top: var(--spacing-xl, 24px);
  text-align: center;
  font-size: var(--font-size-sm, 14px);
  color: var(--color-text-secondary, #5e6c84);
}

.auth-footer a {
  color: var(--color-primary, #0079bf);
  text-decoration: none;
  font-weight: var(--font-weight-medium, 500);
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>
