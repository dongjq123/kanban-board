# Toast 通知组件

Toast 组件是一个现代化的通知提示组件，支持四种类型的通知消息，具有滑入滑出动画效果和自动关闭功能。

## 功能特性

- ✅ 四种通知类型：success、warning、error、info
- ✅ Material Icons 图标支持
- ✅ 标题和消息显示
- ✅ 关闭按钮
- ✅ 滑入滑出动画
- ✅ 3秒自动关闭（可配置）
- ✅ 可访问性支持（role="alert"）
- ✅ 使用 CSS 变量的现代化样式

## 使用方法

### 基本用法

```vue
<template>
  <div>
    <Toast
      type="success"
      title="操作成功"
      message="您的更改已保存"
      @close="handleClose"
    />
  </div>
</template>

<script>
import Toast from '@/components/Toast.vue'

export default {
  components: {
    Toast
  },
  methods: {
    handleClose() {
      console.log('Toast closed')
    }
  }
}
</script>
```

### Props

| 属性 | 类型 | 默认值 | 必需 | 说明 |
|------|------|--------|------|------|
| type | String | 'info' | 否 | 通知类型：'success', 'warning', 'error', 'info' |
| title | String | - | 是 | 通知标题 |
| message | String | '' | 否 | 通知消息内容 |
| duration | Number | 3000 | 否 | 自动关闭时长（毫秒） |
| autoClose | Boolean | true | 否 | 是否自动关闭 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| close | - | Toast 关闭时触发 |

### 示例

#### Success 通知

```vue
<Toast
  type="success"
  title="创建成功"
  message="新的看板已创建"
/>
```

#### Warning 通知

```vue
<Toast
  type="warning"
  title="注意"
  message="此操作无法撤销"
/>
```

#### Error 通知

```vue
<Toast
  type="error"
  title="操作失败"
  message="网络连接失败，请稍后重试"
/>
```

#### Info 通知

```vue
<Toast
  type="info"
  title="提示"
  message="您有新的消息"
/>
```

#### 自定义关闭时长

```vue
<Toast
  type="success"
  title="保存成功"
  :duration="5000"
/>
```

#### 禁用自动关闭

```vue
<Toast
  type="error"
  title="严重错误"
  message="请联系管理员"
  :auto-close="false"
/>
```

## 样式定制

Toast 组件使用 CSS 变量进行样式定制，您可以在全局样式中覆盖这些变量：

```css
:root {
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --radius-md: 12px;
}
```

## 可访问性

- Toast 容器具有 `role="alert"` 属性，便于屏幕阅读器识别
- 关闭按钮具有 `aria-label="Close notification"` 属性
- 支持键盘导航（关闭按钮可通过 Tab 键聚焦）

## 动画效果

Toast 使用 Vue 的 `<transition>` 组件实现滑入滑出动画：

- **进入动画**：从上方滑入，透明度从 0 到 1
- **离开动画**：向上滑出，透明度从 1 到 0
- **动画时长**：250ms（使用 `--transition-base` CSS 变量）

## 图标映射

| 类型 | Material Icon |
|------|---------------|
| success | check_circle |
| warning | warning |
| error | error |
| info | info |

## 注意事项

1. **Material Icons 依赖**：组件依赖 Material Icons 字体库，请确保在项目中已引入：
   ```html
   <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
   ```

2. **定时器清理**：组件在卸载时会自动清理定时器，无需手动处理

3. **事件处理**：关闭事件会在动画完成后触发（延迟 250ms），确保视觉效果流畅

## 需求映射

本组件实现了以下需求：

- **需求 7.2**：操作成功时显示简洁的成功提示
- **需求 7.3**：操作失败时显示清晰的错误信息
- **需求 7.5**：所有反馈信息在 3 秒内自动消失

## 测试覆盖

组件包含完整的单元测试，覆盖以下场景：

- ✅ 基本渲染
- ✅ 四种类型样式
- ✅ 图标显示
- ✅ 关闭功能
- ✅ 自动关闭逻辑
- ✅ Props 验证
- ✅ CSS 类名
- ✅ 可访问性
- ✅ 动画和过渡
- ✅ 边缘情况处理

测试文件：`tests/unit/components/Toast.spec.js`
