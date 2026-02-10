# Toast 通知服务

## 概述

Toast 通知服务提供了一个统一的接口来显示应用程序中的通知消息。它封装了 `vue-toastification` 库，提供了简洁易用的 API。

## 功能特性

- ✅ 支持四种通知类型：成功、错误、警告、信息
- ✅ 自动管理通知的显示和隐藏
- ✅ 可配置的显示时长
- ✅ 支持点击关闭和悬停暂停
- ✅ 提供清除单个或所有通知的方法
- ✅ 优雅的后备方案（在 Vue 上下文外使用时）

## 使用方法

### 基本用法

```javascript
import toast from '@/services/toast'

// 显示成功通知
toast.success('操作成功')

// 显示错误通知
toast.error('操作失败')

// 显示警告通知
toast.warning('请注意')

// 显示信息通知
toast.info('提示信息')
```

### 自定义选项

```javascript
// 自定义显示时长
toast.success('保存成功', { timeout: 5000 })

// 禁用点击关闭
toast.error('严重错误', { 
  timeout: 10000,
  closeOnClick: false 
})

// 禁用悬停暂停
toast.warning('警告', { 
  pauseOnHover: false 
})
```

### 管理通知

```javascript
// 保存通知 ID 以便后续清除
const toastId = toast.info('加载中...')

// 清除特定通知
toast.clear(toastId)

// 清除所有通知
toast.clearAll()
```

## API 参考

### toast.success(message, options)

显示成功通知。

**参数：**
- `message` (string): 通知消息
- `options` (object, 可选): 配置选项
  - `timeout` (number): 显示时长（毫秒），默认 3000
  - `closeOnClick` (boolean): 点击关闭，默认 true
  - `pauseOnHover` (boolean): 悬停暂停，默认 true

**返回值：** Toast 实例 ID

**示例：**
```javascript
toast.success('看板创建成功')
toast.success('保存成功', { timeout: 5000 })
```

### toast.error(message, options)

显示错误通知。

**参数：**
- `message` (string): 错误消息
- `options` (object, 可选): 配置选项
  - `timeout` (number): 显示时长（毫秒），默认 5000（错误消息显示更久）
  - `closeOnClick` (boolean): 点击关闭，默认 true
  - `pauseOnHover` (boolean): 悬停暂停，默认 true

**返回值：** Toast 实例 ID

**示例：**
```javascript
toast.error('操作失败')
toast.error('网络连接失败，请重试', { timeout: 10000 })
```

### toast.warning(message, options)

显示警告通知。

**参数：**
- `message` (string): 警告消息
- `options` (object, 可选): 配置选项
  - `timeout` (number): 显示时长（毫秒），默认 4000
  - `closeOnClick` (boolean): 点击关闭，默认 true
  - `pauseOnHover` (boolean): 悬停暂停，默认 true

**返回值：** Toast 实例 ID

**示例：**
```javascript
toast.warning('请注意')
toast.warning('即将超时', { timeout: 6000 })
```

### toast.info(message, options)

显示信息通知。

**参数：**
- `message` (string): 信息消息
- `options` (object, 可选): 配置选项
  - `timeout` (number): 显示时长（毫秒），默认 3000
  - `closeOnClick` (boolean): 点击关闭，默认 true
  - `pauseOnHover` (boolean): 悬停暂停，默认 true

**返回值：** Toast 实例 ID

**示例：**
```javascript
toast.info('提示信息')
toast.info('新功能已上线', { timeout: 5000 })
```

### toast.clear(toastId)

清除指定的 Toast 通知。

**参数：**
- `toastId` (object): Toast 实例 ID（由 success/error/warning/info 返回）

**示例：**
```javascript
const id = toast.info('加载中...')
// ... 稍后
toast.clear(id)
```

### toast.clearAll()

清除所有 Toast 通知。

**示例：**
```javascript
toast.clearAll()
```

## 默认配置

不同类型的通知有不同的默认显示时长：

| 类型 | 默认时长 | 说明 |
|------|---------|------|
| success | 3000ms | 成功消息快速消失 |
| error | 5000ms | 错误消息显示更久，便于用户阅读 |
| warning | 4000ms | 警告消息适中时长 |
| info | 3000ms | 信息消息快速消失 |

所有通知默认支持：
- 点击关闭 (`closeOnClick: true`)
- 悬停暂停 (`pauseOnHover: true`)

## 在 Vuex Store 中使用

```javascript
import api, { toast } from '@/services/api'

const actions = {
  async createBoard({ commit }, boardData) {
    try {
      const response = await api.createBoard(boardData)
      commit('addBoard', response.data)
      
      // 显示成功通知
      toast.success('看板创建成功')
      
      return response.data
    } catch (error) {
      // 错误通知由 API 拦截器自动处理
      throw error
    }
  }
}
```

## 在组件中使用

```vue
<template>
  <button @click="handleSave">保存</button>
</template>

<script>
import toast from '@/services/toast'

export default {
  methods: {
    async handleSave() {
      try {
        await this.saveData()
        toast.success('保存成功')
      } catch (error) {
        toast.error('保存失败：' + error.message)
      }
    }
  }
}
</script>
```

## 错误处理

Toast 服务具有内置的错误处理机制：

1. **Vue 上下文检测**：如果在 Vue 应用上下文外调用，会自动使用 console 作为后备方案
2. **优雅降级**：即使 toast 初始化失败，应用程序也不会崩溃
3. **错误日志**：所有错误都会记录到控制台，便于调试

## 技术实现

- **延迟初始化**：Toast 实例在首次使用时才创建，确保在 Vue 应用上下文中
- **单例模式**：整个应用共享一个 toast 实例，避免重复创建
- **选项合并**：自定义选项与默认选项智能合并

## 需求映射

- **需求 7.2**：操作成功时显示简洁的成功提示
- **需求 7.3**：操作失败时显示清晰的错误信息

## 相关文件

- `frontend/src/services/toast.js` - Toast 服务实现
- `frontend/src/services/api.js` - API 服务（使用 toast 显示错误）
- `frontend/src/store/modules/boards.js` - Boards Store（使用 toast 显示成功消息）
- `frontend/src/store/modules/lists.js` - Lists Store（使用 toast 显示成功消息）
- `frontend/src/store/modules/cards.js` - Cards Store（使用 toast 显示成功消息）
- `frontend/tests/unit/services/toast-service.spec.js` - Toast 服务单元测试
