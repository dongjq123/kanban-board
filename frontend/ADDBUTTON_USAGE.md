# AddButton 组件使用指南

## 概述

`AddButton` 是一个可复用的通用添加按钮组件，用于在应用中实现"添加"功能。它支持内联输入和提交，可以配置为文本输入或多行文本输入。

## 功能特性

- ✅ 可复用的添加按钮组件
- ✅ 支持文本输入（`input`）和多行文本输入（`textarea`）
- ✅ 内联表单显示/隐藏
- ✅ 键盘快捷键支持（Enter 提交，Esc 取消）
- ✅ 自动聚焦输入框
- ✅ 输入验证（去除首尾空格，禁止空内容提交）
- ✅ 禁用状态支持
- ✅ 外部控制表单显示
- ✅ 完全可自定义的文本

## 基本用法

### 1. 文本输入模式（适用于添加列表）

```vue
<template>
  <AddButton
    button-text="+ 添加列表"
    submit-text="添加列表"
    placeholder="输入列表名称..."
    input-type="text"
    @submit="handleAddList"
    @cancel="handleCancel"
  />
</template>

<script>
import AddButton from '@/components/AddButton.vue'

export default {
  components: {
    AddButton
  },
  methods: {
    handleAddList(name) {
      console.log('添加列表:', name)
      // 调用 API 创建列表
    },
    handleCancel() {
      console.log('取消添加')
    }
  }
}
</script>
```

### 2. 多行文本输入模式（适用于添加卡片）

```vue
<template>
  <AddButton
    button-text="+ 添加卡片"
    submit-text="添加卡片"
    placeholder="输入卡片标题..."
    input-type="textarea"
    :textarea-rows="3"
    @submit="handleAddCard"
  />
</template>

<script>
import AddButton from '@/components/AddButton.vue'

export default {
  components: {
    AddButton
  },
  methods: {
    handleAddCard(title) {
      console.log('添加卡片:', title)
      // 调用 API 创建卡片
    }
  }
}
</script>
```

## Props 属性

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `buttonText` | String | `'+ 添加'` | 添加按钮显示的文本 |
| `submitText` | String | `'添加'` | 提交按钮显示的文本 |
| `placeholder` | String | `'输入内容...'` | 输入框的占位符文本 |
| `inputType` | String | `'text'` | 输入框类型，可选值：`'text'` 或 `'textarea'` |
| `textareaRows` | Number | `3` | 多行文本输入框的行数（仅当 `inputType` 为 `'textarea'` 时有效） |
| `disabled` | Boolean | `false` | 是否禁用组件 |
| `visible` | Boolean | `false` | 外部控制表单显示状态（支持 `.sync` 修饰符） |
| `variant` | String | `'ghost'` | 按钮变体样式，可选值：`'primary'`、`'secondary'` 或 `'ghost'` |

## Events 事件

| 事件名 | 参数 | 说明 |
|--------|------|------|
| `submit` | `(value: string)` | 用户提交表单时触发，参数为输入的内容（已去除首尾空格） |
| `cancel` | - | 用户取消添加时触发 |
| `update:visible` | `(visible: boolean)` | 表单显示状态变化时触发（用于外部控制） |

## 键盘快捷键

- **Enter**：提交表单（文本输入模式）
- **Enter**（不按 Shift）：提交表单（多行文本输入模式）
- **Shift + Enter**：换行（多行文本输入模式）
- **Esc**：取消并隐藏表单

## 高级用法

### 按钮变体样式

组件支持三种按钮变体样式，适用于不同的使用场景：

#### 1. Ghost 变体（默认）
透明背景，适合在列表或卡片容器中使用：

```vue
<AddButton
  variant="ghost"
  button-text="+ 添加卡片"
  @submit="handleSubmit"
/>
```

#### 2. Primary 变体
主色调背景，适合强调重要的添加操作：

```vue
<AddButton
  variant="primary"
  button-text="+ 创建新看板"
  @submit="handleSubmit"
/>
```

#### 3. Secondary 变体
次要样式，适合辅助性的添加操作：

```vue
<AddButton
  variant="secondary"
  button-text="+ 添加标签"
  @submit="handleSubmit"
/>
```

### 外部控制表单显示

```vue
<template>
  <div>
    <button @click="showForm = true">打开表单</button>
    
    <AddButton
      :visible.sync="showForm"
      @submit="handleSubmit"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      showForm: false
    }
  },
  methods: {
    handleSubmit(value) {
      console.log('提交:', value)
      this.showForm = false
    }
  }
}
</script>
```

### 禁用状态

```vue
<template>
  <AddButton
    :disabled="loading"
    @submit="handleSubmit"
  />
</template>

<script>
export default {
  data() {
    return {
      loading: false
    }
  },
  methods: {
    async handleSubmit(value) {
      this.loading = true
      try {
        await this.createItem(value)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
```

## 样式自定义

组件使用 scoped 样式，如果需要自定义样式，可以通过以下方式：

### 1. 使用 CSS 变量（推荐）

```vue
<style>
.add-button-container {
  --button-bg-color: #0079bf;
  --button-hover-bg-color: #026aa7;
}
</style>
```

### 2. 使用深度选择器

```vue
<style>
::v-deep .btn-add {
  color: #ff0000;
}
</style>
```

## 在 Board.vue 中使用示例

```vue
<template>
  <div class="board">
    <!-- 其他内容 -->
    
    <!-- 使用 AddButton 替代原有的添加列表功能 -->
    <div class="add-list-container">
      <AddButton
        button-text="+ 添加列表"
        submit-text="添加列表"
        placeholder="输入列表名称..."
        input-type="text"
        :disabled="loading"
        @submit="handleCreateList"
      />
    </div>
  </div>
</template>

<script>
import AddButton from '@/components/AddButton.vue'

export default {
  components: {
    AddButton
  },
  methods: {
    async handleCreateList(name) {
      const position = this.lists.length
      await this.createList({
        boardId: this.currentBoard.id,
        data: { name, position }
      })
    }
  }
}
</script>
```

## 在 List.vue 中使用示例

```vue
<template>
  <div class="list">
    <!-- 其他内容 -->
    
    <!-- 使用 AddButton 替代原有的添加卡片功能 -->
    <div class="add-card-container">
      <AddButton
        button-text="+ 添加卡片"
        submit-text="添加卡片"
        placeholder="输入卡片标题..."
        input-type="textarea"
        :textarea-rows="3"
        :disabled="loading"
        @submit="handleCreateCard"
      />
    </div>
  </div>
</template>

<script>
import AddButton from '@/components/AddButton.vue'

export default {
  components: {
    AddButton
  },
  methods: {
    async handleCreateCard(title) {
      const position = this.cards.length
      await this.createCard({
        listId: this.list.id,
        data: { title, position }
      })
    }
  }
}
</script>
```

## 注意事项

1. **输入验证**：组件会自动去除输入内容的首尾空格，空内容或仅包含空格的内容无法提交。

2. **自动聚焦**：当表单显示时，输入框会自动获得焦点，提升用户体验。

3. **键盘操作**：
   - 在文本输入模式下，按 Enter 键会立即提交
   - 在多行文本输入模式下，按 Enter 键（不按 Shift）会提交，按 Shift + Enter 会换行

4. **事件处理**：`submit` 事件的参数已经是处理过的字符串（去除首尾空格），可以直接使用。

5. **样式继承**：按钮的颜色会继承父元素的 `color` 属性，便于在不同背景下使用。

## 测试覆盖

组件包含完整的单元测试，覆盖以下场景：

- ✅ 基本渲染
- ✅ 表单显示/隐藏
- ✅ 文本输入和多行文本输入
- ✅ 提交和取消操作
- ✅ 键盘快捷键
- ✅ 禁用状态
- ✅ 外部控制
- ✅ 自定义文本
- ✅ 边缘情况

测试文件位置：`tests/unit/components/AddButton.spec.js`

运行测试：
```bash
npm run test:unit -- AddButton.spec.js
```

## 相关需求

- 需求 1.1：允许用户创建新的看板
- 需求 2.1：允许用户在看板中添加工作列表
- 需求 3.2：点击"添加卡片"按钮创建新卡片
