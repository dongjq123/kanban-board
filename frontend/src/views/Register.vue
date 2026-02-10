/**
 * 注册页面组件
 * 
 * 提供用户注册功能
 * 
 * 需求：1.1-1.6
 */
<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="username"
            type="text"
            class="input"
            placeholder="请输入用户名（3-50 字符）"
            required
            minlength="3"
            maxlength="50"
            :disabled="loading"
          />
        </div>
        
        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="input"
            placeholder="请输入邮箱地址"
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
            placeholder="请输入密码（至少 8 位）"
            required
            minlength="8"
            :disabled="loading"
          />
        </div>
        
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      
      <div class="auth-footer">
        <p>已有账户？<router-link to="/login">立即登录</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from 'vue-toastification'

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      loading: false
    }
  },
  setup() {
    const toast = useToast()
    return { toast }
  },
  methods: {
    async handleRegister() {
      // 验证输入
      if (!this.username || !this.email || !this.password) {
        this.toast.error('请填写所有字段')
        return
      }
      
      if (this.username.length < 3) {
        this.toast.error('用户名长度至少为 3 个字符')
        return
      }
      
      if (this.password.length < 8) {
        this.toast.error('密码长度至少为 8 个字符')
        return
      }
      
      this.loading = true
      
      try {
        // 调用 Vuex action 进行注册
        await this.$store.dispatch('auth/register', {
          username: this.username,
          email: this.email,
          password: this.password
        })
        
        this.toast.success('注册成功！请登录')
        
        // 注册成功后跳转到登录页
        this.$router.push('/login')
      } catch (error) {
        // 错误已经在 axios 拦截器中显示 Toast
        console.error('注册失败:', error)
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
