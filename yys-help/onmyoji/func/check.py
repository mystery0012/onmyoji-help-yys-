import logging
from func import hwnd
from config import CONFIG  

def check_game_window():
    """检查游戏窗口是否存在"""
    try:
        if not hwnd.return_handle():
            error_msg = "找不到游戏窗口，请确保游戏已启动"
            logging.error(error_msg)
            print(error_msg)
            return False
        return True
    except Exception as e:
        logging.error(f"检查游戏窗口时发生错误: {str(e)}")
        return False
    
def process_user_input(input_str):
    """处理用户输入"""
    try:
        if input_str.lower() == 'restart':
            logging.info("用户请求重启程序")
            return 'restart', None
        elif input_str.lower() == 's':
            logging.info("用户请求退出程序")
            return 'exit', None
        else:
            try:
                value = int(input_str)
                logging.info(f"用户设置攻打次数: {value}")
                return 'value', value
            except ValueError:
                value = CONFIG['GAME']['DEFAULT_ATTACK_TIMES']
                logging.warning(f"无效输入，使用默认值: {value}")
                return 'value', value
    except Exception as e:
        logging.error(f"处理用户输入时发生错误: {str(e)}")
        return 'error', None