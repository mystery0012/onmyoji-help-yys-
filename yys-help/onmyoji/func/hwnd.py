import win32gui
import sys
import logging
from config import CONFIG

# 定义一个函数来查找窗口句柄
def find_window_handle(window_title):
    # 使用win32gui.FindWindow函数根据窗口标题查找窗口句柄
    # 第一个参数是窗口的类名，可以设置为None来忽略类名匹配
    # 第二个参数是窗口的标题，设置为要查找的窗口标题
    hwnd = win32gui.FindWindow(None, window_title)

    # 如果找到了窗口，返回句柄值
    # 如果没找到，返回None
    return hwnd

def get_window_position(hwnd):
    """获取窗口位置"""
    try:
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        return x, y
    except Exception as e:
        logging.error(f"获取窗口位置时发生错误: {str(e)}")
        return None, None

def check_window():
    """
    检查游戏窗口是否存在
    返回: bool - True 表示窗口存在，False 表示窗口不存在
    """
    try:
        window_title = CONFIG['WINDOW']['TITLE']
        handle = find_window_handle(window_title)
        
        if handle != 0:
            # 获取并记录窗口位置
            x, y = get_window_position(handle)
            if x is not None and y is not None:
                logging.info(f"找到游戏窗口，句柄值: {handle:#x}, 窗口位置: ({x}, {y})")
            return True
        else:
            logging.warning(f"未找到标题为 '{window_title}' 的窗口")
            return False
            
    except Exception as e:
        logging.error(f"检查窗口时发生错误: {str(e)}")
        return False

def return_handle():
    # 调用函数查找名为"Calculator"的窗口句柄（这里以计算器为例）
    # 注意：你需要将"Calculator"替换为你实际要查找的窗口标题
    window_title = CONFIG['WINDOW']['TITLE']
    handle = find_window_handle(window_title)
    # 检查是否找到了窗口句柄
    if handle != 0:  # 注意：在Windows中，0通常不是一个有效的窗口句柄，但最好检查是否为None或特定的无效值
        # 获取并记录窗口位置
        x, y = get_window_position(handle)
        if x is not None and y is not None:
            logging.info(f"窗口句柄值: {handle:#x}, 窗口位置: ({x}, {y})")
        return handle
    else:
        # 如果没有找到窗口，打印错误信息
        logging.error(f"未找到标题为'{window_title}'的窗口")
        print(f"未找到标题为'{window_title}'的窗口")
        print(f"程序结束")
        sys.exit()
    # 注意：在实际应用中，窗口标题可能包含特殊字符或空格，
    # 因此确保你提供的窗口标题与系统中实际显示的标题完全匹配。
    # 另外，由于窗口可能随时关闭或打开，因此最好在需要时立即查找句柄。

