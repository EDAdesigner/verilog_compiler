# Verilog 编译器前端项目

## 项目简介

这是一个基于 Vue 3 开发的 Verilog 编译器前端界面，提供代码编辑、仿真和可视化功能。项目采用现代化前端技术栈，具有良好的可维护性和扩展性。

## 技术栈

- **前端框架**: Vue 3 + Composition API
- **UI 组件库**: Element Plus
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router
- **代码编辑器**: Monaco Editor
- **可视化**: ECharts

## 项目结构

```
verilog-compiler/
├── public/                # 静态资源
├── src/
│   ├── assets/            # 静态资源
│   ├── components/        # 公共组件
│   │   └── TheSidebar.vue # 侧边栏组件
│   ├── pages/             # 页面组件
│   │   ├── Home.vue       # 首页
│   │   ├── Editor.vue     # 代码编辑器
│   │   ├── Simulate.vue   # 仿真页面
│   │   └── Visualize.vue  # 可视化页面
│   ├── router/            # 路由配置
│   │   └── index.js
│   ├── stores/            # 状态管理
│   │   └── useEditorStore.js
│   ├── utils/             # 工具函数
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── .gitignore
├── package.json
├── README.md
└── vite.config.js
```

## 快速开始

### 环境准备

确保已安装：
- Node.js (>=16.0.0)
- npm (>=8.0.0) 或 yarn

### 安装依赖

```bash
npm install
# 或
yarn install
```

### 开发模式

```bash
npm run dev
# 或
yarn dev
```

开发服务器将运行在 [http://localhost:3000](http://localhost:3000)

### 生产构建

```bash
npm run build
# 或
yarn build
```

构建产物将输出到 `dist/` 目录

## 功能特性

- 支持 Verilog 语法高亮和代码补全
- 实时编译错误检查
- 波形仿真可视化
- 模块依赖关系图展示
- 响应式布局，适配多种设备

## 开发指南

1. 组件开发请遵循 Vue 3 Composition API 规范
2. 全局状态使用 Pinia 管理
3. 新页面需在 `router/index.js` 中注册路由
4. 提交代码前请运行 lint 检查：
   ```bash
   npm run lint
   ```

## 贡献方式

欢迎通过以下方式参与贡献：
- 提交 Issues 报告问题
- 发起 Pull Requests 贡献代码
- 完善项目文档

## 许可证

[MIT License](LICENSE) © 2023 EDAdesigner