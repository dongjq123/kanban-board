# Frontend Dockerfile with multi-stage build
# 需求：8.1

# Stage 1: Build the Vue.js application
FROM node:18-alpine AS build

WORKDIR /app

# 复制 package files
COPY package*.json ./

# 安装依赖 (使用 --legacy-peer-deps 解决依赖冲突)
RUN npm ci --legacy-peer-deps

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# 复制构建产物到 Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
