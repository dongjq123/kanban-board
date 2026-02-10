-- 数据库迁移脚本 002: 创建 users 表
-- 创建用户认证表，包含用户名、邮箱、密码哈希等字段
-- 需求：9.1, 9.3

-- 设置字符集为 utf8mb4 以支持完整的 Unicode（包括 emoji）
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ============================================================================
-- 创建 users 表
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户唯一标识符',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名（唯一）',
    email VARCHAR(255) NOT NULL UNIQUE COMMENT '邮箱地址（唯一）',
    password_hash VARCHAR(255) NOT NULL COMMENT 'bcrypt 加密的密码哈希',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    
    -- 约束：用户名长度至少 3 个字符
    CONSTRAINT username_length CHECK (CHAR_LENGTH(username) >= 3),
    
    -- 约束：邮箱格式验证（基本格式检查）
    CONSTRAINT email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    
    -- 索引：用于快速查询用户名
    INDEX idx_users_username (username),
    
    -- 索引：用于快速查询邮箱
    INDEX idx_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
