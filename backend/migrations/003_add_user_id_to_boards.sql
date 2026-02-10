-- 数据库迁移脚本 003: 在 boards 表添加 user_id 外键
-- 为 boards 表添加 user_id 列，关联到 users 表
-- 需求：9.2, 9.4

-- 设置字符集为 utf8mb4 以支持完整的 Unicode（包括 emoji）
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ============================================================================
-- 在 boards 表添加 user_id 列
-- ============================================================================

-- 添加 user_id 列（外键引用 users.id）
ALTER TABLE boards 
ADD COLUMN user_id INT COMMENT '所属用户 ID';

-- 添加外键约束：级联删除（删除用户时自动删除其所有看板）
ALTER TABLE boards
ADD CONSTRAINT fk_boards_user_id 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- 创建索引以优化查询性能（按用户查询看板）
CREATE INDEX idx_boards_user_id ON boards(user_id);
