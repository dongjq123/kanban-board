<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* 引入基础样式文件 - 按顺序加载以确保正确的样式层叠 */
@import './assets/styles/variables.css';  /* 设计令牌（CSS 变量） */
@import './assets/styles/base.css';       /* 基础样式重置 */
@import './assets/styles/utilities.css';  /* 通用工具类 */
@import './assets/styles/animations.css'; /* 动画定义 */

/* 应用程序特定样式 */
#app {
  min-height: 100vh;
}
</style>
