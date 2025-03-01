CONFIG = {
    'WINDOW': {
        'TITLE': '阴阳师-网易游戏',  # 游戏窗口标题
        'CHECK_INTERVAL': 1,  # 检查窗口间隔（秒）
    },
    
    'IMAGE_PATHS': {
        'HUNTU': 'picture//huntu.png',
        'JIANGLI': 'picture//jiangli.png',
        'SCREENSHOT': 'screenshot.jpg'  # 截图保存路径
    },
    
    'DELAYS': { 
        'CLICK_DELAY': 1,
        'LOOP_DELAY': 0.5,
        'RANDOM_DELAY_MIN': 0,
        'RANDOM_DELAY_MAX': 0.8,
        'ERROR_RETRY_DELAY': 1,
        'HUNTU_WAIT': 23,  # 魂土等待时间（秒）
    },
    
    'MOUSE': {
        'OFFSET_MIN': -10,
        'OFFSET_MAX': 10,
        'MOVE_DURATION_MIN': 0.3,
        'MOVE_DURATION_MAX': 0.8,
        'DOUBLE_CLICK': True  # 是否使用双击
    },
    
    'IMAGE_RECOGNITION': {
        'CONFIDENCE': 0.8,  # 图像识别置信度阈值
        'GRAYSCALE': True,  # 是否使用灰度图像识别
    },
    
    'LOGGING': {
        'LEVEL': 'DEBUG',  # 日志级别
        'FILE_PATH': 'logs',  # 日志文件路径
        'FILE_NAME_FORMAT': 'game_%Y%m%d_%H%M%S.log',  # 日志文件名格式
        'FORMAT': '%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
    },
    
    'GAME': {
        'DEFAULT_ATTACK_TIMES': 100,  # 默认攻打次数
        'MAX_RETRIES': 3,  # 最大重试次数
        'AUTO_RESTART': True  # 是否在错误后自动重启
    },
    
    'CONTROL': {
        'PAUSE_KEY': 'f9',      # 暂停/继续热键
        'EXIT_KEY': 'esc',      # 退出热键
        'CHECK_INTERVAL': 0.1,  # 暂停状态检查间隔（秒）
    },
} 