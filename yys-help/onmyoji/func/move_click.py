from config import CONFIG
import random
import pyautogui
import time
import logging

def move_click(target_x=0, target_y=0):
    try:
        double_click = CONFIG['MOUSE']['DOUBLE_CLICK']
        # 从配置文件获取参数
        offset_min = CONFIG['MOUSE']['OFFSET_MIN']
        offset_max = CONFIG['MOUSE']['OFFSET_MAX']
        
        x_offset = random.randint(offset_min, offset_max)
        y_offset = random.randint(offset_min, offset_max)
        
        actual_x = target_x + x_offset
        actual_y = target_y + y_offset
        
        # 添加更自然的鼠标移动
        duration = random.uniform(
            CONFIG['MOUSE']['MOVE_DURATION_MIN'],
            CONFIG['MOUSE']['MOVE_DURATION_MAX']
        )
        
        # 记录操作日志
        logging.debug(f"移动鼠标到: ({actual_x}, {actual_y}), 偏移量: ({x_offset}, {y_offset})")
        
        pyautogui.moveTo(actual_x, actual_y, duration=duration, tween=pyautogui.easeInOutQuad)
        time.sleep(0.1)
        
        if double_click:
            pyautogui.doubleClick()
        else:
            pyautogui.click()
            
        return True
        
    except Exception as e:
        logging.error(f"鼠标操作失败: {str(e)}")
        return False






