-- 数据库迁移脚本 001 回滚: 删除基础表结构
-- 删除 cards、lists、boards 表（按依赖顺序反向删除）

-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 删除表（按依赖顺序：先删除子表，再删除父表）
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS lists;
DROP TABLE IF EXISTS boards;
