"""注册功能模块
"""

__all__ = [
    'MAX_MODULES_NUMBER', 'MODULES', 'EXCLUDED_ENDPOINTS'
]

# 最大功能模块数量
MAX_MODULES_NUMBER = 32

# 功能模块编号
MODULES = {
    'main': 0,
    'api': 1
}

# 排除的endpoint
EXCLUDED_ENDPOINTS = [
    'main.favicon'
]
