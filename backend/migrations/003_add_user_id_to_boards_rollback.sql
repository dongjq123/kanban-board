-- 数据库迁移脚本 003 回滚: 移除 boards 表的 user_id 外键
-- 回滚 003_add_user_id_to_boards.sql 的更改
-- 需求：9.2, 9.4

-- 设置字符集为 utf8mb4 以支持完整的 Unicode（包括 emoji）
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ============================================================================
-- 从 boards 表移除 user_id 列
-- ============================================================================

-- 删除索引
DROP INDEX idx_boards_user_id ON boards;

-- 删除外键约束
ALTER TABLE boards
DROP FOREIGN KEY fk_boards_user_id;

-- 删除 user_id 列
ALTER TABLE boards
DROP COLUMN user_id;
