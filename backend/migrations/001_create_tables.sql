-- 数据库迁移脚本 001: 创建基础表结构
-- 创建 boards、lists、cards 表，配置外键约束和索引
-- 需求：7.1, 7.2, 7.3, 7.4

-- 设置字符集为 utf8mb4 以支持完整的 Unicode（包括 emoji）
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ============================================================================
-- 创建 boards 表
-- ============================================================================
CREATE TABLE IF NOT EXISTS boards (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '看板唯一标识符',
    name VARCHAR(255) NOT NULL COMMENT '看板名称',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
    
    -- 索引
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='看板表';

-- ============================================================================
-- 创建 lists 表
-- ============================================================================
CREATE TABLE IF NOT EXISTS lists (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '列表唯一标识符',
    board_id INT NOT NULL COMMENT '所属看板 ID',
    name VARCHAR(255) NOT NULL COMMENT '列表名称',
    position INT NOT NULL DEFAULT 0 COMMENT '列表在看板中的位置顺序',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
    
    -- 外键约束：级联删除
    FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_board_id (board_id),
    INDEX idx_position (position),
    INDEX idx_board_position (board_id, position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工作列表表';

-- ============================================================================
-- 创建 cards 表
-- ============================================================================
CREATE TABLE IF NOT EXISTS cards (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '卡片唯一标识符',
    list_id INT NOT NULL COMMENT '所属列表 ID',
    title VARCHAR(255) NOT NULL COMMENT '卡片标题',
    description TEXT COMMENT '卡片描述（可选）',
    due_date DATE COMMENT '截止日期（可选）',
    tags JSON COMMENT '标签数组，存储为 JSON 格式（可选）',
    position INT NOT NULL DEFAULT 0 COMMENT '卡片在列表中的位置顺序',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
    
    -- 外键约束：级联删除
    FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_list_id (list_id),
    INDEX idx_position (position),
    INDEX idx_due_date (due_date),
    INDEX idx_list_position (list_id, position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务卡片表';
